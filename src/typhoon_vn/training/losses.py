"""Loss functions for multi-horizon track and intensity forecasting."""

from __future__ import annotations

import math
from collections.abc import Sequence

import torch
from torch import nn

from typhoon_vn.features.geo import EARTH_RADIUS_KM


class HaversineLoss(nn.Module):
    """Great-circle distance in kilometres for (..., 2) lat/lon tensors."""

    _REDUCTIONS = {"none", "mean", "sum"}

    def __init__(self, reduction: str = "mean") -> None:
        super().__init__()
        if reduction not in self._REDUCTIONS:
            raise ValueError(
                f"reduction must be one of {sorted(self._REDUCTIONS)}, got {reduction!r}"
            )
        self.reduction = reduction

    @staticmethod
    def _validate_coordinates(pred: torch.Tensor, target: torch.Tensor) -> None:
        if pred.shape != target.shape:
            raise ValueError("pred and target coordinates must have the same shape")
        if pred.ndim < 1 or pred.shape[-1] != 2:
            raise ValueError("coordinate tensors must have shape (..., 2)")
        if pred.numel() == 0:
            raise ValueError("coordinate tensors must not be empty")
        if not torch.is_floating_point(pred) or not torch.is_floating_point(target):
            raise TypeError("coordinate tensors must use a floating-point dtype")
        if not torch.isfinite(pred).all() or not torch.isfinite(target).all():
            raise ValueError("coordinate tensors must contain only finite values")
        if (pred[..., 0].abs() > 90).any() or (target[..., 0].abs() > 90).any():
            raise ValueError("latitude must be within [-90, 90] degrees")

    def forward(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        self._validate_coordinates(pred, target)
        lat1, lon1 = pred[..., 0], pred[..., 1]
        lat2, lon2 = target[..., 0], target[..., 1]
        dlat = torch.deg2rad(lat2 - lat1)
        dlon_deg = torch.remainder(lon2 - lon1 + 180.0, 360.0) - 180.0
        dlon = torch.deg2rad(dlon_deg)
        rad_lat1 = torch.deg2rad(lat1)
        rad_lat2 = torch.deg2rad(lat2)
        a = (
            torch.sin(dlat / 2.0) ** 2
            + torch.cos(rad_lat1) * torch.cos(rad_lat2) * torch.sin(dlon / 2.0) ** 2
        ).clamp(min=0.0, max=1.0)
        dist = EARTH_RADIUS_KM * 2.0 * torch.asin(torch.sqrt(a))
        if not torch.isfinite(dist).all():
            raise ValueError("haversine distance must be finite")
        if self.reduction == "mean":
            return dist.mean()
        if self.reduction == "sum":
            return dist.sum()
        return dist


class MultiHorizonLoss(nn.Module):
    """Combined regression and classification loss with horizon weights.

    This tensor-only component can be tested with synthetic fixtures before the
    real-data M1 gate. Passing these contracts is not model-skill evidence.
    """

    def __init__(
        self,
        n_horizons: int,
        n_classes: int,
        reg_loss: str = "smooth_l1",
        horizon_weights: Sequence[float] | None = None,
        reg_weight: float = 1.0,
        cls_weight: float = 0.3,
    ) -> None:
        super().__init__()
        if n_horizons <= 0:
            raise ValueError("n_horizons must be positive")
        if n_classes <= 1:
            raise ValueError("n_classes must be greater than one")
        if not math.isfinite(reg_weight) or reg_weight < 0:
            raise ValueError("reg_weight must be finite and non-negative")
        if not math.isfinite(cls_weight) or cls_weight < 0:
            raise ValueError("cls_weight must be finite and non-negative")
        if reg_weight == 0 and cls_weight == 0:
            raise ValueError("at least one loss component weight must be positive")
        self.n_horizons = n_horizons
        self.n_classes = n_classes
        self.reg_weight = reg_weight
        self.cls_weight = cls_weight
        self.reg_loss_name = reg_loss
        if horizon_weights is None:
            horizon_weights = [1.26**i for i in range(n_horizons)]
        weights = list(horizon_weights)
        if len(weights) != n_horizons:
            raise ValueError("horizon_weights length must equal n_horizons")
        if not all(math.isfinite(weight) and weight > 0 for weight in weights):
            raise ValueError("horizon_weights must contain finite positive values")
        self.register_buffer(
            "horizon_weights", torch.tensor(weights, dtype=torch.float32)
        )
        if reg_loss == "smooth_l1":
            self.reg_criterion = nn.SmoothL1Loss(reduction="none")
        elif reg_loss == "haversine":
            self.reg_criterion = HaversineLoss(reduction="none")
        else:
            raise ValueError(f"Unknown regression loss: {reg_loss}")
        self.cls_criterion = nn.CrossEntropyLoss(reduction="none")

    def _validate_inputs(
        self,
        pred_reg: torch.Tensor,
        pred_cls: torch.Tensor,
        target_reg: torch.Tensor,
        target_cls: torch.Tensor,
    ) -> None:
        batch_size = pred_reg.shape[0] if pred_reg.ndim else 0
        if pred_reg.ndim != 3 or tuple(pred_reg.shape[1:]) != (self.n_horizons, 2):
            raise ValueError(f"pred_reg must have shape (B, {self.n_horizons}, 2)")
        if target_reg.shape != pred_reg.shape:
            raise ValueError("target_reg must have the same shape as pred_reg")
        if tuple(pred_cls.shape) != (batch_size, self.n_horizons, self.n_classes):
            raise ValueError("pred_cls has an invalid shape")
        if tuple(target_cls.shape) != (batch_size, self.n_horizons):
            raise ValueError("target_cls has an invalid shape")
        if batch_size == 0:
            raise ValueError("loss inputs must contain at least one sample")
        # Validate model outputs here so invalid predictions fail at the loss
        # boundary. Non-finite targets intentionally flow into the component
        # metrics, allowing Trainer to report whether the failure came from the
        # training or validation loader while preserving its checkpoint guard.
        for name, tensor in (("pred_reg", pred_reg), ("pred_cls", pred_cls)):
            if not torch.is_floating_point(tensor):
                raise TypeError(f"{name} must use a floating-point dtype")
            if not torch.isfinite(tensor).all():
                raise ValueError(f"{name} must contain only finite values")
        if target_cls.dtype == torch.bool or target_cls.is_floating_point():
            raise TypeError("target_cls must use an integer dtype")
        if (target_cls < 0).any() or (target_cls >= self.n_classes).any():
            raise ValueError(
                f"target_cls values must be within [0, {self.n_classes - 1}]"
            )

    def forward(
        self,
        pred_reg: torch.Tensor,
        pred_cls: torch.Tensor,
        target_reg: torch.Tensor,
        target_cls: torch.Tensor,
    ) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        self._validate_inputs(pred_reg, pred_cls, target_reg, target_cls)
        weights = self.horizon_weights.to(device=pred_reg.device, dtype=pred_reg.dtype)
        if self.reg_loss_name == "smooth_l1":
            reg_per_step = self.reg_criterion(pred_reg, target_reg).mean(dim=-1)
        else:
            reg_per_step = self.reg_criterion(pred_reg, target_reg)
        reg_loss = (reg_per_step * weights).mean()
        cls_per_step = self.cls_criterion(
            pred_cls.reshape(-1, self.n_classes), target_cls.reshape(-1)
        ).view(-1, self.n_horizons)
        cls_loss = (cls_per_step * weights.to(pred_cls)).mean()
        total = self.reg_weight * reg_loss + self.cls_weight * cls_loss
        # Trainer performs the final component check so its error identifies
        # whether a non-finite target came from training or validation data.
        return total, {"loss": total, "reg_loss": reg_loss, "cls_loss": cls_loss}
