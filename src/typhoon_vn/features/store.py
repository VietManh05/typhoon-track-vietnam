"""Minimal versioned feature store (WBS 4.5 / 5.x).

Stores processed feature tables as Parquet partitions with a JSON manifest
(version, timestamp, feature list, row counts, provenance) and refuses to
serve a table whose schema drifted from the registered contract.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from typhoon_vn.features.build import FEATURE_COLUMNS
from typhoon_vn.features.dictionary import (
    FEATURE_SCHEMA_VERSION,
    feature_dictionary,
    feature_schema_fingerprint,
)


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
    parquet_path = target / "features.parquet"
    parquet_tmp = target / ".features.parquet.tmp"
    df.to_parquet(parquet_tmp, index=False)
    os.replace(parquet_tmp, parquet_path)
    manifest = {
        "version": version,
        "feature_schema_version": FEATURE_SCHEMA_VERSION,
        "feature_schema_fingerprint": feature_schema_fingerprint(),
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "n_rows": len(df),
        "n_storms": int(df["storm_id"].nunique()) if "storm_id" in df.columns else None,
        "feature_columns": list(FEATURE_COLUMNS),
        "columns": [
            {"name": name, "dtype": str(dtype)}
            for name, dtype in zip(df.columns, df.dtypes)
        ],
        "feature_dictionary": [asdict(item) for item in feature_dictionary()],
        "provenance": provenance or {},
    }
    manifest_path = target / "manifest.json"
    manifest_tmp = target / ".manifest.json.tmp"
    manifest_tmp.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    os.replace(manifest_tmp, manifest_path)
    return parquet_path


def check_schema_drift(
    df: pd.DataFrame,
    expected: list[str] | None = None,
    expected_columns: list[dict[str, str]] | None = None,
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
    if not missing and not extra and list(df.columns) != expected_cols:
        issues.append(
            f"column order changed: expected {expected_cols}, "
            f"received {list(df.columns)}"
        )
    if expected_columns:
        expected_order = [item["name"] for item in expected_columns]
        actual_order = list(df.columns)
        if actual_order != expected_order and not any(
            issue.startswith("column order changed") for issue in issues
        ):
            issues.append(
                f"column order changed: expected {expected_order}, received {actual_order}"
            )
        expected_dtypes = {item["name"]: item["dtype"] for item in expected_columns}
        changed = {
            name: (expected_dtypes[name], str(df[name].dtype))
            for name in actual_order
            if name in expected_dtypes and expected_dtypes[name] != str(df[name].dtype)
        }
        if changed:
            issues.append(f"dtype changes: {changed}")
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
    issues = check_schema_drift(
        df,
        manifest.get("feature_columns"),
        manifest.get("columns"),
    )
    if manifest.get("feature_schema_fingerprint") != feature_schema_fingerprint():
        issues.append("registered feature schema fingerprint changed")
    if issues and strict:
        raise SchemaDriftError("; ".join(issues))
    return df


def list_versions(store_dir: str | Path) -> list[str]:
    """List stored feature versions that contain a manifest."""

    store_dir = Path(store_dir)
    if not store_dir.exists():
        return []
    return sorted(p.name for p in store_dir.iterdir() if (p / "manifest.json").exists())


__all__ = [
    "SchemaDriftError",
    "check_schema_drift",
    "list_versions",
    "load_feature_table",
    "save_feature_table",
]
