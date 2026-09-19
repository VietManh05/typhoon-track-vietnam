"""Synthetic tensor contracts for Phase 3 loss prework."""

import pytest
import torch

from typhoon_vn.training.losses import HaversineLoss, MultiHorizonLoss


def _valid_batch(batch_size: int = 2, horizons: int = 3, classes: int = 4):
    pred_reg = torch.zeros(batch_size, horizons, 2, requires_grad=True)
    pred_cls = torch.zeros(batch_size, horizons, classes, requires_grad=True)
    target_reg = torch.ones(batch_size, horizons, 2)
    target_cls = torch.zeros(batch_size, horizons, dtype=torch.long)
    return pred_reg, pred_cls, target_reg, target_cls


def test_multi_horizon_loss_has_finite_components_and_gradients() -> None:
    loss_fn = MultiHorizonLoss(n_horizons=3, n_classes=4)
    pred_reg, pred_cls, target_reg, target_cls = _valid_batch()
    loss, components = loss_fn(pred_reg, pred_cls, target_reg, target_cls)
    loss.backward()
    assert set(components) == {"loss", "reg_loss", "cls_loss"}
    assert all(torch.isfinite(value) for value in components.values())
    assert pred_reg.grad is not None and torch.isfinite(pred_reg.grad).all()
    assert pred_cls.grad is not None and torch.isfinite(pred_cls.grad).all()


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"n_horizons": 0, "n_classes": 4}, "n_horizons"),
        ({"n_horizons": 3, "n_classes": 1}, "n_classes"),
        (
            {"n_horizons": 3, "n_classes": 4, "horizon_weights": [1.0, 2.0]},
            "horizon_weights length",
        ),
        (
            {"n_horizons": 3, "n_classes": 4, "horizon_weights": [1.0, 0.0, 2.0]},
            "finite positive",
        ),
    ],
)
def test_multi_horizon_loss_rejects_invalid_configuration(kwargs, message) -> None:
    with pytest.raises(ValueError, match=message):
        MultiHorizonLoss(**kwargs)


def test_multi_horizon_loss_rejects_nan_and_empty_batches() -> None:
    loss_fn = MultiHorizonLoss(n_horizons=3, n_classes=4)
    pred_reg, pred_cls, target_reg, target_cls = _valid_batch()
    pred_reg = pred_reg.detach()
    pred_reg[0, 0, 0] = float("nan")
    with pytest.raises(ValueError, match="pred_reg.*finite"):
        loss_fn(pred_reg, pred_cls, target_reg, target_cls)
    with pytest.raises(ValueError, match="at least one sample"):
        loss_fn(
            torch.empty(0, 3, 2),
            torch.empty(0, 3, 4),
            torch.empty(0, 3, 2),
            torch.empty(0, 3, dtype=torch.long),
        )


def test_multi_horizon_loss_rejects_invalid_class_instead_of_clamping() -> None:
    loss_fn = MultiHorizonLoss(n_horizons=3, n_classes=4)
    pred_reg, pred_cls, target_reg, target_cls = _valid_batch()
    target_cls[0, 0] = 4
    with pytest.raises(ValueError, match="target_cls values"):
        loss_fn(pred_reg, pred_cls, target_reg, target_cls)


def test_horizon_weights_change_the_loss_contribution() -> None:
    pred_reg = torch.tensor([[[1.0, 1.0], [1.0, 1.0]]])
    target_reg = torch.zeros_like(pred_reg)
    pred_cls = torch.zeros(1, 2, 2)
    target_cls = torch.zeros(1, 2, dtype=torch.long)
    equal = MultiHorizonLoss(2, 2, horizon_weights=[1.0, 1.0], cls_weight=0.0)
    later = MultiHorizonLoss(2, 2, horizon_weights=[1.0, 4.0], cls_weight=0.0)
    equal_loss, _ = equal(pred_reg, pred_cls, target_reg, target_cls)
    later_loss, _ = later(pred_reg, pred_cls, target_reg, target_cls)
    assert later_loss > equal_loss


def test_haversine_loss_handles_identity_reference_and_dateline() -> None:
    loss_fn = HaversineLoss(reduction="none")
    pred = torch.tensor([[0.0, 0.0], [0.0, 179.0], [0.0, 0.0]])
    target = torch.tensor([[0.0, 0.0], [0.0, -179.0], [0.0, 1.0]])
    distances = loss_fn(pred, target)
    assert distances[0].item() == pytest.approx(0.0, abs=1e-6)
    assert distances[1].item() == pytest.approx(222.39, abs=0.5)
    assert distances[2].item() == pytest.approx(111.195, abs=0.5)


@pytest.mark.parametrize(
    "bad", [torch.tensor([[float("nan"), 0.0]]), torch.empty(0, 2)]
)
def test_haversine_loss_rejects_non_finite_or_empty_coordinates(bad) -> None:
    with pytest.raises(ValueError):
        HaversineLoss()(bad, bad)
