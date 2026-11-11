"""Additional model, loss, and evaluation gate contracts."""

import numpy as np
import pandas as pd
import pytest
import torch

from typhoon_vn.evaluation.backtest import backtest_storm
from typhoon_vn.evaluation.metrics import (
    intensity_classification_scores,
    track_error_km,
)
from typhoon_vn.models.lstm import (
    AttentionLSTMTrackForecaster,
    LSTMTrackForecaster,
    Seq2SeqLSTMTrackForecaster,
)
from typhoon_vn.models.transformer import TransformerTrackForecaster
from typhoon_vn.training.losses import MultiHorizonLoss


@pytest.mark.parametrize(
    "factory",
    [
        lambda: LSTMTrackForecaster(3, 2, 4, hidden_size=8, num_layers=1),
        lambda: AttentionLSTMTrackForecaster(3, 2, 4, hidden_size=8, num_layers=1),
    ],
)
def test_right_padding_does_not_change_valid_sequence_output(factory) -> None:
    torch.manual_seed(4)
    model = factory().eval()
    prefix = torch.randn(1, 2, 3)
    first = torch.cat([prefix, torch.zeros(1, 2, 3)], dim=1)
    second = torch.cat([prefix, torch.full((1, 2, 3), 99.0)], dim=1)
    mask = torch.tensor([[1.0, 1.0, 0.0, 0.0]])
    assert torch.allclose(model(first, mask)["reg"], model(second, mask)["reg"])


def test_attention_masks_padding_and_normalizes_valid_weights() -> None:
    model = AttentionLSTMTrackForecaster(3, 2, 4, hidden_size=8, num_layers=1)
    output = model(torch.randn(1, 4, 3), torch.tensor([[1.0, 1.0, 0.0, 0.0]]))
    assert output["attn"][0, 2:].tolist() == [0.0, 0.0]
    assert output["attn"][0, :2].sum().item() == pytest.approx(1.0)


def test_seq2seq_eval_never_reads_teacher_forcing_targets() -> None:
    model = Seq2SeqLSTMTrackForecaster(
        3, 2, 4, hidden_size=8, num_layers=1, teacher_forcing_ratio=1.0
    ).eval()
    x = torch.randn(1, 4, 3)
    mask = torch.ones(1, 4)
    first = model(x, mask, torch.zeros(1, 2, 2), torch.zeros(1, 2, dtype=torch.long))
    second = model(x, mask, torch.ones(1, 2, 2), torch.ones(1, 2, dtype=torch.long))
    assert torch.allclose(first["reg"], second["reg"])
    assert torch.allclose(first["cls"], second["cls"])


def test_transformer_rejects_fully_masked_sequence() -> None:
    model = TransformerTrackForecaster(3, 2, 4, d_model=8, nhead=2, n_layers=1)
    with pytest.raises(ValueError, match="valid timestep"):
        model(torch.zeros(1, 4, 3), torch.zeros(1, 4))


def test_loss_masks_missing_regression_and_classification_targets() -> None:
    loss_fn = MultiHorizonLoss(2, 3)
    pred_reg = torch.zeros(1, 2, 2)
    pred_cls = torch.zeros(1, 2, 3)
    target_reg = torch.tensor([[[1.0, 1.0], [float("nan"), float("nan")]]])
    target_cls = torch.tensor([[1, -1]])
    loss, parts = loss_fn(
        pred_reg,
        pred_cls,
        target_reg,
        target_cls,
        reg_mask=torch.tensor([[True, False]]),
        cls_mask=torch.tensor([[True, False]]),
    )
    assert torch.isfinite(loss)
    assert all(torch.isfinite(value) for value in parts.values())


def test_metrics_reject_empty_and_mask_unknown_labels() -> None:
    with pytest.raises(ValueError, match="empty"):
        track_error_km(np.empty((0, 2)), np.empty((0, 2)))
    scores = intensity_classification_scores(
        np.array([[0, 1], [1, 0]]),
        np.array([[0, -1], [1, 0]]),
        n_classes=2,
        unknown_label=-1,
    )
    assert scores["support"].tolist() == [[1, 1], [1, 0]]
    assert scores["accuracy"].tolist() == [1.0, 1.0]


def test_backtest_storm_rejects_multiple_storm_ids() -> None:
    frame = pd.DataFrame(
        {
            "storm_id": ["A", "B"],
            "timestamp": pd.date_range("2025-01-01", periods=2, freq="6h", tz="UTC"),
            "lat": [10.0, 11.0],
            "lon": [110.0, 111.0],
        }
    )
    model = LSTMTrackForecaster(2, 1, 2, hidden_size=4, num_layers=1)
    with pytest.raises(ValueError, match="single storm"):
        backtest_storm(model, frame)
