"""JMA RSMC Tokyo best-track archive adapter."""

from __future__ import annotations

import os
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from typhoon_vn.ingestion.http import HttpDownloader
from typhoon_vn.ingestion.identifiers import canonical_storm_id
from typhoon_vn.ingestion.lineage import write_download_lineage
from typhoon_vn.ingestion.models import DownloadResult, Observation

DEFAULT_JMA_BEST_TRACK_URL = (
    "https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/"
    "Besttracks/bst_all.zip"
)


class JMAProvider:
    """Download JMA's all-years text archive (1951 onward)."""

    source = "jma"

    def __init__(self, url: str | None = None) -> None:
        self.url = url or os.getenv("JMA_BEST_TRACK_URL") or DEFAULT_JMA_BEST_TRACK_URL

    def download(
        self,
        *,
        data_root: Path,
        downloader: HttpDownloader | None = None,
    ) -> DownloadResult:
        """Fetch the public archive and emit an immutable lineage manifest."""

        result = (downloader or HttpDownloader()).fetch(
            source=self.source,
            url=self.url,
            destination=data_root / "raw" / "downloads" / self.source / "bst_all.zip",
        )
        write_download_lineage(
            result,
            data_root=data_root,
            dataset_version="JMA RSMC Best Track",
            parser="parse_jma_archive",
            licence_note="JMA RSMC Tokyo Best Track Data; retain source notice.",
        )
        return result


def parse_jma_archive(
    archive: Path,
    *,
    source_url: str,
    checksum: str,
) -> list[Observation]:
    """Parse every text member from JMA's all-years ZIP archive."""

    observations: list[Observation] = []
    with zipfile.ZipFile(archive) as bundle:
        for name in bundle.namelist():
            if not name.lower().endswith(".txt"):
                continue
            text = bundle.read(name).decode("utf-8", errors="replace")
            observations.extend(
                parse_jma_text(text, source_url=source_url, checksum=checksum)
            )
    return observations


def parse_jma_text(
    text: str,
    *,
    source_url: str,
    checksum: str,
) -> list[Observation]:
    """Parse the documented JMA header/data record stream."""

    source_id = "UNKNOWN"
    storm_name: str | None = None
    observations: list[Observation] = []
    for raw_line in text.splitlines():
        fields = raw_line.split()
        if not fields:
            continue
        if fields[0] == "66666":
            source_id = fields[1] if len(fields) > 1 else "UNKNOWN"
            storm_name = fields[7] if len(fields) > 7 else None
            continue
        if len(fields) < 6 or len(fields[0]) != 8 or not fields[0].isdigit():
            continue
        try:
            timestamp = _parse_jma_time(fields[0])
            latitude = float(fields[3]) / 10
            longitude = float(fields[4]) / 10
            pressure = _positive(fields[5])
            wind = _positive(fields[6]) if len(fields) > 6 else None
        except ValueError:
            continue
        observations.append(
            Observation(
                source="jma",
                source_storm_id=source_id,
                storm_id=canonical_storm_id(source_id, basin="WP"),
                timestamp=timestamp,
                latitude=latitude,
                longitude=longitude,
                pressure_hpa=pressure,
                wind=wind,
                wind_unit="kt",
                storm_name=storm_name,
                intensity_code=fields[2],
                source_url=source_url,
                source_file_checksum=checksum,
                dataset_version="JMA RSMC Best Track",
            )
        )
    return observations


def _parse_jma_time(value: str) -> datetime:
    year = int(value[:2])
    full_year = 1900 + year if year >= 51 else 2000 + year
    return datetime(
        full_year,
        int(value[2:4]),
        int(value[4:6]),
        int(value[6:8]),
        tzinfo=timezone.utc,
    )


def _positive(value: str) -> float | None:
    number = float(value)
    return number if number > 0 else None
