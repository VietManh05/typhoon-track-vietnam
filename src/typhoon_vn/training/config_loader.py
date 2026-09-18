"""Strict configuration loader for the supported LSTM training pipeline."""

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ExperimentConfig(StrictModel):
    name: str = Field(min_length=1)
    seed: int = 42
    device: str = "cpu"


class DataConfig(StrictModel):
    input_len: int = Field(default=4, ge=2)
    horizon: list[int] = Field(default_factory=lambda: [1, 2, 4, 8, 12], min_length=1)
    split_by_year: bool = False
    val_ratio: float = Field(default=0.1, ge=0, lt=1)
    test_ratio: float = Field(default=0.1, ge=0, lt=1)
    random_seed: int = 42


class ModelConfig(StrictModel):
    type: Literal["LSTMTrackForecaster"]
    hidden_size: int = Field(default=128, ge=1)
    num_layers: int = Field(default=2, ge=1)
    dropout: float = Field(default=0.2, ge=0, lt=1)
    teacher_forcing_ratio: float | None = None
    d_model: int | None = None
    nhead: int | None = None
    n_layers: int | None = None
    dim_feedforward: int | None = None


class TrainConfig(StrictModel):
    epochs: int = Field(default=100, ge=1)
    batch_size: int = Field(default=32, ge=1)
    learning_rate: float = Field(default=1e-3, gt=0)
    weight_decay: float = Field(default=1e-5, ge=0)
    patience: int = Field(default=10, ge=1)
    gradient_clip: float = Field(default=1.0, ge=0)
    scheduler: Literal["cosine", "plateau", "none"] = "cosine"
    log_every: int = Field(default=10, ge=1)


class LossConfig(StrictModel):
    reg_loss: Literal["smooth_l1", "haversine"] = "smooth_l1"
    reg_weight: float = Field(default=1.0, ge=0)
    cls_weight: float = Field(default=0.3, ge=0)
    horizon_weights: list[float] | None = None


class CheckpointConfig(StrictModel):
    dir: str = "checkpoints/model"
    save_last: bool = True
    save_best: bool = True


class MlflowConfig(StrictModel):
    enabled: bool = False
    tracking_uri: str = "mlruns"
    experiment_name: str = "typhoon_vn"


class PipelineConfig(StrictModel):
    experiment: ExperimentConfig
    dataset: DataConfig
    model: ModelConfig
    training: TrainConfig
    loss: LossConfig
    checkpoint: CheckpointConfig
    mlflow: MlflowConfig


def load_config(path: str | Path) -> PipelineConfig:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    config = PipelineConfig.model_validate(payload)
    if config.dataset.val_ratio + config.dataset.test_ratio >= 1:
        raise ValueError("validation and test ratios must sum to less than 1")
    if sorted(set(config.dataset.horizon)) != config.dataset.horizon or any(
        horizon <= 0 for horizon in config.dataset.horizon
    ):
        raise ValueError("dataset horizons must be unique, increasing and positive")
    if config.mlflow.enabled:
        raise ValueError("MLflow export is not implemented by the local pipeline")
    return config
