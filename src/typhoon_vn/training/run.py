"""End-to-end local training pipeline used by the CLI and integration tests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

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
from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.models.base import TrackForecaster
from typhoon_vn.models.lstm import (
    AttentionLSTMTrackForecaster,
    LSTMTrackForecaster,
    Seq2SeqLSTMTrackForecaster,
)
from typhoon_vn.models.transformer import TransformerTrackForecaster
from typhoon_vn.training.config_loader import PipelineConfig, load_config
from typhoon_vn.training.experiment import ExperimentTracker
from typhoon_vn.training.losses import MultiHorizonLoss
from typhoon_vn.training.pipeline import export_bundle, load_bundle
from typhoon_vn.training.reproducibility import seed_worker, set_global_determinism
from typhoon_vn.training.trainer import Trainer, TrainingConfig


def _frame_hash(frame: pd.DataFrame) -> str:
    stable = frame.sort_values(["storm_id", "timestamp"]).to_json(
        date_format="iso", orient="records"
    )
    return hashlib.sha256(stable.encode()).hexdigest()


def _source_hash() -> str:
    digest = hashlib.sha256()
    source_root = Path(__file__).resolve().parents[1]
    for path in sorted(source_root.rglob("*.py")):
        digest.update(path.relative_to(source_root).as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _ids(frame: pd.DataFrame) -> list[str]:
    return sorted(map(str, frame["storm_id"].unique()))


def _build_model(
    config: PipelineConfig,
    *,
    n_features: int,
    n_horizons: int,
    n_classes: int,
    anchor: dict[str, list[float] | list[int]] | None = None,
) -> tuple[TrackForecaster, dict[str, Any]]:
    common = {
        "n_features": n_features,
        "n_horizons": n_horizons,
        "n_classes": n_classes,
    }
    if config.model.type == "LSTMTrackForecaster":
        constructor = {
            **common,
            "hidden_size": config.model.hidden_size,
            "num_layers": config.model.num_layers,
            "dropout": config.model.dropout,
            **(anchor or {}),
        }
        return LSTMTrackForecaster(**constructor), constructor
    if config.model.type == "Seq2SeqLSTMTrackForecaster":
        constructor = {
            **common,
            "hidden_size": config.model.hidden_size,
            "num_layers": config.model.num_layers,
            "dropout": config.model.dropout,
            "teacher_forcing_ratio": (
                0.5
                if config.model.teacher_forcing_ratio is None
                else config.model.teacher_forcing_ratio
            ),
        }
        return Seq2SeqLSTMTrackForecaster(**constructor), constructor
    if config.model.type == "AttentionLSTMTrackForecaster":
        constructor = {
            **common,
            "hidden_size": config.model.hidden_size,
            "num_layers": config.model.num_layers,
            "dropout": config.model.dropout,
        }
        return AttentionLSTMTrackForecaster(**constructor), constructor
    constructor = {
        **common,
        "d_model": config.model.d_model or 64,
        "nhead": config.model.nhead or 4,
        "n_layers": config.model.n_layers or 2,
        "dim_feedforward": config.model.dim_feedforward or 128,
        "dropout": config.model.dropout,
    }
    return TransformerTrackForecaster(**constructor), constructor


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
    model, model_config = _build_model(
        config,
        n_features=len(FEATURE_COLUMNS),
        n_horizons=len(config.dataset.horizon),
        n_classes=train_ds.n_classes,
        anchor=(
            {
                "anchor_indices": [
                    FEATURE_COLUMNS.index("lat"),
                    FEATURE_COLUMNS.index("lon"),
                ],
                "anchor_mean": [
                    float(scaler._scaler.mean_[FEATURE_COLUMNS.index(name)])
                    for name in ("lat", "lon")
                ],
                "anchor_scale": [
                    float(scaler._scaler.scale_[FEATURE_COLUMNS.index(name)])
                    for name in ("lat", "lon")
                ],
                "anchor_horizon_steps": list(config.dataset.horizon),
            }
            if config.model.type == "LSTMTrackForecaster"
            and not dataset_version.startswith("synthetic")
            else None
        ),
    )
    loss = MultiHorizonLoss(
        len(config.dataset.horizon),
        train_ds.n_classes,
        reg_loss=config.loss.reg_loss,
        horizon_weights=config.loss.horizon_weights,
        reg_weight=config.loss.reg_weight,
        cls_weight=config.loss.cls_weight,
    )
    output_dir = Path(output_dir)
    checkpoint_dir = output_dir / config.checkpoint.dir
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
            checkpoint_dir=checkpoint_dir,
            log_every=config.training.log_every,
        ),
        loss,
    )
    result = trainer.fit(train_loader, val_loader)
    # Export the selected validation checkpoint, without rewinding trainer/RNG state.
    best = torch.load(
        checkpoint_dir / "best.pt",
        map_location="cpu",
        weights_only=False,  # Trusted checkpoint just generated by this run.
    )
    model.load_state_dict(best["model_state_dict"])
    # Smoke artifact: radii are explicitly illustrative, not a real calibration claim.
    horizons_hours = [
        step * dataset_config.time_step_hours for step in config.dataset.horizon
    ]
    radii = {str(hour): max(30.0, hour * 5.0) for hour in horizons_hours}
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
        uncertainty_method="illustrative heuristic; not calibrated coverage",
    )
    load_bundle(manifest)
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
                "source_sha256": _source_hash(),
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
    result_payload = {
        "history": result["history"],
        "manifest": str(manifest),
        "run_id": tracker.run_id,
    }
    (output_dir / "result.json").write_text(
        json.dumps(result_payload, indent=2), encoding="utf-8"
    )
    return {
        "manifest": manifest,
        "history": result["history"],
        "split": split_manifest,
        "run_id": tracker.run_id,
    }


def run_training_file(
    config_path: str | Path, output_dir: str | Path
) -> dict[str, Any]:
    return run_training(load_config(config_path), output_dir=output_dir)
