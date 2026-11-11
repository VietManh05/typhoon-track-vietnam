"""End-to-end functional backtest and reporting contracts."""

import json

from typhoon_vn.datasets.synthetic import generate_synthetic_catalogue
from typhoon_vn.datasets.typhoon_dataset import DatasetConfig
from typhoon_vn.evaluation.backtest import backtest_catalogue
from typhoon_vn.evaluation.reporting import (
    build_case_report,
    save_evaluation_report,
    save_track_error_plot,
)
from typhoon_vn.models.baselines import PersistenceForecaster


def test_persistence_backtest_covers_all_horizons_and_writes_reports(tmp_path) -> None:
    frame = generate_synthetic_catalogue(n_storms=4, n_fixes=20, seed=17)
    config = DatasetConfig(input_len=4, horizon=(1, 2, 4, 8, 12))
    model = PersistenceForecaster(5, 7, horizon_steps=[1, 2, 4, 8, 12])
    detail, summary = backtest_catalogue(model, frame, config=config)
    assert summary["horizon_h"].tolist() == [6, 12, 24, 48, 72]
    assert (summary["n_forecasts"] > 0).all()
    assert (summary["mean_error_km"] >= 0).all()
    cases = build_case_report(detail, top_n=2)
    report = save_evaluation_report(
        tmp_path / "evaluation.json",
        summary=summary,
        cases=cases,
        metadata={
            "model_version": "persistence-v1",
            "dataset_version": "synthetic-contract-v1",
            "split_policy": "functional fixture; not final-test skill evidence",
            "run_id": "test-run",
            "checkpoint_sha256": "not-applicable-classical-baseline",
        },
    )
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["cases"]["best_cases"]
    plot = save_track_error_plot(tmp_path / "track-error.svg", summary)
    assert plot.read_text(encoding="utf-8").startswith("<svg")
