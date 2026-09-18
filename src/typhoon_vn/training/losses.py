"""Loss functions for multi-horizon track and intensity forecasting."""

from __future__ import annotations

import math
from collections.abc import Sequence

import torch
from torch import nn

from typhoon_vn.features.geo import EARTH_RADIUS_KM


class HaversineLoss(nn.Module):
    """Direct great-circle distance loss in kilometres."""

    def __init__(self, reduction: str = "mean") -> None:
        super().__init__()
        self.reduction = reduction

    def forward(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        # pred/target: (..., 2) with last dim (lat, lon) in degrees
        lat1, lon1 = pred[..., 0], pred[..., 1]
        lat2, lon2 = target[..., 0], target[..., 1]
        dlat = torch.deg2rad(lat2 - lat1)
        dlon = torch.deg2rad(lon2 - lon1)
        rad_lat1 = torch.deg2rad(lat1)
        rad_lat2 = torch.deg2rad(lat2)
        a = (
            torch.sin(dlat / 2.0) ** 2
            + torch.cos(rad_lat1) * torch.cos(rad_lat2) * torch.sin(dlon / 2.0) ** 2
        )
        c = 2.0 * torch.asin(torch.sqrt(a.clamp(min=0.0, max=1.0)))
        dist = EARTH_RADIUS_KM * c
        if self.reduction == "mean":
            return dist.mean()
        if self.reduction == "sum":
            return dist.sum()
        return dist


class MultiHorizonLoss(nn.Module):
    """Combined regression + classification loss with per-horizon weights.

    The regression loss can be Smooth L1 or Haversine. Classification uses
    cross-entropy. Later horizons can be penalised more heavily via
    ``horizon_weights``.
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
        self.n_horizons = n_horizons
        self.n_classes = n_classes
        self.reg_weight = reg_weight
        self.cls_weight = cls_weight
        self.reg_loss_name = reg_loss
        if horizon_weights is None:
            # Exponential growth: penalise far horizons meaningfully.
            # Track forecast error grows roughly exponentially with lead time,
            # so weights should too.  With base 1.26 and 5 horizons the weights
            # are approximately [1.0, 1.26, 1.59, 2.0, 2.52], giving the 72-h
            # horizon ~2.5× the weight of the 6-h horizon.
            horizon_weights = [1.26**i for i in range(n_horizons)]
        self.register_buffer(
            "horizon_weights",
            torch.tensor(list(horizon_weights), dtype=torch.float32),
        )
        if reg_loss == "smooth_l1":
            self.reg_criterion = nn.SmoothL1Loss(reduction="none")
        elif reg_loss == "haversine":
            self.reg_criterion = HaversineLoss(reduction="none")
        else:
            raise ValueError(f"Unknown regression loss: {reg_loss}")
        self.cls_criterion = nn.CrossEntropyLoss(reduction="none")

    def forward(
        self,
        pred_reg: torch.Tensor,
        pred_cls: torch.Tensor,
        target_reg: torch.Tensor,
        target_cls: torch.Tensor,
    ) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        # pred_reg/target_reg: (B, H, 2); pred_cls: (B, H, C); target_cls: (B, H)
        if self.reg_loss_name == "smooth_l1":
            reg_loss_per_step = self.reg_criterion(pred_reg, target_reg).mean(dim=-1)  # (B, H)
        else:
            reg_loss_per_step = self.reg_criterion(pred_reg, target_reg)  # (B, H)
        reg_loss = (reg_loss_per_step * self.horizon_weights).mean()

        cls_loss_per_step = self.cls_criterion(
            pred_cls.reshape(-1, self.n_classes),
            target_cls.reshape(-1).clamp(0, self.n_classes - 1),
        ).view(-1, self.n_horizons)
        cls_loss = (cls_loss_per_step * self.horizon_weights).mean()

        total = self.reg_weight * reg_loss + self.cls_weight * cls_loss
        return total, {
            "loss": total,
            "reg_loss": reg_loss,
            "cls_loss": cls_loss,
        }
