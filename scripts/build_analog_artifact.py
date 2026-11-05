"""Build the k-NN analog library served by the API (``ANALOG_ARTIFACT``).

Uses the train + validation storms of the year split (default 1980-2020), so
the 2021-2024 test storms used for evaluation and replays are never in the
library. Hyper-parameters default to the validation-selected values from
``run_model_comparison.py`` (k=40, position 1.0, season 0.5).

Usage::

    python scripts/build_analog_artifact.py --data-root data \
        --output artifacts/analog/analog-wp.npz
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from typhoon_vn.datasets.ibtracs import load_ibtracs_tracks
from typhoon_vn.datasets.typhoon_dataset import DatasetConfig, split_by_storm_or_year
from typhoon_vn.evaluation.comparison import build_windows
from typhoon_vn.features.build import FEATURE_COLUMNS
from typhoon_vn.inference.analog import save_analog_artifact

HORIZON_STEPS = (1, 2, 4, 8, 12)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--years", type=int, nargs=2, default=(1980, 2024))
    parser.add_argument("--k", type=int, default=40)
    parser.add_argument("--position-weight", type=float, default=1.0)
    parser.add_argument("--season-weight", type=float, default=0.5)
    args = parser.parse_args(argv)

    raw, cleaned, _ = load_ibtracs_tracks(args.data_root, tuple(args.years))
    train, val, test = split_by_storm_or_year(
        cleaned, val_ratio=0.1, test_ratio=0.1, by_year=True
    )
    library = pd.concat([train, val], ignore_index=True)
    config = DatasetConfig(
        input_len=4, horizon=HORIZON_STEPS, feature_cols=tuple(FEATURE_COLUMNS)
    )
    windows = build_windows(library, config)
    names = (
        raw.dropna(subset=["storm_name"])
        .drop_duplicates("storm_id")
        .set_index("storm_id")["storm_name"]
        .astype(str)
    )
    last_year = int(library.groupby("storm_id")["timestamp"].max().dt.year.max())
    path = save_analog_artifact(
        args.output,
        x_raw=windows.x_raw,
        y=windows.y,
        storm_ids=windows.storm_ids,
        storm_names=[names.get(s, s) for s in windows.storm_ids],
        issue_times=[pd.Timestamp(t).isoformat() for t in windows.issue_times],
        k=args.k,
        weights={
            "track": 1.0,
            "position": args.position_weight,
            "season": args.season_weight,
        },
        horizons_hours=[6 * step for step in HORIZON_STEPS],
        dataset_version=f"IBTrACS WP {args.years[0]}-{last_year}",
    )
    print(
        f"wrote {path} ({len(windows)} windows, "
        f"{library.storm_id.nunique()} storms, test storms excluded: "
        f"{test.storm_id.nunique()})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
