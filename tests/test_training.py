"""Tests for the training loop and evaluation metrics."""

import torch
from torch.utils.data import DataLoader

from typhoon_vn.datasets.synthetic import generate_synthetic_catalogue
from typhoon_vn.datasets.typhoon_dataset import (
    DatasetConfig,
    TyphoonDataset,
    collate_fn,
    split_by_storm_or_year,
)
from typhoon_vn.evaluation.metrics import intensity_accuracy, track_error_km
from typhoon_vn.models.lstm import LSTMTrackForecaster
from typhoon_vn.training.losses import MultiHorizonLoss
from typhoon_vn.training.trainer import Trainer, TrainingConfig


def test_haversine_loss_smaller_when_closer() -> None:
    from typhoon_vn.training.losses import HaversineLoss

    loss_fn = HaversineLoss()
    far = torch.tensor([[[12.0, 122.0], [13.0, 123.0]]])
    close = torch.tensor([[[10.1, 120.1], [11.1, 121.1]]])
    target = torch.tensor([[[10.0, 120.0], [11.0, 121.0]]])
    assert loss_fn(close, target) < loss_fn(far, target)


def test_multi_horizon_loss_runs() -> None:
    df = generate_synthetic_catalogue(n_storms=4, seed=20)
    config = DatasetConfig(input_len=4, horizon=(1, 2, 4))
    ds = TyphoonDataset(df, config=config)
    loader = DataLoader(ds, batch_size=4, collate_fn=collate_fn, shuffle=False)
    batch = next(iter(loader))
    model = LSTMTrackForecaster(
        n_features=ds.n_features,
        n_horizons=ds.n_horizons,
        n_classes=ds.n_classes,
        hidden_size=32,
        num_layers=1,
    )
    loss_fn = MultiHorizonLoss(n_horizons=ds.n_horizons, n_classes=ds.n_classes)
    out = model(batch["x"], batch["mask"])
    loss, metrics = loss_fn(out["reg"], out["cls"], batch["y_reg"], batch["y_cls"])
    assert loss.ndim == 0
    assert metrics["reg_loss"] >= 0
    assert metrics["cls_loss"] >= 0


def test_trainer_runs_one_epoch(tmp_path) -> None:
    df = generate_synthetic_catalogue(n_storms=6, seed=21)
    train_df, val_df, _ = split_by_storm_or_year(
        df, val_ratio=0.3, test_ratio=0.0, random_seed=8
    )
    config = DatasetConfig(input_len=4, horizon=(1, 2, 4))
    train_ds = TyphoonDataset(train_df, config=config)
    val_ds = TyphoonDataset(val_df, config=config)
    train_loader = DataLoader(
        train_ds, batch_size=4, collate_fn=collate_fn, shuffle=True
    )
    val_loader = DataLoader(val_ds, batch_size=4, collate_fn=collate_fn)

    model = LSTMTrackForecaster(
        n_features=train_ds.n_features,
        n_horizons=train_ds.n_horizons,
        n_classes=train_ds.n_classes,
        hidden_size=32,
        num_layers=1,
    )
    loss_fn = MultiHorizonLoss(
        n_horizons=train_ds.n_horizons, n_classes=train_ds.n_classes
    )
    trainer_config = TrainingConfig(
        epochs=2,
        batch_size=4,
        patience=5,
        log_every=1,
        device="cpu",
        checkpoint_dir=tmp_path / "checkpoints",
    )
    trainer = Trainer(model, trainer_config, loss_fn)
    result = trainer.fit(train_loader, val_loader)
    assert len(result["history"]) == 2
    assert result["best_epoch"] > 0


def test_track_error_km_shape() -> None:
    pred = torch.randn(8, 5, 2)
    actual = torch.randn(8, 5, 2)
    errors = track_error_km(pred, actual)
    assert errors.shape == (8, 5)
    assert (errors >= 0).all()


def test_intensity_accuracy_per_horizon() -> None:
    pred = torch.tensor([[0, 1, 2, 3, 4], [0, 1, 2, 3, 4]])
    target = torch.tensor([[0, 1, 2, 3, 4], [0, 1, 2, 3, 5]])
    acc = intensity_accuracy(pred, target)
    assert acc.shape == (5,)
    assert acc[0] == 1.0
    assert acc[-1] == 0.5
