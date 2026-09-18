"""Append-only lineage manifests for raw source objects."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from typhoon_vn.ingestion.models import DownloadResult


def write_download_lineage(
    result: DownloadResult,
    *,
    data_root: Path,
    dataset_version: str | None = None,
    parser: str | None = None,
    licence_note: str | None = None,
) -> Path:
    """Write one immutable JSON manifest next to the raw-data hierarchy."""

    manifest_dir = data_root / "raw" / "lineage" / result.source
    manifest_dir.mkdir(parents=True, exist_ok=True)
    timestamp = result.downloaded_at.strftime("%Y%m%dT%H%M%SZ")
    manifest = manifest_dir / f"{timestamp}-{result.sha256[:12]}.json"
    payload = {
        **result.to_dict(),
        "dataset_version": dataset_version,
        "parser": parser,
        "licence_note": licence_note,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    manifest.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return manifest


def read_download_lineage(path: Path) -> dict[str, object]:
    """Load a manifest without making its mutable raw file authoritative."""

    return json.loads(path.read_text(encoding="utf-8"))
