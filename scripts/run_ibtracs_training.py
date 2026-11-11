"""Run an isolated, reproducible training experiment on local IBTrACS partitions."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import pandas as pd

from typhoon_vn.features.bridge import to_canonical_frame
from typhoon_vn.features.cleaning import clean_tracks
from typhoon_vn.training.config_loader import load_config
from typhoon_vn.training.run import run_training


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--start-year", type=int, default=2015)
    parser.add_argument("--end-year", type=int, default=2024)
    args = parser.parse_args()
    train_from_ibtracs(
        config=args.config,
        data_root=args.data_root,
        output_dir=args.output_dir,
        start_year=args.start_year,
        end_year=args.end_year,
    )
    return 0


def train_from_ibtracs(
    *,
    config: Path,
    data_root: Path,
    output_dir: Path,
    start_year: int,
    end_year: int,
) -> dict[str, object]:
    """Create an isolated candidate from one verified IBTrACS snapshot."""
    if start_year > end_year:
        raise ValueError("start_year must not be later than end_year")
    if output_dir.exists():
        raise SystemExit(f"refusing to overwrite existing output: {output_dir}")
    cleaned, details = load_ibtracs_tracks(
        data_root=data_root, start_year=start_year, end_year=end_year
    )
    source_sha256 = str(details["source_sha256"])
    started = time.perf_counter()
    dataset_version = (
        f"IBTrACS-v04r01-WP-{start_year}-{end_year}-sha256:{source_sha256}"
    )
    result = run_training(
        load_config(config),
        output_dir=output_dir,
        frame=cleaned,
        dataset_version=dataset_version,
    )
    summary = {
        **details,
        "elapsed_seconds": time.perf_counter() - started,
        "split_storms": {
            key: len(result["split"][key]) for key in ("train", "val", "test")
        },
        "history": result["history"],
        "manifest": str(result["manifest"]),
    }
    summary_path = output_dir / "training-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary))
    return summary


def load_ibtracs_tracks(
    *, data_root: Path, start_year: int, end_year: int
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Load only the selected years from the exact current CSV snapshot."""
    source = data_root / "raw/downloads/ibtracs/ibtracs-wp.csv"
    if not source.is_file():
        raise SystemExit(f"IBTrACS source is missing: {source}")
    source_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
    partition_root = data_root / "raw/observations/source=ibtracs"
    files = [
        path
        for year in range(start_year, end_year + 1)
        for path in sorted((partition_root / f"year={year}").glob("part-*.parquet"))
    ]
    if not files:
        raise FileNotFoundError(f"no IBTrACS partitions under {partition_root}")
    raw = pd.concat((pd.read_parquet(path) for path in files), ignore_index=True)
    raw = raw[
        (raw["source"] == "ibtracs")
        & (raw["source_file_checksum"] == source_sha256)
        & ~raw["storm_id"].astype(str).str.contains("UNRESOLVED")
    ].copy()
    raw["timestamp"] = pd.to_datetime(raw["timestamp"], utc=True)
    raw = raw[raw["timestamp"].dt.year.between(start_year, end_year)]
    raw = raw[raw["timestamp"].dt.hour % 6 == 0].copy()
    raw = raw.drop_duplicates(["storm_id", "timestamp"], keep="last")
    if raw.empty:
        raise ValueError("no IBTrACS observations match the current source checksum")
    canonical = to_canonical_frame(raw)
    cleaned, quality = clean_tracks(canonical)
    details = {
        "source": str(source),
        "source_sha256": source_sha256,
        "selected_raw_rows": len(raw),
        "clean_rows": len(cleaned),
        "storms": int(cleaned["storm_id"].nunique()),
        "start": str(cleaned["timestamp"].min()),
        "end": str(cleaned["timestamp"].max()),
        "cleaning": quality.as_dict(),
    }
    return cleaned, details


if __name__ == "__main__":
    raise SystemExit(main())
