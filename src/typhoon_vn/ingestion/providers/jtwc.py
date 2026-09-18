"""JTWC ATCF best-track parser and manifest-based acquisition."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from urllib.parse import urlparse

from typhoon_vn.ingestion.http import HttpDownloader
from typhoon_vn.ingestion.lineage import write_download_lineage
from typhoon_vn.ingestion.models import DownloadResult, Observation


def download_manifest(
    manifest: Path,
    *,
    data_root: Path,
    downloader: HttpDownloader | None = None,
) -> list[DownloadResult]:
    """Download approved JTWC URLs listed one per line in a manifest.

    JTWC archive publication structure can change. Keeping an approved,
    versioned manifest avoids silently crawling a moved or restricted endpoint.
    """

    client = downloader or HttpDownloader()
    results: list[DownloadResult] = []
    for raw_url in manifest.read_text(encoding="utf-8").splitlines():
        url = raw_url.strip()
        if not url or url.startswith("#"):
            continue
        filename = Path(urlparse(url).path).name or "jtwc-best-track.dat"
        result = client.fetch(
            source="jtwc",
            url=url,
            destination=data_root / "raw" / "downloads" / "jtwc" / filename,
        )
        write_download_lineage(
            result,
            data_root=data_root,
            dataset_version="JTWC Best Track",
            parser="parse_jtwc_atcf",
            licence_note="JTWC Best Track archive; retain publication date and URL.",
        )
        results.append(result)
    return results


def parse_jtwc_atcf(
    text: str,
    *,
    source_url: str,
    checksum: str,
) -> list[Observation]:
    """Parse comma-separated ATCF B-deck BEST records."""

    observations: list[Observation] = []
    for fields in csv.reader(StringIO(text)):
        if len(fields) < 10 or fields[3].strip().upper() != "BEST":
            continue
        basin = fields[0].strip().upper()
        number = fields[1].strip().zfill(2)
        try:
            timestamp = datetime.strptime(fields[2].strip(), "%Y%m%d%H").replace(
                tzinfo=timezone.utc
            )
            latitude = _atcf_coordinate(fields[6])
            longitude = _atcf_coordinate(fields[7])
            wind = _float_or_none(fields[8])
            pressure = _float_or_none(fields[9])
        except ValueError:
            continue
        source_id = f"{basin}{number}{timestamp.year}"
        observations.append(
            Observation(
                source="jtwc",
                source_storm_id=source_id,
                storm_id=source_id,
                timestamp=timestamp,
                latitude=latitude,
                longitude=longitude,
                wind=wind,
                wind_unit="kt",
                pressure_hpa=pressure,
                intensity_code=fields[10].strip() if len(fields) > 10 else None,
                source_url=source_url,
                source_file_checksum=checksum,
                dataset_version="JTWC Best Track",
            )
        )
    return observations


def _atcf_coordinate(value: str) -> float:
    cleaned = value.strip().upper()
    if not cleaned or cleaned[-1] not in "NSEW":
        raise ValueError(f"invalid ATCF coordinate: {value}")
    scale = -1 if cleaned[-1] in "SW" else 1
    return scale * float(cleaned[:-1]) / 10


def _float_or_none(value: str) -> float | None:
    number = float(value.strip())
    return number if number > 0 else None
