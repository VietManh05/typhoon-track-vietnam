"""Measure an IBTrACS candidate on its held-out storms against persistence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from run_ibtracs_training import load_ibtracs_tracks

from typhoon_vn.datasets.typhoon_dataset import DatasetConfig
from typhoon_vn.evaluation.backtest import backtest_bundle, backtest_catalogue
from typhoon_vn.models.baselines import PersistenceForecaster
from typhoon_vn.training.pipeline import load_bundle


def evaluate_candidate(
    *, candidate: Path, data_root: Path, start_year: int, end_year: int
) -> dict[str, object]:
    summary = json.loads(
        (candidate / "training-summary.json").read_text(encoding="utf-8")
    )
    cleaned, details = load_ibtracs_tracks(
        data_root=data_root, start_year=start_year, end_year=end_year
    )
    if details["source_sha256"] != summary["source_sha256"]:
        raise ValueError("source checksum changed since candidate training")
    manifest_path = candidate / "bundle/manifest.json"
    bundle = load_bundle(manifest_path)
    manifest = bundle["manifest"]
    split = json.loads(
        (candidate / "bundle/split-manifest.json").read_text(encoding="utf-8")
    )
    test_ids = set(map(str, split["test"]))
    test = cleaned[cleaned["storm_id"].astype(str).isin(test_ids)]
    if test.empty:
        raise ValueError("candidate has no held-out test storms")

    _, model_metrics = backtest_bundle(bundle, test)
    step_hours = int(manifest["time_step_hours"])
    horizon_steps = [int(hour) // step_hours for hour in manifest["horizons_hours"]]
    config = DatasetConfig(
        input_len=int(manifest["input_len"]),
        horizon=tuple(horizon_steps),
        time_step_hours=step_hours,
        feature_cols=tuple(manifest["feature_columns"]),
    )
    persistence = PersistenceForecaster(
        n_horizons=len(horizon_steps),
        n_classes=7,
        horizon_steps=horizon_steps,
        time_step_hours=step_hours,
    )
    _, baseline_metrics = backtest_catalogue(persistence, test, config=config)
    if model_metrics.empty or baseline_metrics.empty:
        raise ValueError("held-out storms contain no complete forecast windows")
    model_rows = model_metrics.set_index("horizon_h")
    baseline_rows = baseline_metrics.set_index("horizon_h")
    if set(model_rows.index) != set(baseline_rows.index):
        raise ValueError("candidate and baseline horizons differ")
    horizons = []
    for hour in sorted(model_rows.index):
        model_row = model_rows.loc[hour]
        baseline_row = baseline_rows.loc[hour]
        if model_row["n_forecasts"] != baseline_row["n_forecasts"]:
            raise ValueError("candidate and baseline sample counts differ")
        horizons.append(
            {
                "horizon_h": int(hour),
                "n_forecasts": int(model_row["n_forecasts"]),
                "candidate_mean_error_km": float(model_row["mean_error_km"]),
                "persistence_mean_error_km": float(baseline_row["mean_error_km"]),
            }
        )
    beats_baseline = all(
        row["candidate_mean_error_km"] < row["persistence_mean_error_km"]
        for row in horizons
    )
    report: dict[str, object] = {
        "status": "research_candidate" if beats_baseline else "rejected_baseline",
        "source_sha256": details["source_sha256"],
        "test_storms": int(test["storm_id"].nunique()),
        "horizons": horizons,
        "beats_persistence_all_horizons": beats_baseline,
        "promoted": False,
    }
    (candidate / "heldout-evaluation.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--start-year", type=int, default=2015)
    parser.add_argument("--end-year", type=int, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            evaluate_candidate(
                candidate=args.candidate,
                data_root=args.data_root,
                start_year=args.start_year,
                end_year=args.end_year,
            )
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
