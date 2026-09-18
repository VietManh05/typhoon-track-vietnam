"""NOAA IBTrACS v4r01 adapter, the primary normalised source."""

from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

from typhoon_vn.ingestion.http import HttpDownloader
from typhoon_vn.ingestion.identifiers import canonical_storm_id
from typhoon_vn.ingestion.lineage import write_download_lineage
from typhoon_vn.ingestion.models import DownloadResult, Observation

DEFAULT_IBTRACS_URL = (
    "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-"
    "stewardship-ibtracs/v04r01/access/csv/ibtracs.WP.list.v04r01.csv"
)


class IBTrACSProvider:
    """Acquire the Western Pacific subset of NOAA's frequently updated archive."""

    source = "ibtracs"

    def __init__(self, url: str | None = None) -> None:
        self.url = url or os.getenv("IBTRACS_URL") or DEFAULT_IBTRACS_URL

    def download(
        self,
        *,
        data_root: Path,
        downloader: HttpDownloader | None = None,
    ) -> DownloadResult:
        """Fetch the official WP CSV and persist download provenance."""

        result = (downloader or HttpDownloader()).fetch(
            source=self.source,
            url=self.url,
            destination=(
                data_root / "raw" / "downloads" / self.source / "ibtracs-wp.csv"
            ),
        )
        write_download_lineage(
            result,
            data_root=data_root,
            dataset_version="IBTrACS v04r01",
            parser="parse_ibtracs_csv",
            licence_note="NOAA NCEI IBTrACS v04r01; retain required citation.",
        )
        return result


def parse_ibtracs_csv(
    text: str,
    *,
    source_url: str,
    checksum: str,
    dataset_version: str = "IBTrACS v04r01",
    basin: str = "WP",
) -> list[Observation]:
    """Parse the official CSV while ignoring its units-description row."""

    reader = csv.DictReader(StringIO(text))
    observations: list[Observation] = []
    for row in reader:
        timestamp = _parse_timestamp(row.get("ISO_TIME", ""))
        latitude = _float_or_none(row.get("LAT"))
        longitude = _float_or_none(row.get("LON"))
        row_basin = (row.get("BASIN") or "").strip().upper()
        if timestamp is None or latitude is None or longitude is None:
            continue
        if basin and row_basin != basin:
            continue
        source_id = (row.get("SID") or "").strip()
        atcf_id = (row.get("USA_ATCF_ID") or "").strip()
        observations.append(
            Observation(
                source="ibtracs",
                source_storm_id=source_id,
                storm_id=canonical_storm_id(
                    atcf_id,
                    basin=row_basin or basin,
                    season=timestamp.year,
                ),
                timestamp=timestamp,
                latitude=latitude,
                longitude=longitude,
                wind=_first_float(row, "USA_WIND", "WMO_WIND"),
                wind_unit="kt",
                pressure_hpa=_first_float(row, "USA_PRES", "WMO_PRES"),
                storm_name=(row.get("NAME") or "").strip() or None,
                source_url=source_url,
                source_file_checksum=checksum,
                dataset_version=dataset_version,
                metadata={
                    "ibtracs_sid": source_id,
                    "usa_atcf_id": atcf_id or None,
                    "agency": (row.get("USA_AGENCY") or "").strip() or None,
                },
            )
        )
    return observations


def _parse_timestamp(value: str) -> datetime | None:
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        return None


def _float_or_none(value: str | None) -> float | None:
    try:
        return float(value) if value not in (None, "", " ") else None
    except ValueError:
        return None


def _first_float(row: dict[str, str], *columns: str) -> float | None:
    for column in columns:
        value = _float_or_none(row.get(column))
        if value is not None:
            return value
    return None
