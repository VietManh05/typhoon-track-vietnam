"""Uncertainty estimation and cone-of-uncertainty helpers.

Provides Monte-Carlo dropout, quantile regression, deep-ensemble wrappers,
and a cone-radius heuristic compatible with the multi-horizon outputs.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np
import torch
from torch import nn

from typhoon_vn.models.base import TrackForecaster


def cone_radius_km(horizon_hours: int, base_km: float = 30.0, growth_rate: float = 1.18) -> float:
    """Heuristic cone radius that grows with forecast lead time.

    The default parameters approximate typical NHC/NCHMF cone growth:
    roughly 30 km at 6 h, ~100 km at 72 h.
    """

    return base_km * (growth_rate ** (horizon_hours / 6.0))


def build_cone(
    center_lat: float,
    center_lon: float,
    radius_km: float,
    n_points: int = 32,
) -> list[tuple[float, float]]:
    """Return a circle of lat/lon points around a center."""

    from typhoon_vn.features.geo import destination_point

    points: list[tuple[float, float]] = []
    for i in range(n_points):
        bearing = i * 360.0 / n_points
        points.append(destination_point(center_lat, center_lon, bearing, radius_km))
    points.append(points[0])  # close ring
    return points


def cone_to_geojson(
    forecast_points: list[tuple[float, float]],
    horizon_hours: list[int],
    base_km: float = 30.0,
    growth_rate: float = 1.18,
    n_points: int = 32,
) -> dict[str, Any]:
    """Build a GeoJSON FeatureCollection with cone polygons and track points.

    Each horizon produces:
    - A ``Polygon`` feature for the uncertainty circle (cone slice).
    - A ``Point`` feature for the forecast position.

    Args:
        forecast_points: list of ``(lat, lon)`` forecast positions, one per horizon.
        horizon_hours: lead-time in hours for each forecast position.
        base_km: base cone radius at 6 h (passed to ``cone_radius_km``).
        growth_rate: growth factor (passed to ``cone_radius_km``).
        n_points: number of ring vertices per cone polygon.

    Returns:
        A GeoJSON FeatureCollection dict ready for ``json.dumps``.
    """
    features: list[dict[str, Any]] = []
    for (lat, lon), hours in zip(forecast_points, horizon_hours):
        radius = cone_radius_km(hours, base_km=base_km, growth_rate=growth_rate)
        ring = build_cone(lat, lon, radius, n_points=n_points)
        # GeoJSON uses [lon, lat] coordinate order
        ring_coords = [[pt[1], pt[0]] for pt in ring]
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Polygon", "coordinates": [ring_coords]},
                "properties": {
                    "horizon_hours": hours,
                    "radius_km": round(radius, 2),
                    "center_lat": lat,
                    "center_lon": lon,
                    "feature_type": "cone",
                },
            }
        )
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": {
                    "horizon_hours": hours,
                    "feature_type": "forecast_point",
                },
            }
        )
    return {"type": "FeatureCollection", "features": features}


def mc_dropout_predict(
    model: TrackForecaster,
    x: torch.Tensor,
    mask: torch.Tensor | None,
    n_samples: int = 50,
) -> dict[str, torch.Tensor]:
    """Run inference ``n_samples`` times with dropout enabled.

    Returns mean and std for regression outputs and class probabilities.
    """

    model.train()  # keep dropout active
    reg_samples: list[torch.Tensor] = []
    cls_samples: list[torch.Tensor] = []
    with torch.no_grad():
        for _ in range(n_samples):
            out = model(x, mask)
            reg_samples.append(out["reg"])
            cls_samples.append(torch.softmax(out["cls"], dim=-1))
    reg_stack = torch.stack(reg_samples, dim=0)  # (S, B, H, 2)
    cls_stack = torch.stack(cls_samples, dim=0)  # (S, B, H, C)
    return {
        "reg_mean": reg_stack.mean(dim=0),
        "reg_std": reg_stack.std(dim=0),
        "cls_mean": cls_stack.mean(dim=0),
        "cls_std": cls_stack.std(dim=0),
    }


class QuantileTrackForecaster(TrackForecaster):
    """Wraps any forecaster and replaces the regression head with quantile outputs.

    Predicts three quantiles (0.1, 0.5, 0.9) for each horizon and coordinate.

    The wrapped ``base_model`` must implement :meth:`encode` and
    :attr:`context_size` (i.e. not ``Seq2SeqLSTMTrackForecaster``).
    """

    def __init__(
        self,
        base_model: TrackForecaster,
        quantiles: Sequence[float] = (0.1, 0.5, 0.9),
    ) -> None:
        super().__init__()
        self.base_model = base_model
        self.quantiles = list(quantiles)
        n_horizons = base_model.n_horizons
        n_classes = base_model.n_classes
        # Use context_size from the base model (e.g. hidden_size for LSTM, d_model
        # for Transformer) so the Linear layer always matches the encoder output.
        try:
            context_sz = base_model.context_size
        except NotImplementedError:
            raise ValueError(
                f"{type(base_model).__name__} does not implement context_size. "
                "Use LSTMTrackForecaster or AttentionLSTMTrackForecaster."
            )
        self.reg_head = nn.Linear(context_sz, n_horizons * 2 * len(quantiles))
        self._n_classes = n_classes
        self._n_horizons = n_horizons

    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> dict[str, torch.Tensor]:
        # Single forward pass through the encoder — no double-forward, no
        # dropout inconsistency between the reg and cls branches.
        context = self.base_model.encode(x, mask)  # (B, context_size)
        reg = self.reg_head(context).view(-1, self._n_horizons, 2, len(self.quantiles))
        # Reuse the base model's classification head directly on the same context.
        cls = self.base_model.cls_head(context).view(-1, self._n_horizons, self._n_classes)
        return {"reg": reg, "cls": cls, "quantiles": self.quantiles}

    def encode(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        return self.base_model.encode(x, mask)

    @property
    def context_size(self) -> int:
        return self.base_model.context_size


def quantile_loss(pred: torch.Tensor, target: torch.Tensor, quantiles: Sequence[float]) -> torch.Tensor:
    """Pinball loss for quantile regression.

    ``pred`` shape: (B, H, 2, Q); ``target`` shape: (B, H, 2).
    """

    quantiles_t = torch.tensor(quantiles, device=pred.device, dtype=pred.dtype)
    target = target.unsqueeze(-1)  # (B, H, 2, 1)
    errors = target - pred  # negative when pred is too high
    losses = torch.max(
        quantiles_t.view(1, 1, 1, -1) * errors,
        (quantiles_t.view(1, 1, 1, -1) - 1.0) * errors,
    )
    return losses.mean()


class DeepEnsemble:
    """Simple deep-ensemble wrapper that aggregates multiple trained models."""

    def __init__(self, models: Sequence[TrackForecaster]) -> None:
        self.models = list(models)

    def predict(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> dict[str, torch.Tensor]:
        reg_samples: list[torch.Tensor] = []
        cls_samples: list[torch.Tensor] = []
        with torch.no_grad():
            for m in self.models:
                m.eval()
                out = m(x, mask)
                reg_samples.append(out["reg"])
                cls_samples.append(torch.softmax(out["cls"], dim=-1))
        reg_stack = torch.stack(reg_samples, dim=0)
        cls_stack = torch.stack(cls_samples, dim=0)
        return {
            "reg_mean": reg_stack.mean(dim=0),
            "reg_std": reg_stack.std(dim=0),
            "cls_mean": cls_stack.mean(dim=0),
            "cls_std": cls_stack.std(dim=0),
        }
