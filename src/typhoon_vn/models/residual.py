"""Residual wrapper: any track model predicts displacement from the last fix.

Neural models see train-scaled inputs. Predicting absolute degrees from those
inputs forces the network to learn the whole coordinate range (thousands of
km of error); predicting the displacement from the last observed position is
the standard formulation. This wrapper recovers the last position in degrees
from the scaled lat/lon features (columns 0 and 1) and adds it to ``reg``.
"""

from __future__ import annotations

import torch

from typhoon_vn.models.base import TrackForecaster


class ResidualTrackForecaster(TrackForecaster):
    def __init__(
        self,
        base: TrackForecaster,
        position_mean: list[float],
        position_scale: list[float],
    ) -> None:
        super().__init__()
        if len(position_mean) != 2 or len(position_scale) != 2:
            raise ValueError("position statistics must hold lat and lon")
        if min(position_scale) <= 0:
            raise ValueError("position_scale must be positive")
        self.base = base
        self.register_buffer(
            "position_mean", torch.tensor(position_mean, dtype=torch.float32)
        )
        self.register_buffer(
            "position_scale", torch.tensor(position_scale, dtype=torch.float32)
        )

    def forward(
        self, x: torch.Tensor, mask: torch.Tensor | None = None
    ) -> dict[str, torch.Tensor]:
        out = dict(self.base(x, mask))
        if mask is None:
            last = x[:, -1, :2]
        else:
            lengths = mask.to(torch.long).sum(dim=1)
            last = x[torch.arange(x.shape[0], device=x.device), lengths - 1, :2]
        anchor = last * self.position_scale + self.position_mean
        out["reg"] = anchor.unsqueeze(1) + out["reg"]
        return out

    def encode(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        return self.base.encode(x, mask)

    @property
    def context_size(self) -> int:
        return self.base.context_size

    @property
    def n_horizons(self) -> int:
        return self.base.n_horizons

    @property
    def n_classes(self) -> int:
        return self.base.n_classes
