"""China Meteorological Administration CMA-BST acquisition and parsing."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from typhoon_vn.ingestion.http import HttpDownloader
from typhoon_vn.ingestion.identifiers import canonical_storm_id
from typhoon_vn.ingestion.lineage import write_download_lineage
from typhoon_vn.ingestion.models import DownloadResult, Observation

DEFAULT_CMA_BASE_URL = "https://tcdata.typhoon.org.cn/data/CMABSTdata"


class CMAProvider:
    """CMA's annual ``CHYYYYBST.txt`` files, available from 1949 onward."""

    source = "cma"

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (
            base_url or os.getenv("CMA_BASE_URL") or DEFAULT_CMA_BASE_URL
        ).rstrip("/")

    def url_for_year(self, year: int) -> str:
        """Build the published annual URL without relying on a directory index."""

        return f"{self.base_url}/CH{year}BST.txt"

    def download_years(
        self,
        years: Iterable[int],
        *,
        data_root: Path,
        downloader: HttpDownloader | None = None,
    ) -> list[DownloadResult]:
        """Fetch requested annual files with retry, checksum, and lineage."""

        client = downloader or HttpDownloader()
        results: list[DownloadResult] = []
        for year in years:
            url = self.url_for_year(year)
            target = data_root / "raw" / "downloads" / self.source / str(year)
            result = client.fetch(
                source=self.source,
                url=url,
                destination=target / f"CH{year}BST.txt",
            )
            write_download_lineage(
                result,
                data_root=data_root,
                dataset_version="CMA-BST annual file",
                parser="parse_cma_text",
                licence_note="Cite tcdata.typhoon.org.cn and CMA-BST references.",
            )
            results.append(result)
        return results


def parse_cma_text(
    text: str,
    *,
    source_url: str,
    checksum: str,
    dataset_version: str | None = None,
) -> list[Observation]:
    """Parse CMA whitespace records without restricting the historical period.

    CMA has revised header layout over time. This parser interprets only data
    rows containing a full UTC datetime and documented position/intensity fields;
    raw objects remain available whenever a row needs source-specific review.
    """

    current_source_id = "UNKNOWN"
    observations: list[Observation] = []
    for raw_line in text.splitlines():
        fields = raw_line.split()
        if not fields:
            continue
        if fields[0] == "66666":
            current_source_id = _header_storm_id(fields)
            continue
        parsed = _parse_cma_record(fields)
        if parsed is None:
            continue
        timestamp, category, latitude, longitude, pressure, wind = parsed
        observations.append(
            Observation(
                source="cma",
                source_storm_id=current_source_id,
                storm_id=canonical_storm_id(
                    current_source_id,
                    basin="WP",
                    season=timestamp.year,
                ),
                timestamp=timestamp,
                latitude=latitude,
                longitude=longitude,
                pressure_hpa=pressure,
                wind=wind,
                wind_unit="m/s",
                intensity_code=category,
                source_url=source_url,
                source_file_checksum=checksum,
                dataset_version=dataset_version,
            )
        )
    return observations


def _header_storm_id(fields: list[str]) -> str:
    candidates = [field for field in fields[1:] if field.isdigit()]
    if len(candidates) >= 2:
        return candidates[1]
    return candidates[0] if candidates else "UNKNOWN"


def _parse_cma_record(
    fields: list[str],
) -> tuple[datetime, str, float, float, float | None, float | None] | None:
    datetime_token = fields[0]
    offset = 1
    if len(datetime_token) == 8 and len(fields) >= 7 and fields[1].isdigit():
        datetime_token = f"{datetime_token}{fields[1].zfill(2)}"
        offset = 2
    if (
        len(datetime_token) != 10
        or not datetime_token.isdigit()
        or len(fields) < offset + 5
    ):
        return None
    try:
        timestamp = datetime.strptime(datetime_token, "%Y%m%d%H").replace(
            tzinfo=timezone.utc
        )
        category = fields[offset]
        latitude = float(fields[offset + 1]) / 10
        longitude = float(fields[offset + 2]) / 10
        pressure = _positive_float(fields[offset + 3])
        wind = _positive_float(fields[offset + 4])
    except ValueError:
        return None
    return timestamp, category, latitude, longitude, pressure, wind


def _positive_float(value: str) -> float | None:
    number = float(value)
    return number if number > 0 else None
