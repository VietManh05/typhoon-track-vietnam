"""Generate deterministic functional evidence for Phase 3.

The outputs use synthetic data and validate contracts only. They are not
meteorological skill or production promotion evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from typhoon_vn.datasets.synthetic import generate_synthetic_catalogue
from typhoon_vn.datasets.typhoon_dataset import DatasetConfig
from typhoon_vn.evaluation.backtest import backtest_catalogue
from typhoon_vn.evaluation.reporting import (
    build_case_report,
    save_evaluation_report,
    save_track_error_plot,
)
from typhoon_vn.models.baselines import PersistenceForecaster
from typhoon_vn.models.uncertainty import CalibratedCone, quantile_calibration_report
from typhoon_vn.training.validation import (
    run_sequence_length_ablation,
    save_ablation_report,
)

HORIZON_STEPS = (1, 2, 4, 8, 12)
HORIZON_HOURS = (6, 12, 24, 48, 72)


def main(output_dir: str | Path = "reports/evaluation") -> dict[str, Path]:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    frame = generate_synthetic_catalogue(n_storms=6, n_fixes=24, seed=42)
    model = PersistenceForecaster(
        len(HORIZON_STEPS), 7, horizon_steps=list(HORIZON_STEPS)
    )
    details = {}
    summaries = {}
    for length in (4, 6, 8):
        detail, summary = backtest_catalogue(
            model,
            frame,
            config=DatasetConfig(input_len=length, horizon=HORIZON_STEPS),
        )
        detail = detail.copy()
        detail["sample_id"] = (
            detail["storm_id"].astype(str)
            + "|"
            + detail["issue_time"].astype(str)
            + "|"
            + detail["horizon_h"].astype(str)
        )
        details[length] = detail
        summaries[length] = summary

    def evaluate(length: int, common_ids: tuple[str, ...] | None) -> dict:
        detail = details[length]
        if common_ids is not None:
            detail = detail[detail["sample_id"].isin(common_ids)]
        return {
            "sample_ids": sorted(detail["sample_id"].tolist()),
            "mean_error_km": float(detail["track_error_km"].mean()),
            "median_error_km": float(detail["track_error_km"].median()),
        }

    ablation = run_sequence_length_ablation(
        (4, 6, 8),
        evaluate,
        seed=42,
        split_id="synthetic-functional-v1",
        budget="persistence-no-training",
    )
    ablation_path = save_ablation_report(
        destination / "sequence-length-ablation.json", ablation
    )

    detail = details[4]
    summary = summaries[4]
    report_path = save_evaluation_report(
        destination / "persistence-backtest.json",
        summary=summary,
        cases=build_case_report(detail),
        metadata={
            "model_version": "persistence-v1",
            "dataset_version": "synthetic-functional-v1",
            "split_policy": "synthetic contract only; not final-test skill evidence",
            "run_id": "phase3-functional-seed-42",
            "checkpoint_sha256": "not-applicable-classical-baseline",
        },
    )
    plot_path = save_track_error_plot(
        destination / "persistence-track-error.svg", summary
    )

    matrix = (
        detail.pivot_table(
            index=["storm_id", "issue_time"],
            columns="horizon_h",
            values="track_error_km",
        )
        .dropna()
        .loc[:, list(HORIZON_HOURS)]
        .to_numpy()
    )
    cone_path = CalibratedCone.fit(matrix, HORIZON_HOURS, coverage=0.9).save(
        destination / "calibrated-cone-synthetic.json"
    )

    targets = np.zeros((8, len(HORIZON_HOURS), 2))
    predictions = np.stack((targets - 1.0, targets, targets + 1.0), axis=-1)
    quantile_path = destination / "quantile-calibration-synthetic.json"
    quantile_path.write_text(
        json.dumps(
            {
                "scope": "synthetic functional calibration; not operational coverage",
                **quantile_calibration_report(
                    predictions, targets, quantiles=(0.1, 0.5, 0.9)
                ),
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return {
        "ablation": ablation_path,
        "backtest": report_path,
        "plot": plot_path,
        "cone": cone_path,
        "quantiles": quantile_path,
    }


if __name__ == "__main__":
    print(
        json.dumps(
            {name: str(path) for name, path in main().items()},
            indent=2,
            sort_keys=True,
        )
    )
