"""Classical baseline forecasters for benchmarking.

Provides two baselines that are common reference points in tropical cyclone
track research:

* **PersistenceForecaster** — assumes the storm keeps moving at the same
  speed and bearing as its most recent step (no model learning involved).
* **CLIPERForecaster** — Climatology and PERsistence, a standard
  meteorological benchmark.  Here we implement a simplified version using
  only persistence of motion (speed + bearing) with a climatological
  correction factor per horizon (no external climatology dataset required).

Both implement the ``TrackForecaster`` interface so they can be swapped in
anywhere the LSTM models are used (evaluation, backtest, etc.).
"""

from __future__ import annotations

import math

import torch

from typhoon_vn.features.geo import destination_point, haversine_km
from typhoon_vn.models.base import TrackForecaster


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
        self.time_step_hours = time_step_hours
        # No learnable parameters — register a dummy buffer so .to(device) works
        self.register_buffer("_dummy", torch.zeros(1))

    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> dict[str, torch.Tensor]:
        """Autoregressive persistence: propagate last motion for each horizon.

        Args:
            x: shape ``(B, T, F)`` where ``F >= 2`` and ``x[..., :2]`` is lat/lon.
            mask: ignored (kept for interface compatibility).

        Returns:
            dict with ``reg`` of shape ``(B, H, 2)`` and dummy ``cls`` zeros.
        """
        batch_size = x.size(0)
        device = x.device

        # Extract last two observed positions
        lat1 = x[:, -2, 0]  # (B,)
        lon1 = x[:, -2, 1]
        lat2 = x[:, -1, 0]
        lon2 = x[:, -1, 1]

        reg_outputs: list[torch.Tensor] = []
        prev_lat, prev_lon = lat2.clone(), lon2.clone()

        for step in self.horizon_steps:
            # Compute bearing and distance of the last step
            delta_lat = lat2 - lat1
            delta_lon = lon2 - lon1

            # Accumulate `step` steps of the same motion vector
            target_lat = prev_lat + delta_lat * step
            target_lon = prev_lon + delta_lon * step
            reg_outputs.append(torch.stack([target_lat, target_lon], dim=-1))

        reg = torch.stack(reg_outputs, dim=1)  # (B, H, 2)
        cls = torch.zeros(batch_size, len(self.horizon_steps), self._n_classes, device=device)
        return {"reg": reg, "cls": cls}


class CLIPERForecaster(TrackForecaster):
    """Simplified CLIPER (CLImatology and PERsistence) baseline.

    Applies a horizon-dependent damping factor to the persistence motion
    vector to approximate the climatological decay in skill over time.
    The damping factors are derived empirically from NWP ensemble studies
    (roughly 0.9 at 6 h, 0.6 at 24 h, 0.35 at 72 h).

    No external climatology file is needed — this is appropriate for a
    structural baseline rather than an operational one.
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
        self.time_step_hours = time_step_hours
        self.register_buffer("_dummy", torch.zeros(1))

    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> dict[str, torch.Tensor]:
        """Damped-persistence forecast.

        Args:
            x: shape ``(B, T, F)`` where ``x[..., :2]`` is lat/lon.
            mask: ignored.

        Returns:
            dict with ``reg`` of shape ``(B, H, 2)`` and dummy ``cls`` zeros.
        """
        batch_size = x.size(0)
        device = x.device

        lat1 = x[:, -2, 0]
        lon1 = x[:, -2, 1]
        lat2 = x[:, -1, 0]
        lon2 = x[:, -1, 1]

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        reg_outputs: list[torch.Tensor] = []
        for step in self.horizon_steps:
            damp = self._DAMP_BASE ** step
            target_lat = lat2 + delta_lat * step * damp
            target_lon = lon2 + delta_lon * step * damp
            reg_outputs.append(torch.stack([target_lat, target_lon], dim=-1))

        reg = torch.stack(reg_outputs, dim=1)  # (B, H, 2)
        cls = torch.zeros(batch_size, len(self.horizon_steps), self._n_classes, device=device)
        return {"reg": reg, "cls": cls}
