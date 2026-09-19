"""Experiment, tuning, registry, and validation contracts."""

import json
from pathlib import Path

import pandas as pd
import pytest

from typhoon_vn.features.build import FEATURE_COLUMNS
from typhoon_vn.training.cross_validation import build_seasonal_folds
from typhoon_vn.training.experiment import ExperimentTracker
from typhoon_vn.training.registry import ModelRegistry, PromotionPolicy
from typhoon_vn.training.tuning import SearchSpace, run_search


def _season_frame() -> pd.DataFrame:
    rows = []
    for storm_id, start in (("A", "2023-12-30"), ("B", "2024-02-01"), ("C", "2025-03-01")):
        for index, timestamp in enumerate(pd.date_range(start, periods=4, freq="6h", tz="UTC")):
            row = {"storm_id": storm_id, "timestamp": timestamp, "lat": 10 + index, "lon": 110 + index}
            for feature_index, name in enumerate(FEATURE_COLUMNS):
                row[name] = float(feature_index + index)
            rows.append(row)
    return pd.DataFrame(rows)


def test_seasonal_folds_keep_storms_whole_and_fit_distinct_scalers() -> None:
    folds = build_seasonal_folds(_season_frame())
    assert [fold.season for fold in folds] == [2023, 2024, 2025]
    assert all(not (set(fold.train_ids) & set(fold.validation_ids)) for fold in folds)
    assert len({fold.scaler_fingerprint for fold in folds}) == len(folds)


def test_local_experiment_always_has_traceable_run_id_and_index(tmp_path) -> None:
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("ok", encoding="utf-8")
    with ExperimentTracker(tmp_path, name="smoke") as tracker:
        tracker.log_params({"dataset": {"version": "v1"}})
        tracker.log_metrics({"loss": 1.0}, step=1)
        tracker.log_artifact(artifact)
    record = json.loads((tmp_path / "experiment.json").read_text(encoding="utf-8"))
    assert record["run_id"] == tracker.run_id
    assert record["run_id"].startswith("local-")
    assert (tmp_path / "experiment-index.csv").is_file()


def test_search_uses_validation_only_and_seals_test_until_selection() -> None:
    seen = []

    def objective(params, fold):
        seen.append((params, fold))
        return params["hidden_size"] / 100 + fold

    result = run_search(
        SearchSpace(hidden_size=(8, 16), num_layers=(1,), dropout=(0.0,), learning_rate=(0.001,), batch_size=(8,), sequence_length=(4, 6, 8), horizon_weights=((1.0, 1.0),)),
        folds=(0, 1),
        objective=objective,
        n_trials=3,
        seed=7,
    )
    assert result.best_params["sequence_length"] in {4, 6, 8}
    assert result.test_evaluations == 0
    result.record_final_test({"mean_error_km": 10.0})
    with pytest.raises(RuntimeError, match="exactly once"):
        result.record_final_test({"mean_error_km": 9.0})


def _bundle(directory: Path, text: str = "bundle") -> Path:
    directory.mkdir(parents=True)
    manifest = directory / "manifest.json"
    manifest.write_text(text, encoding="utf-8")
    return manifest


def test_registry_promotion_gate_and_rollback(tmp_path) -> None:
    registry = ModelRegistry(tmp_path / "registry")
    first = registry.register(_bundle(tmp_path / "b1", "one"), version="v1", metadata={"dataset_version": "d1"})
    second = registry.register(_bundle(tmp_path / "b2", "two"), version="v2", metadata={"dataset_version": "d1"})
    policy = PromotionPolicy(max_mean_error_km=100.0, min_calibration_coverage=0.8)
    registry.promote(first.version, "staging", metrics={"mean_error_km": 80.0, "calibration_coverage": 0.9}, policy=policy)
    registry.promote(first.version, "production", metrics={"mean_error_km": 80.0, "calibration_coverage": 0.9}, policy=policy)
    with pytest.raises(ValueError, match="promotion gate"):
        registry.promote(second.version, "production", metrics={"mean_error_km": 120.0, "calibration_coverage": 0.9}, policy=policy)
    registry.promote(second.version, "staging", metrics={"mean_error_km": 70.0, "calibration_coverage": 0.9}, policy=policy)
    registry.promote(second.version, "production", metrics={"mean_error_km": 70.0, "calibration_coverage": 0.9}, policy=policy)
    assert registry.rollback("production") == "v1"
