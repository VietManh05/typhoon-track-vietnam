"""Classical baseline forecasters for benchmarking.

Provides two baselines that are common reference points in tropical cyclone
track research:

* **PersistenceForecaster** — assumes the storm keeps moving at the same
  speed and bearing as its most recent step (no model learning involved).
* **CLIPERForecaster** — a clearly labelled damped-persistence proxy.  It is
  not presented as an operational CLIPER implementation.

Both implement the ``TrackForecaster`` interface so they can be swapped in
anywhere the LSTM models are used (evaluation, backtest, etc.).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from typhoon_vn.models.base import TrackForecaster


def _wrap_longitude_tensor(longitude: torch.Tensor) -> torch.Tensor:
    return torch.remainder(longitude + 180.0, 360.0) - 180.0


def _wrap_longitude_array(longitude: np.ndarray) -> np.ndarray:
    return np.remainder(longitude + 180.0, 360.0) - 180.0


def _last_two_positions(
    x: torch.Tensor, mask: torch.Tensor | None
) -> tuple[torch.Tensor, torch.Tensor]:
    if x.ndim != 3 or x.shape[1] < 2 or x.shape[2] < 2:
        raise ValueError("x must have shape (B, T>=2, F>=2)")
    if not torch.isfinite(x[..., :2]).all():
        raise ValueError("baseline coordinates must be finite")
    if mask is None:
        return x[:, -2, :2], x[:, -1, :2]
    if mask.shape != x.shape[:2]:
        raise ValueError("mask must have shape (B, T)")
    valid = mask.to(dtype=torch.bool)
    if (valid.sum(dim=1) < 2).any():
        raise ValueError("each baseline input requires at least two valid positions")
    indices = torch.arange(x.shape[1], device=x.device).expand(x.shape[0], -1)
    ranked = indices.masked_fill(~valid, -1).topk(2, dim=1).values.sort(dim=1).values
    batch = torch.arange(x.shape[0], device=x.device).unsqueeze(1)
    selected = x[batch, ranked, :2]
    return selected[:, 0], selected[:, 1]


class PersistenceForecaster(TrackForecaster):
    """Predict future positions by persisting the last observed motion vector.

    Assumes:
    - First two features of ``x`` are lat/lon (degrees).
    - The step between consecutive observations is ``time_step_hours`` hours.
    - ``horizon_steps`` is the list of horizon step indices (same as
      ``DatasetConfig.horizon``).

    This is the simplest meaningful baseline for track forecasting.
    """

    def __init__(
        self,
        n_horizons: int,
        n_classes: int,
        horizon_steps: list[int] | None = None,
        time_step_hours: float = 6.0,
    ) -> None:
        super().__init__()
        self._n_horizons = n_horizons
        self._n_classes = n_classes
        # Default: 6h, 12h, 24h, 48h, 72h expressed as 6h steps
        self.horizon_steps: list[int] = horizon_steps or [1, 2, 4, 8, 12]
        if len(self.horizon_steps) != n_horizons:
            raise ValueError("horizon_steps length must equal n_horizons")
        if any(step <= 0 for step in self.horizon_steps):
            raise ValueError("horizon_steps must be positive")
        self.time_step_hours = time_step_hours
        # No learnable parameters — register a dummy buffer so .to(device) works
        self.register_buffer("_dummy", torch.zeros(1))

    def forward(
        self, x: torch.Tensor, mask: torch.Tensor | None = None
    ) -> dict[str, torch.Tensor]:
        """Autoregressive persistence: propagate last motion for each horizon.

        Args:
            x: shape ``(B, T, F)`` where ``F >= 2`` and ``x[..., :2]`` is lat/lon.
            mask: ignored (kept for interface compatibility).

        Returns:
            dict with ``reg`` of shape ``(B, H, 2)`` and dummy ``cls`` zeros.
        """
        batch_size = x.size(0)
        device = x.device
        previous, current = _last_two_positions(x, mask)
        lat1, lon1 = previous.unbind(dim=-1)
        lat2, lon2 = current.unbind(dim=-1)

        reg_outputs: list[torch.Tensor] = []
        for step in self.horizon_steps:
            # Compute bearing and distance of the last step
            delta_lat = lat2 - lat1
            delta_lon = _wrap_longitude_tensor(lon2 - lon1)

            # Accumulate `step` steps of the same motion vector
            target_lat = lat2 + delta_lat * step
            target_lon = _wrap_longitude_tensor(lon2 + delta_lon * step)
            reg_outputs.append(torch.stack([target_lat, target_lon], dim=-1))

        reg = torch.stack(reg_outputs, dim=1)  # (B, H, 2)
        cls = torch.zeros(
            batch_size, len(self.horizon_steps), self._n_classes, device=device
        )
        return {"reg": reg, "cls": cls}


class CLIPERForecaster(TrackForecaster):
    """Simplified CLIPER (CLImatology and PERsistence) baseline.

    This is intentionally labelled a *damped persistence proxy*, not an
    operational CLIPER implementation: it does not claim published CLIPER
    coefficients or skill.  Use :class:`ClimatologyPersistenceBaseline` below
    when a train-only catalogue is available.
    """

    # Damping factors per horizon step index (6-h units: 1→0.9, 2→0.82, …)
    # Fit to approximate JTWC CLIPER5 skill decline curve.
    _DAMP_BASE: float = 0.92

    def __init__(
        self,
        n_horizons: int,
        n_classes: int,
        horizon_steps: list[int] | None = None,
        time_step_hours: float = 6.0,
    ) -> None:
        super().__init__()
        self._n_horizons = n_horizons
        self._n_classes = n_classes
        self.horizon_steps: list[int] = horizon_steps or [1, 2, 4, 8, 12]
        if len(self.horizon_steps) != n_horizons:
            raise ValueError("horizon_steps length must equal n_horizons")
        if any(step <= 0 for step in self.horizon_steps):
            raise ValueError("horizon_steps must be positive")
        self.time_step_hours = time_step_hours
        self.register_buffer("_dummy", torch.zeros(1))

    def forward(
        self, x: torch.Tensor, mask: torch.Tensor | None = None
    ) -> dict[str, torch.Tensor]:
        """Damped-persistence forecast.

        Args:
            x: shape ``(B, T, F)`` where ``x[..., :2]`` is lat/lon.
            mask: ignored.

        Returns:
            dict with ``reg`` of shape ``(B, H, 2)`` and dummy ``cls`` zeros.
        """
        batch_size = x.size(0)
        device = x.device
        previous, current = _last_two_positions(x, mask)
        lat1, lon1 = previous.unbind(dim=-1)
        lat2, lon2 = current.unbind(dim=-1)

        delta_lat = lat2 - lat1
        delta_lon = _wrap_longitude_tensor(lon2 - lon1)

        reg_outputs: list[torch.Tensor] = []
        for step in self.horizon_steps:
            damp = self._DAMP_BASE**step
            target_lat = lat2 + delta_lat * step * damp
            target_lon = _wrap_longitude_tensor(lon2 + delta_lon * step * damp)
            reg_outputs.append(torch.stack([target_lat, target_lon], dim=-1))

        reg = torch.stack(reg_outputs, dim=1)  # (B, H, 2)
        cls = torch.zeros(
            batch_size, len(self.horizon_steps), self._n_classes, device=device
        )
        return {"reg": reg, "cls": cls}


@dataclass(frozen=True, slots=True)
class ClimatologyPersistenceBaseline:
    """Train-only mean residual correction on top of motion persistence."""

    horizon_steps: tuple[int, ...]
    residual_lat_lon: tuple[tuple[float, float], ...]
    time_step_hours: int = 6

    @classmethod
    def fit(
        cls,
        frame: pd.DataFrame,
        *,
        horizon_steps: tuple[int, ...] = (1, 2, 4, 8, 12),
        time_step_hours: int = 6,
    ) -> "ClimatologyPersistenceBaseline":
        required = {"storm_id", "timestamp", "lat", "lon"}
        if not required.issubset(frame.columns):
            raise ValueError(f"baseline frame missing columns: {sorted(required - set(frame))}")
        corrections: dict[int, list[np.ndarray]] = {step: [] for step in horizon_steps}
        delta = pd.Timedelta(hours=time_step_hours)
        for _, group in frame.groupby("storm_id", sort=False):
            ordered = group.sort_values("timestamp").copy()
            ordered["timestamp"] = pd.to_datetime(ordered["timestamp"], utc=True)
            lookup = ordered.set_index("timestamp")[["lat", "lon"]]
            for index in range(1, len(ordered)):
                previous = ordered.iloc[index - 1][["lat", "lon"]].to_numpy(float)
                current = ordered.iloc[index][["lat", "lon"]].to_numpy(float)
                issue = ordered.iloc[index]["timestamp"]
                motion = current - previous
                motion[1] = _wrap_longitude_array(np.asarray(motion[1]))
                for step in horizon_steps:
                    target_time = issue + delta * step
                    if target_time not in lookup.index:
                        continue
                    target = lookup.loc[target_time].to_numpy(float)
                    predicted = current + motion * step
                    residual = target - predicted
                    residual[1] = _wrap_longitude_array(np.asarray(residual[1]))
                    corrections[step].append(residual)
        residuals = []
        for step in horizon_steps:
            if not corrections[step]:
                raise ValueError(f"no training samples for horizon step {step}")
            residuals.append(tuple(np.mean(corrections[step], axis=0).tolist()))
        return cls(tuple(horizon_steps), tuple(residuals), time_step_hours)

    def predict(self, recent_positions: np.ndarray) -> np.ndarray:
        positions = np.asarray(recent_positions, dtype=float)
        if positions.shape != (2, 2) or not np.isfinite(positions).all():
            raise ValueError("recent_positions must be finite shape (2, 2)")
        motion = positions[1] - positions[0]
        motion[1] = _wrap_longitude_array(np.asarray(motion[1]))
        forecast = np.asarray(
            [
                positions[1] + motion * step + np.asarray(residual)
                for step, residual in zip(self.horizon_steps, self.residual_lat_lon)
            ]
        )
        forecast[:, 1] = _wrap_longitude_array(forecast[:, 1])
        return forecast

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "method": "train-only climatology residual + persistence",
                    "horizon_steps": self.horizon_steps,
                    "residual_lat_lon": self.residual_lat_lon,
                    "time_step_hours": self.time_step_hours,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return path

    @classmethod
    def load(cls, path: str | Path) -> "ClimatologyPersistenceBaseline":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            tuple(payload["horizon_steps"]),
            tuple(tuple(item) for item in payload["residual_lat_lon"]),
            int(payload["time_step_hours"]),
        )
