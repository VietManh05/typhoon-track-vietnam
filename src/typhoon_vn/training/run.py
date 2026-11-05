"""End-to-end local training pipeline used by the CLI and integration tests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

from typhoon_vn.datasets.synthetic import generate_synthetic_catalogue
from typhoon_vn.datasets.typhoon_dataset import (
    DatasetConfig,
    TyphoonDataset,
    collate_fn,
    split_by_storm_or_year,
)
from typhoon_vn.evaluation.backtest import backtest_catalogue
from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.models.baselines import CLIPERForecaster, PersistenceForecaster
from typhoon_vn.models.lstm import LSTMTrackForecaster
from typhoon_vn.models.uncertainty import CalibratedCone
from typhoon_vn.training.config_loader import PipelineConfig, load_config
from typhoon_vn.training.experiment import ExperimentTracker
from typhoon_vn.training.losses import MultiHorizonLoss
from typhoon_vn.training.pipeline import export_bundle, load_bundle, position_stats
from typhoon_vn.training.reproducibility import seed_worker, set_global_determinism
from typhoon_vn.training.trainer import Trainer, TrainingConfig


def _frame_hash(frame: pd.DataFrame) -> str:
    stable = frame.sort_values(["storm_id", "timestamp"]).to_json(
        date_format="iso", orient="records"
    )
    return hashlib.sha256(stable.encode()).hexdigest()


def _ids(frame: pd.DataFrame) -> list[str]:
    return sorted(map(str, frame["storm_id"].unique()))


def run_training(
    config: PipelineConfig,
    *,
    output_dir: str | Path,
    frame: pd.DataFrame | None = None,
    dataset_version: str = "synthetic-smoke-v1",
) -> dict[str, Any]:
    """Train, export and reload one supported LSTM bundle."""

    set_global_determinism(config.experiment.seed)
    if frame is None:
        frame = generate_synthetic_catalogue(
            n_storms=8, n_fixes=20, seed=config.experiment.seed
        )
    train, val, test = split_by_storm_or_year(
        frame,
        val_ratio=config.dataset.val_ratio,
        test_ratio=config.dataset.test_ratio,
        by_year=config.dataset.split_by_year,
        random_seed=config.dataset.random_seed,
    )
    if train.empty or val.empty:
        raise ValueError("training and validation splits must be non-empty")
    split_manifest = {
        "seed": config.dataset.random_seed,
        "train": _ids(train),
        "val": _ids(val),
        "test": _ids(test),
        "dataset_sha256": _frame_hash(frame),
    }
    if set(split_manifest["train"]) & set(split_manifest["val"]):
        raise RuntimeError("split leakage detected")

    builder = FeatureBuilder()
    train_matrix = builder.feature_matrix(train)
    scaler = FeatureScaler(list(FEATURE_COLUMNS)).fit(train_matrix)
    dataset_config = DatasetConfig(
        input_len=config.dataset.input_len,
        horizon=tuple(config.dataset.horizon),
        feature_cols=tuple(FEATURE_COLUMNS),
    )
    train_ds = TyphoonDataset(train, dataset_config, scaler=scaler)
    val_ds = TyphoonDataset(val, dataset_config, scaler=scaler)
    if not train_ds or not val_ds:
        raise ValueError("splits do not contain enough regular windows")
    generator = torch.Generator().manual_seed(config.experiment.seed)
    train_loader = DataLoader(
        train_ds,
        batch_size=config.training.batch_size,
        shuffle=True,
        generator=generator,
        collate_fn=collate_fn,
        worker_init_fn=seed_worker,
    )
    val_loader = DataLoader(
        val_ds, batch_size=config.training.batch_size, collate_fn=collate_fn
    )
    model_config = {
        "n_features": len(FEATURE_COLUMNS),
        "n_horizons": len(config.dataset.horizon),
        "n_classes": train_ds.n_classes,
        "hidden_size": config.model.hidden_size,
        "num_layers": config.model.num_layers,
        "dropout": config.model.dropout,
        # Predict displacement from the last fix (physical degrees).
        **position_stats(scaler),
    }
    model = LSTMTrackForecaster(**model_config)
    loss = MultiHorizonLoss(
        len(config.dataset.horizon),
        train_ds.n_classes,
        reg_loss=config.loss.reg_loss,
        horizon_weights=config.loss.horizon_weights,
        reg_weight=config.loss.reg_weight,
        cls_weight=config.loss.cls_weight,
    )
    output_dir = Path(output_dir)
    trainer = Trainer(
        model,
        TrainingConfig(
            epochs=config.training.epochs,
            batch_size=config.training.batch_size,
            learning_rate=config.training.learning_rate,
            weight_decay=config.training.weight_decay,
            patience=config.training.patience,
            gradient_clip=config.training.gradient_clip,
            scheduler=config.training.scheduler,
            device=config.experiment.device,
            checkpoint_dir=output_dir / "checkpoints",
            log_every=config.training.log_every,
        ),
        loss,
    )
    result = trainer.fit(train_loader, val_loader)
    # Export/evaluate the best-validation weights, not the (possibly overfit) last.
    best_path = output_dir / "checkpoints" / "best.pt"
    if best_path.exists():
        # Written by this trainer moments ago (holds RNG state, so not weights-only).
        best = torch.load(best_path, map_location="cpu", weights_only=False)
        model.load_state_dict(best["model_state_dict"])
    horizons_hours = [
        step * dataset_config.time_step_hours for step in config.dataset.horizon
    ]
    coverage = config.uncertainty.coverage
    val_errors = _error_matrix(model, val, dataset_config, scaler)
    cone = None
    if val_errors is not None and len(val_errors) >= 2:
        cone = CalibratedCone.fit(val_errors, horizons_hours, coverage=coverage)
        radii = {str(h): r for h, r in zip(horizons_hours, cone.radii_km)}
        uncertainty_method = (
            f"Empirical {coverage:.0%} quantile of validation-split track error "
            f"({len(val_errors)} forecasts, {val['storm_id'].nunique()} storms); "
            "same split as early stopping, errors within a storm are correlated"
        )
    else:
        radii = {str(hour): max(30.0, hour * 5.0) for hour in horizons_hours}
        uncertainty_method = (
            "Illustrative radius 5 km/hour (minimum 30 km); too few validation "
            "forecasts to calibrate"
        )
    manifest = export_bundle(
        output_dir / "bundle",
        model,
        scaler,
        version=config.experiment.name,
        dataset_version=dataset_version,
        dataset_sha256=split_manifest["dataset_sha256"],
        model_config=model_config,
        input_len=config.dataset.input_len,
        horizons_hours=horizons_hours,
        validation_radius_km=radii,
        split_manifest=split_manifest,
        synthetic=dataset_version.startswith("synthetic"),
        uncertainty_method=uncertainty_method,
    )
    load_bundle(manifest)
    evaluation = _evaluate_test_split(
        model, test, dataset_config, scaler, n_classes=train_ds.n_classes
    )
    if evaluation is not None and cone is not None:
        test_errors = _error_matrix(model, test, dataset_config, scaler)
        evaluation["cone"] = {
            "coverage_target": coverage,
            "calibration_split": "val",
            "radius_km": radii,
            "test_coverage": {
                str(h): v for h, v in cone.coverage_report(test_errors).items()
            },
        }
    if evaluation is not None:
        (output_dir / "evaluation.json").write_text(
            json.dumps(evaluation, indent=2), encoding="utf-8"
        )
    tracker = ExperimentTracker(
        output_dir,
        name=config.experiment.name,
        enabled=config.mlflow.enabled,
        tracking_uri=config.mlflow.tracking_uri,
        experiment_name=config.mlflow.experiment_name,
    )
    with tracker:
        tracker.log_params(config.model_dump(mode="json"))
        tracker.log_params(
            {
                "dataset_version": dataset_version,
                "dataset_sha256": split_manifest["dataset_sha256"],
            }
        )
        for record in result["history"]:
            epoch = int(record["epoch"])
            tracker.log_metrics(
                {key: value for key, value in record.items() if key != "epoch"},
                step=epoch,
            )
        tracker.log_artifact(manifest)
        tracker.log_artifact(manifest.parent / "split-manifest.json")
        if evaluation is not None:
            for name, rows in evaluation["models"].items():
                tracker.log_metrics(
                    {
                        f"test_{name}_err_km_{row['horizon_h']}h": row["mean_error_km"]
                        for row in rows
                    }
                )
            tracker.log_artifact(output_dir / "evaluation.json")
    result_payload = {
        "history": result["history"],
        "manifest": str(manifest),
        "run_id": tracker.run_id,
        "evaluation": evaluation,
    }
    (output_dir / "result.json").write_text(
        json.dumps(result_payload, indent=2), encoding="utf-8"
    )
    return {
        "manifest": manifest,
        "history": result["history"],
        "split": split_manifest,
        "run_id": tracker.run_id,
        "best_epoch": result["best_epoch"],
        "evaluation": evaluation,
    }


_SUMMARY_FIELDS = (
    "horizon_h",
    "mean_error_km",
    "median_error_km",
    "rmse_km",
    "p90_km",
    "mean_along_track_error_km",
    "mean_cross_track_error_km",
    "n_forecasts",
)


def _error_matrix(
    model: torch.nn.Module,
    frame: pd.DataFrame,
    dataset_config: DatasetConfig,
    scaler: FeatureScaler,
) -> np.ndarray | None:
    """Track errors (km) shaped ``(forecasts, horizons)`` for one split."""

    if frame.empty:
        return None
    detail, _ = backtest_catalogue(model, frame, config=dataset_config, scaler=scaler)
    if detail.empty:
        return None
    table = detail.pivot_table(
        index=["storm_id", "issue_time"],
        columns="horizon_h",
        values="track_error_km",
    ).sort_index(axis=1)
    return table.dropna().to_numpy(dtype=float)


def _evaluate_test_split(
    model: torch.nn.Module,
    test: pd.DataFrame,
    dataset_config: DatasetConfig,
    scaler: FeatureScaler,
    *,
    n_classes: int,
) -> dict[str, Any] | None:
    """Score the trained model and motion baselines on the held-out test storms.

    The LSTM sees train-fitted scaled features; the baselines need raw lat/lon
    in the first two feature columns, so they run without the scaler.
    """

    if test.empty:
        return None
    steps = list(dataset_config.horizon)
    candidates = {
        "lstm": (model, scaler),
        "persistence": (
            PersistenceForecaster(len(steps), n_classes, horizon_steps=steps),
            None,
        ),
        "cliper": (
            CLIPERForecaster(len(steps), n_classes, horizon_steps=steps),
            None,
        ),
    }
    models: dict[str, list[dict[str, Any]]] = {}
    for name, (candidate, candidate_scaler) in candidates.items():
        _, summary = backtest_catalogue(
            candidate, test, config=dataset_config, scaler=candidate_scaler
        )
        if summary.empty:
            return None
        models[name] = [
            {field: row[field] for field in _SUMMARY_FIELDS}
            for row in json.loads(summary.to_json(orient="records"))
        ]
    return {
        "split": "test",
        "n_storms": int(test["storm_id"].nunique()),
        "models": models,
    }


def run_training_file(
    config_path: str | Path, output_dir: str | Path
) -> dict[str, Any]:
    return run_training(load_config(config_path), output_dir=output_dir)
