"""Run the Phase 2 cleaning + feature-engineering pipeline on real raw data.

Pipeline (read-only w.r.t. ``data/raw``):

1. Load every raw observation partition (IBTrACS, JMA, ...).
2. Map rows onto the canonical schema (knots -> m/s, JMA grades -> classes).
3. Merge duplicate fixes across sources (IBTrACS priority, conflicts kept).
4. Clean: validate -> dedupe -> sort -> interpolate -> flag.
5. Build motion/time/coast/intensity features.
6. Split by storm ID (train/val/test) and fit ``FeatureScaler`` on train only.
7. Persist feature/scaler/manifest artefacts under ``data/processed/phase2/``.

Usage (repo root)::

    $env:PYTHONPATH = "src"
    python scripts/run_phase2.py --limit-years 2000-2025
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow running the script before the package is installed.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import numpy as np
import pandas as pd

from typhoon_vn.datasets.typhoon_dataset import split_by_storm_or_year
from typhoon_vn.features import build as features
from typhoon_vn.features.bridge import load_raw_observations, to_canonical_frame
from typhoon_vn.features.cleaning import clean_tracks, quality_summary
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.features.schema import CleaningReport, TrackSchema
from typhoon_vn.ingestion.merge_sources import merge_observations
from typhoon_vn.ingestion.models import Observation


def _parse_year_range(value: str | None) -> tuple[int, int] | None:
    if not value:
        return None
    start, _, end = value.partition("-")
    return int(start), int(end)


def _row_to_observation(row: pd.Series) -> Observation:
    return Observation(
        source=str(row["source"]),
        source_storm_id=str(row["source_storm_id"]),
        storm_id=str(row["storm_id"]),
        timestamp=pd.Timestamp(row["timestamp"]).to_pydatetime(),
        latitude=float(row["latitude"]),
        longitude=float(row["longitude"]),
        source_url=str(row["source_url"]),
        source_file_checksum=str(row.get("source_file_checksum") or "raw-partition"),
        wind=float(row["wind"]) if pd.notna(row["wind"]) else None,
        wind_unit=str(row["wind_unit"]) if pd.notna(row["wind_unit"]) else None,
        pressure_hpa=(
            float(row["pressure_hpa"]) if pd.notna(row["pressure_hpa"]) else None
        ),
        storm_name=(str(row["storm_name"]) if pd.notna(row["storm_name"]) else None),
        intensity_code=(
            str(row["intensity_code"]) if pd.notna(row["intensity_code"]) else None
        ),
        dataset_version=(
            str(row["dataset_version"]) if pd.notna(row["dataset_version"]) else None
        ),
    )


def _merged_frame(merged: list[Observation]) -> pd.DataFrame:
    """Hand merged fixes back to the bridge as raw-shaped rows."""

    rows = []
    for obs in merged:
        rows.append(
            {
                "storm_id": obs.storm_id,
                "timestamp": obs.timestamp.isoformat(),
                "latitude": obs.latitude,
                "longitude": obs.longitude,
                # Keep the source-native magnitude+unit; the bridge converts
                # knots -> m/s and passes m/s (CMA) through unchanged.
                "wind": obs.wind,
                "wind_unit": obs.wind_unit or ("m/s" if obs.source == "cma" else "kt"),
                "pressure_hpa": obs.pressure_hpa,
                "intensity_code": obs.intensity_code,
                "source": obs.source,
            }
        )
    # CMA rows store m/s natively; keep their raw magnitude under "m/s".
    return pd.DataFrame(rows)


def _fast_merge(raw: pd.DataFrame) -> pd.DataFrame:
    """Reconcile cross-source duplicates storm by storm.

    Rows are grouped by storm ID before calling the authoritative
    :func:`merge_observations` reconciler, so the pairwise (O(n^2) per storm)
    identity/space check only ever compares fixes that could match. This keeps
    the multi-decade archive tractable without re-implementing the merge rules:
    the priority source, ``contributing_sources`` and ``source_conflicts`` are
    exactly those produced by :mod:`typhoon_vn.ingestion.merge_sources`.
    """

    merged: list[Observation] = []
    for _, group in raw.groupby("storm_id", sort=False):
        observations = [_row_to_observation(row) for _, row in group.iterrows()]
        merged.extend(merge_observations(observations))
    return _merged_frame(merged)


def run(
    data_root: Path,
    output_dir: Path,
    year_range: tuple[int, int] | None = None,
    seed: int = 42,
) -> dict:
    schema = TrackSchema()
    raw = load_raw_observations(data_root)
    if year_range:
        years = pd.to_datetime(raw["timestamp"], utc=True).dt.year
        raw = raw[(years >= year_range[0]) & (years <= year_range[1])].copy()
    print(
        f"Loaded {len(raw)} raw observations from "
        f"sources {sorted(raw['source'].unique())}"
    )

    # IBTrACS parquet holds repeated agency rows for the same fix; drop exact
    # duplicates before the conservative cross-source merge.
    raw = raw.drop_duplicates(
        subset=[
            "source",
            "storm_id",
            "timestamp",
            "latitude",
            "longitude",
            "wind",
            "pressure_hpa",
        ]
    )
    print(f"After exact-duplicate removal: {len(raw)} rows", flush=True)

    # Storm-at-a-time reconciliation: the authoritative pairwise Observation
    # merge (O(n^2) per storm) only ever compares fixes that could match, so the
    # multi-decade archive stays tractable without duplicating merge rules.
    print("Merging cross-source duplicates ...", flush=True)
    merged_rows = _fast_merge(raw)
    print(f"After cross-source merge: {len(merged_rows)} fixes", flush=True)

    canonical = to_canonical_frame(merged_rows, schema)
    cleaned, report = clean_tracks(canonical, schema, CleaningReport())
    print(
        f"Cleaned: {report.n_input} -> {report.n_output} rows "
        f"(coords dropped={report.n_dropped_invalid_coords}, "
        f"physics dropped={report.n_dropped_invalid_physics}, "
        f"dupes={report.n_duplicates_removed}, "
        f"interpolated={report.n_interpolated}, "
        f"suspicious={report.n_suspicious_flagged})"
    )
    print("Quality summary:", json.dumps(quality_summary(cleaned, schema)))

    builder = features.FeatureBuilder()
    featured = builder.transform(cleaned)
    assert not [c for c in builder.feature_columns if c not in featured.columns]
    matrix = featured[["storm_id", "timestamp", *builder.feature_columns]].copy()
    print(
        f"Feature table: {len(matrix)} rows x {len(builder.feature_columns)} "
        f"features, {matrix['storm_id'].nunique()} storms"
    )

    train_df, val_df, test_df = split_by_storm_or_year(
        featured, val_ratio=0.1, test_ratio=0.1, by_year=False, random_seed=seed
    )
    train_ids, val_ids = set(train_df["storm_id"]), set(val_df["storm_id"])
    assert not (train_ids & val_ids), "storm leakage into val"
    assert not (train_ids & set(test_df["storm_id"])), "storm leakage into test"

    scaler = FeatureScaler(feature_columns=builder.feature_columns)
    scaler.fit(builder.feature_matrix(train_df))
    # Compare in the *original* space over rows that round-trip losslessly:
    # NaN/±inf inputs are replaced by the train fill value on the way in, so
    # including them would make this self-check meaningless (max err = NaN).
    sample = builder.feature_matrix(train_df).head(50)
    sample_values = sample[builder.feature_columns].to_numpy(dtype=float)
    finite_rows = np.isfinite(sample_values).all(axis=1)
    roundtrip = scaler.inverse_transform(scaler.transform(sample.loc[finite_rows]))
    max_err = float(
        np.abs(
            roundtrip[builder.feature_columns].to_numpy() - sample_values[finite_rows]
        ).max()
    )
    assert math.isfinite(max_err), "scaler round-trip must be measurable"
    print(
        f"Scaler fitted on {len(train_df)} train rows; "
        f"round-trip max err={max_err:.2e} over {int(finite_rows.sum())} finite rows"
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    matrix.to_parquet(output_dir / "features.parquet", index=False)
    cleaned.to_parquet(output_dir / "cleaned.parquet", index=False)
    scaler_path = scaler.save(output_dir / "scaler.joblib")
    for name, split in (("train", train_df), ("val", val_df), ("test", test_df)):
        split[["storm_id"]].drop_duplicates().to_csv(
            output_dir / f"{name}_ids.csv", index=False
        )
    manifest = {
        "phase": 2,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "data_root": str(data_root),
        "year_range": list(year_range) if year_range else None,
        "n_raw": int(len(raw)),
        "n_merged": int(len(merged_rows)),
        "cleaning_report": report.as_dict(),
        "n_feature_rows": int(len(matrix)),
        "n_storms": int(matrix["storm_id"].nunique()),
        "feature_columns": builder.feature_columns,
        "splits": {
            "train_storms": int(train_df["storm_id"].nunique()),
            "val_storms": int(val_df["storm_id"].nunique()),
            "test_storms": int(test_df["storm_id"].nunique()),
        },
        "scaler_roundtrip_max_err": max_err,
        "artefacts": {
            "features": "features.parquet",
            "cleaned": "cleaned.parquet",
            "scaler": scaler_path.name,
        },
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Wrote artefacts to {output_dir}")
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Phase 2 on real raw data.")
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/phase2"))
    parser.add_argument(
        "--limit-years", default=None, help="e.g. 2000-2025 (default: all years)"
    )
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(argv)
    run(args.data_root, args.output, _parse_year_range(args.limit_years), args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
