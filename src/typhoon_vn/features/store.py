"""Minimal versioned feature store (WBS 4.5 / 5.x).

Stores processed feature tables as Parquet partitions with a JSON manifest
(version, timestamp, feature list, row counts, provenance) and refuses to
serve a table whose schema drifted from the registered contract.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from typhoon_vn.features.build import FEATURE_COLUMNS


class SchemaDriftError(ValueError):
    """Raised when a stored feature table no longer matches the contract."""


def _manifest_path(store_dir: Path, version: str) -> Path:
    return store_dir / version / "manifest.json"


def save_feature_table(
    df: pd.DataFrame,
    store_dir: str | Path,
    version: str,
    provenance: dict | None = None,
) -> Path:
    """Persist ``df`` as ``<store_dir>/<version>/features.parquet`` + manifest."""

    store_dir = Path(store_dir)
    target = store_dir / version
    target.mkdir(parents=True, exist_ok=True)
    df.to_parquet(target / "features.parquet", index=False)
    manifest = {
        "version": version,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "n_rows": len(df),
        "n_storms": int(df["storm_id"].nunique()) if "storm_id" in df.columns else None,
        "feature_columns": list(FEATURE_COLUMNS),
        "provenance": provenance or {},
    }
    (target / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return target / "features.parquet"


def check_schema_drift(
    df: pd.DataFrame, expected: list[str] | None = None
) -> list[str]:
    """Return human-readable drift issues (empty list means no drift)."""

    expected_cols = list(expected or FEATURE_COLUMNS)
    issues: list[str] = []
    missing = [c for c in expected_cols if c not in df.columns]
    extra = [c for c in df.columns if c not in set(expected_cols)]
    if missing:
        issues.append(f"missing columns: {missing}")
    if extra:
        issues.append(f"unexpected columns: {extra}")
    return issues


def load_feature_table(
    store_dir: str | Path, version: str, strict: bool = True
) -> pd.DataFrame:
    """Load a versioned table, optionally enforcing the schema contract."""

    store_dir = Path(store_dir)
    manifest_file = _manifest_path(store_dir, version)
    if not manifest_file.exists():
        raise FileNotFoundError(f"No manifest for feature version {version!r}.")
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    df = pd.read_parquet(store_dir / version / "features.parquet")
    issues = check_schema_drift(df, manifest.get("feature_columns"))
    if issues and strict:
        raise SchemaDriftError("; ".join(issues))
    return df


def list_versions(store_dir: str | Path) -> list[str]:
    """List stored feature versions that contain a manifest."""

    store_dir = Path(store_dir)
    if not store_dir.exists():
        return []
    return sorted(
        p.name for p in store_dir.iterdir() if (p / "manifest.json").exists()
    )


__all__ = [
    "SchemaDriftError",
    "check_schema_drift",
    "list_versions",
    "load_feature_table",
    "save_feature_table",
]
