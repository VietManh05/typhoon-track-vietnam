"""Raw acquisition of Vietnam boundary and coastline source datasets."""

from __future__ import annotations

import os
from pathlib import Path

from typhoon_vn.ingestion.errors import DownloadError
from typhoon_vn.ingestion.http import HttpDownloader
from typhoon_vn.ingestion.lineage import write_download_lineage
from typhoon_vn.ingestion.models import DownloadResult

DEFAULT_GADM_VIETNAM_URL = (
    "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_VNM_1.json.zip"
)


def download_gadm_vietnam(
    *,
    data_root: Path,
    downloader: HttpDownloader | None = None,
) -> DownloadResult:
    """Download GADM Vietnam level-1 boundaries as a preserved raw archive."""

    url = os.getenv("GADM_VIETNAM_URL") or DEFAULT_GADM_VIETNAM_URL
    result = (downloader or HttpDownloader()).fetch(
        source="gadm",
        url=url,
        destination=data_root / "raw" / "geospatial" / "gadm" / "gadm_vnm_level1.zip",
    )
    write_download_lineage(
        result,
        data_root=data_root,
        dataset_version="GADM 4.1",
        parser="Raw boundary archive; CRS validation is a Phase 2 operation.",
        licence_note="GADM licence applies; review before redistribution.",
    )
    return result


def download_gshhg(
    *,
    data_root: Path,
    url: str | None = None,
    downloader: HttpDownloader | None = None,
) -> DownloadResult:
    """Download an operator-approved GSHHG release URL with provenance."""

    source_url = url or os.getenv("GSHHG_URL")
    if not source_url:
        raise DownloadError(
            "Set GSHHG_URL to an approved official GSHHG release before downloading."
        )
    result = (downloader or HttpDownloader()).fetch(
        source="gshhg",
        url=source_url,
        destination=data_root / "raw" / "geospatial" / "gshhg" / "gshhg-release.zip",
    )
    write_download_lineage(
        result,
        data_root=data_root,
        dataset_version="operator-specified GSHHG release",
        parser="Raw coastline archive; landfall processing is a Phase 2 operation.",
        licence_note="GSHHG source and licence recorded in the manifest.",
    )
    return result
