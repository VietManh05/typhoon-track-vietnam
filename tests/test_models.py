"""Tests for Phase-3 model architectures and uncertainty helpers."""

import numpy as np
import pytest
import torch

from typhoon_vn.datasets.synthetic import generate_synthetic_catalogue
from typhoon_vn.datasets.typhoon_dataset import DatasetConfig, TyphoonDataset
from typhoon_vn.models.lstm import (
    AttentionLSTMTrackForecaster,
    LSTMTrackForecaster,
    Seq2SeqLSTMTrackForecaster,
)
from typhoon_vn.models.uncertainty import (
    DeepEnsemble,
    QuantileTrackForecaster,
    build_cone,
    cone_radius_km,
    mc_dropout_predict,
    quantile_loss,
)


@pytest.fixture
def sample_batch() -> dict[str, torch.Tensor]:
    df = generate_synthetic_catalogue(n_storms=4, seed=10)
    config = DatasetConfig(input_len=4, horizon=(1, 2, 4, 8, 12))
    ds = TyphoonDataset(df, config=config)
    x = torch.from_numpy(ds[0]["x"]).unsqueeze(0)
    mask = torch.from_numpy(ds[0]["mask"]).unsqueeze(0)
    return {"x": x, "mask": mask}


def test_baseline_lstm_forward_shape(sample_batch: dict[str, torch.Tensor]) -> None:
    x, mask = sample_batch["x"], sample_batch["mask"]
    n_features = x.size(-1)
    model = LSTMTrackForecaster(
        n_features=n_features, n_horizons=5, n_classes=7, hidden_size=32, num_layers=1
    )
    out = model(x, mask)
    assert out["reg"].shape == (1, 5, 2)
    assert out["cls"].shape == (1, 5, 7)


def test_seq2seq_lstm_forward_shape(sample_batch: dict[str, torch.Tensor]) -> None:
    x, mask = sample_batch["x"], sample_batch["mask"]
    n_features = x.size(-1)
    model = Seq2SeqLSTMTrackForecaster(
        n_features=n_features, n_horizons=5, n_classes=7, hidden_size=32, num_layers=1
    )
    out = model(x, mask)
    assert out["reg"].shape == (1, 5, 2)
    assert out["cls"].shape == (1, 5, 7)


def test_attention_lstm_returns_attention(sample_batch: dict[str, torch.Tensor]) -> None:
    x, mask = sample_batch["x"], sample_batch["mask"]
    n_features = x.size(-1)
    model = AttentionLSTMTrackForecaster(
        n_features=n_features, n_horizons=5, n_classes=7, hidden_size=32, num_layers=1
    )
    out = model(x, mask)
    assert "attn" in out
    assert out["attn"].shape == (1, x.size(1))


def test_mc_dropout_produces_uncertainty(sample_batch: dict[str, torch.Tensor]) -> None:
    x, mask = sample_batch["x"], sample_batch["mask"]
    n_features = x.size(-1)
    model = LSTMTrackForecaster(
        n_features=n_features, n_horizons=5, n_classes=7, hidden_size=32, num_layers=1, dropout=0.3
    )
    result = mc_dropout_predict(model, x, mask, n_samples=10)
    assert result["reg_mean"].shape == (1, 5, 2)
    assert result["reg_std"].shape == (1, 5, 2)
    assert (result["reg_std"] >= 0).all()


def test_quantile_wrapper_shape(sample_batch: dict[str, torch.Tensor]) -> None:
    x, mask = sample_batch["x"], sample_batch["mask"]
    n_features = x.size(-1)
    base = LSTMTrackForecaster(
        n_features=n_features, n_horizons=5, n_classes=7, hidden_size=32, num_layers=1
    )
    model = QuantileTrackForecaster(base, quantiles=(0.1, 0.5, 0.9))
    out = model(x, mask)
    assert out["reg"].shape == (1, 5, 2, 3)


def test_quantile_loss_decreases_with_better_prediction() -> None:
    pred = torch.zeros(2, 5, 2, 3)
    target = torch.ones(2, 5, 2)
    loss = quantile_loss(pred, target, quantiles=(0.1, 0.5, 0.9))
    assert loss > 0
    pred_good = torch.ones(2, 5, 2, 3)
    loss_good = quantile_loss(pred_good, target, quantiles=(0.1, 0.5, 0.9))
    assert loss_good < loss


def test_deep_ensemble_aggregates_predictions(sample_batch: dict[str, torch.Tensor]) -> None:
    x, mask = sample_batch["x"], sample_batch["mask"]
    n_features = x.size(-1)
    models = [
        LSTMTrackForecaster(
            n_features=n_features, n_horizons=5, n_classes=7, hidden_size=32, num_layers=1
        )
        for _ in range(3)
    ]
    ensemble = DeepEnsemble(models)
    result = ensemble.predict(x, mask)
    assert result["reg_mean"].shape == (1, 5, 2)


def test_cone_radius_grows_with_horizon() -> None:
    r6 = cone_radius_km(6)
    r72 = cone_radius_km(72)
    assert r72 > r6


def test_build_cone_closes_ring() -> None:
    points = build_cone(12.0, 120.0, 50.0, n_points=16)
    assert len(points) == 17
    assert points[0] == points[-1]
