"""Uncertainty estimation and cone-of-uncertainty helpers.

Provides Monte-Carlo dropout, quantile regression, deep-ensemble wrappers,
and a cone-radius heuristic compatible with the multi-horizon outputs.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import nn

from typhoon_vn.models.base import TrackForecaster


def cone_radius_km(
    horizon_hours: int, base_km: float = 30.0, growth_rate: float = 1.18
) -> float:
    """Heuristic cone radius that grows with forecast lead time.

    The default parameters approximate typical NHC/NCHMF cone growth:
    roughly 30 km at 6 h, ~100 km at 72 h.
    """

    if horizon_hours <= 0:
        raise ValueError("horizon_hours must be positive")
    if base_km <= 0 or growth_rate < 1:
        raise ValueError("base_km must be positive and growth_rate must be >= 1")
    return base_km * (growth_rate ** (horizon_hours / 6.0))


def build_cone(
    center_lat: float,
    center_lon: float,
    radius_km: float,
    n_points: int = 32,
) -> list[tuple[float, float]]:
    """Return a circle of lat/lon points around a center."""

    from typhoon_vn.features.geo import destination_point

    if not all(math.isfinite(value) for value in (center_lat, center_lon, radius_km)):
        raise ValueError("cone inputs must be finite")
    if not -90 <= center_lat <= 90 or not -180 <= center_lon <= 180:
        raise ValueError("cone center is outside valid latitude/longitude bounds")
    if radius_km <= 0 or n_points < 3:
        raise ValueError("radius_km must be positive and n_points must be >= 3")

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
    if len(forecast_points) != len(horizon_hours):
        raise ValueError("forecast_points and horizon_hours must have equal length")
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

    if n_samples < 2:
        raise ValueError("n_samples must be at least 2")
    original_states = {module: module.training for module in model.modules()}
    model.eval()
    for module in model.modules():
        if isinstance(module, nn.modules.dropout._DropoutNd):
            module.train()
    reg_samples: list[torch.Tensor] = []
    cls_samples: list[torch.Tensor] = []
    try:
        with torch.no_grad():
            for _ in range(n_samples):
                out = model(x, mask)
                reg_samples.append(out["reg"])
                cls_samples.append(torch.softmax(out["cls"], dim=-1))
    finally:
        for module, training in original_states.items():
            module.train(training)
    reg_stack = torch.stack(reg_samples, dim=0)  # (S, B, H, 2)
    cls_stack = torch.stack(cls_samples, dim=0)  # (S, B, H, C)
    return {
        "reg_samples": reg_stack,
        "reg_mean": reg_stack.mean(dim=0),
        "reg_std": reg_stack.std(dim=0, unbiased=False),
        "reg_quantiles": torch.quantile(
            reg_stack, torch.tensor([0.1, 0.5, 0.9], device=reg_stack.device), dim=0
        ),
        "cls_samples": cls_stack,
        "cls_mean": cls_stack.mean(dim=0),
        "cls_std": cls_stack.std(dim=0, unbiased=False),
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
        if not self.quantiles or any(not 0 < q < 1 for q in self.quantiles):
            raise ValueError("quantiles must be non-empty and lie inside (0, 1)")
        if self.quantiles != sorted(set(self.quantiles)):
            raise ValueError("quantiles must be unique and strictly increasing")
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

    def forward(
        self, x: torch.Tensor, mask: torch.Tensor | None = None
    ) -> dict[str, torch.Tensor]:
        # Single forward pass through the encoder — no double-forward, no
        # dropout inconsistency between the reg and cls branches.
        context = self.base_model.encode(x, mask)  # (B, context_size)
        raw_reg = self.reg_head(context).view(
            -1, self._n_horizons, 2, len(self.quantiles)
        )
        reg = torch.sort(raw_reg, dim=-1).values
        # Reuse the base model's classification head directly on the same context.
        cls = self.base_model.cls_head(context).view(
            -1, self._n_horizons, self._n_classes
        )
        return {"reg": reg, "cls": cls, "quantiles": self.quantiles}

    def encode(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        return self.base_model.encode(x, mask)

    @property
    def context_size(self) -> int:
        return self.base_model.context_size


def quantile_loss(
    pred: torch.Tensor, target: torch.Tensor, quantiles: Sequence[float]
) -> torch.Tensor:
    """Pinball loss for quantile regression.

    ``pred`` shape: (B, H, 2, Q); ``target`` shape: (B, H, 2).
    """

    if pred.ndim != 4 or target.shape != pred.shape[:-1]:
        raise ValueError("pred must be (B,H,2,Q) and target must be (B,H,2)")
    if pred.shape[-1] != len(quantiles):
        raise ValueError("prediction quantile dimension does not match quantiles")
    if not quantiles or any(not 0 < q < 1 for q in quantiles):
        raise ValueError("quantiles must lie inside (0, 1)")
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
        if not self.models:
            raise ValueError("deep ensemble requires at least one model")
        contract = (self.models[0].n_horizons, self.models[0].n_classes)
        if any((model.n_horizons, model.n_classes) != contract for model in self.models):
            raise ValueError("all ensemble members must share the same output contract")

    def predict(
        self, x: torch.Tensor, mask: torch.Tensor | None = None
    ) -> dict[str, torch.Tensor]:
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
            "reg_samples": reg_stack,
            "reg_mean": reg_stack.mean(dim=0),
            "reg_std": reg_stack.std(dim=0, unbiased=False),
            "cls_samples": cls_stack,
            "cls_mean": cls_stack.mean(dim=0),
            "cls_std": cls_stack.std(dim=0, unbiased=False),
        }


@dataclass(frozen=True)
class CalibratedCone:
    """Empirical per-horizon cone radii fitted only on held-out errors."""

    horizons: tuple[int, ...]
    radii_km: tuple[float, ...]
    coverage: float = 0.9

    @classmethod
    def fit(
        cls,
        errors_km: np.ndarray | torch.Tensor,
        horizons: Sequence[int],
        coverage: float = 0.9,
    ) -> "CalibratedCone":
        errors = (
            errors_km.detach().cpu().numpy()
            if isinstance(errors_km, torch.Tensor)
            else np.asarray(errors_km, dtype=float)
        )
        horizon_values = tuple(int(value) for value in horizons)
        if errors.ndim != 2 or errors.shape[1] != len(horizon_values):
            raise ValueError("errors_km must have shape (samples, horizons)")
        if errors.shape[0] < 2 or not np.isfinite(errors).all() or (errors < 0).any():
            raise ValueError("calibration errors must be finite, non-negative samples")
        if not 0 < coverage < 1:
            raise ValueError("coverage must lie inside (0, 1)")
        if any(value <= 0 for value in horizon_values):
            raise ValueError("horizons must be positive")
        radii = np.quantile(errors, coverage, axis=0, method="higher")
        radii = np.maximum.accumulate(radii)
        return cls(horizon_values, tuple(float(value) for value in radii), coverage)

    def coverage_report(
        self, errors_km: np.ndarray | torch.Tensor
    ) -> dict[int, float]:
        errors = (
            errors_km.detach().cpu().numpy()
            if isinstance(errors_km, torch.Tensor)
            else np.asarray(errors_km, dtype=float)
        )
        if errors.ndim != 2 or errors.shape[1] != len(self.horizons):
            raise ValueError("errors_km must match calibrated horizons")
        return {
            horizon: float(np.mean(errors[:, index] <= self.radii_km[index]))
            for index, horizon in enumerate(self.horizons)
        }

    def radius_for(self, horizon_hours: int) -> float:
        try:
            return self.radii_km[self.horizons.index(horizon_hours)]
        except ValueError as exc:
            raise KeyError(f"no calibrated radius for {horizon_hours} h") from exc

    def save(self, path: str | Path) -> Path:
        """Persist calibration independently from model-selection/test data."""

        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(
                {
                    "horizons": self.horizons,
                    "radii_km": self.radii_km,
                    "coverage": self.coverage,
                    "method": "empirical held-out radial-error quantile",
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        return destination

    @classmethod
    def load(cls, path: str | Path) -> "CalibratedCone":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if set(payload) != {"horizons", "radii_km", "coverage", "method"}:
            raise ValueError("invalid calibrated-cone schema")
        if payload["method"] != "empirical held-out radial-error quantile":
            raise ValueError("unsupported calibrated-cone method")
        return cls(
            tuple(int(value) for value in payload["horizons"]),
            tuple(float(value) for value in payload["radii_km"]),
            float(payload["coverage"]),
        )

    def to_geojson(
        self,
        forecast_points: Sequence[tuple[float, float]],
        *,
        n_points: int = 32,
    ) -> dict[str, Any]:
        """Create calibrated polygons without relabelling dispersion as coverage."""

        if len(forecast_points) != len(self.horizons):
            raise ValueError("forecast_points must match calibrated horizons")
        features: list[dict[str, Any]] = []
        for (lat, lon), horizon, radius in zip(
            forecast_points, self.horizons, self.radii_km
        ):
            ring = build_cone(lat, lon, radius, n_points=n_points)
            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[point_lon, point_lat] for point_lat, point_lon in ring]],
                    },
                    "properties": {
                        "horizon_hours": horizon,
                        "radius_km": radius,
                        "coverage": self.coverage,
                        "calibrated": True,
                    },
                }
            )
        return {
            "type": "FeatureCollection",
            "properties": {
                "calibrated_coverage": self.coverage,
                "method": "empirical held-out radial-error quantile",
            },
            "features": features,
        }


def quantile_calibration_report(
    predictions: np.ndarray | torch.Tensor,
    targets: np.ndarray | torch.Tensor,
    quantiles: Sequence[float],
) -> dict[str, Any]:
    """Report interval coverage/width on a calibration set, not final test."""

    pred = (
        predictions.detach().cpu().numpy()
        if isinstance(predictions, torch.Tensor)
        else np.asarray(predictions, dtype=float)
    )
    actual = (
        targets.detach().cpu().numpy()
        if isinstance(targets, torch.Tensor)
        else np.asarray(targets, dtype=float)
    )
    values = tuple(float(value) for value in quantiles)
    if pred.ndim != 4 or actual.shape != pred.shape[:-1]:
        raise ValueError("predictions must be (B,H,2,Q) and targets (B,H,2)")
    if pred.shape[-1] != len(values) or len(values) < 2:
        raise ValueError("quantile dimension must match at least two quantiles")
    if not np.isfinite(pred).all() or not np.isfinite(actual).all():
        raise ValueError("calibration arrays must be finite")
    if tuple(sorted(values)) != values or len(set(values)) != len(values):
        raise ValueError("quantiles must be unique and increasing")
    crossing = np.diff(pred, axis=-1) < 0
    lower = pred[..., 0]
    upper = pred[..., -1]
    covered = (actual >= lower) & (actual <= upper)
    return {
        "lower_quantile": values[0],
        "upper_quantile": values[-1],
        "interval_coverage": covered.mean(axis=(0, 2)).tolist(),
        "mean_width": (upper - lower).mean(axis=(0, 2)).tolist(),
        "crossing_rate": float(crossing.mean()),
        "n_samples": int(pred.shape[0]),
    }
