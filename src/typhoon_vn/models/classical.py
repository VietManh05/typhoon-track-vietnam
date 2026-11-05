"""Classical (non-neural) track forecasters on raw-feature windows.

* :class:`AnalogForecaster` — k-nearest-neighbour "analog" forecasting
  (case-based reasoning): find historical storm situations whose recent track,
  location and season look most like the current one, and suggest the
  displacements those storms actually made next. Each forecast can name the
  analog storms it relied on, which makes the suggestion explainable.
* :class:`GradientBoostingForecaster` — gradient-boosted trees regressing the
  displacement at every horizon from the flattened input window.

Both work on windows built *without* the feature scaler (physical units) and
predict displacement in degrees from the last observed position.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neighbors import NearestNeighbors

from typhoon_vn.features.build import FEATURE_COLUMNS

_COL = {name: index for index, name in enumerate(FEATURE_COLUMNS)}


def anchors(x_raw: np.ndarray) -> np.ndarray:
    """Last observed (lat, lon) of each window, shape ``(N, 2)``."""

    return x_raw[:, -1, :2].astype(float)


def displacement_targets(x_raw: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Future positions minus the anchor, shape ``(N, H, 2)`` in degrees."""

    return y.astype(float) - anchors(x_raw)[:, None, :]


def analog_features(x_raw: np.ndarray) -> dict[str, np.ndarray]:
    """Feature groups for analog matching (before standardisation)."""

    anchor = anchors(x_raw)
    coslat = np.cos(np.radians(anchor[:, 0]))[:, None]
    relative = x_raw[:, :-1, :2].astype(float) - anchor[:, None, :]
    relative[..., 1] *= coslat  # degrees of longitude -> comparable distance
    return {
        "track": relative.reshape(len(x_raw), -1),
        "position": anchor,
        "season": x_raw[:, -1, [_COL["month_sin"], _COL["month_cos"]]].astype(float),
    }


@dataclass
class AnalogForecaster:
    """Inverse-distance weighted k-NN over historical storm windows."""

    k: int = 20
    weights: dict[str, float] = field(
        default_factory=lambda: {"track": 1.0, "position": 1.0, "season": 0.5}
    )

    def fit(
        self,
        x_raw: np.ndarray,
        y: np.ndarray,
        storm_ids: Sequence[str],
        issue_times: Sequence[object],
    ) -> "AnalogForecaster":
        if len(x_raw) < self.k:
            raise ValueError("analog library is smaller than k")
        groups = analog_features(x_raw)
        self._scale = {
            name: values.std(axis=0) + 1e-6 for name, values in groups.items()
        }
        self._mean = {name: values.mean(axis=0) for name, values in groups.items()}
        self._targets = displacement_targets(x_raw, y)
        self._storm_ids = np.asarray(storm_ids)
        self._issue_times = np.asarray(issue_times, dtype=object)
        self._index = NearestNeighbors(n_neighbors=self.k).fit(self._embed(groups))
        return self

    def _embed(self, groups: dict[str, np.ndarray]) -> np.ndarray:
        parts = []
        for name, values in groups.items():
            standardised = (values - self._mean[name]) / self._scale[name]
            # Normalise each group by its width so weights compare groups.
            width = np.sqrt(values.shape[1])
            parts.append(self.weights.get(name, 0.0) * standardised / width)
        return np.hstack(parts)

    def _neighbours(self, x_raw: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        return self._index.kneighbors(self._embed(analog_features(x_raw)))

    def predict(self, x_raw: np.ndarray) -> np.ndarray:
        """Forecast positions ``(N, H, 2)`` in degrees."""

        distance, index = self._neighbours(x_raw)
        weight = 1.0 / (distance + 1e-6)
        weight /= weight.sum(axis=1, keepdims=True)
        displacement = np.einsum("nk,nkhc->nhc", weight, self._targets[index])
        return anchors(x_raw)[:, None, :] + displacement

    def explain(self, x_raw: np.ndarray, top: int = 5) -> list[list[dict]]:
        """Name the historical analogs behind each forecast (closest first)."""

        distance, index = self._neighbours(x_raw)
        result = []
        for row_distance, row_index in zip(distance, index):
            seen: list[dict] = []
            for d, i in zip(row_distance, row_index):
                storm = str(self._storm_ids[i])
                if any(item["storm_id"] == storm for item in seen):
                    continue
                seen.append(
                    {
                        "storm_id": storm,
                        "issue_time": str(self._issue_times[i]),
                        "distance": float(d),
                    }
                )
                if len(seen) == top:
                    break
            result.append(seen)
        return result


def boosting_features(x_raw: np.ndarray) -> np.ndarray:
    """Flattened window plus analog-style relative track features."""

    groups = analog_features(x_raw)
    return np.hstack([x_raw.reshape(len(x_raw), -1).astype(float), groups["track"]])


@dataclass
class GradientBoostingForecaster:
    max_iter: int = 300
    learning_rate: float = 0.05
    max_leaf_nodes: int = 31
    random_state: int = 0

    def fit(self, x_raw: np.ndarray, y: np.ndarray) -> "GradientBoostingForecaster":
        targets = displacement_targets(x_raw, y)
        self._shape = targets.shape[1:]
        self._model = MultiOutputRegressor(
            HistGradientBoostingRegressor(
                max_iter=self.max_iter,
                learning_rate=self.learning_rate,
                max_leaf_nodes=self.max_leaf_nodes,
                early_stopping=False,
                random_state=self.random_state,
            )
        ).fit(boosting_features(x_raw), targets.reshape(len(targets), -1))
        return self

    def predict(self, x_raw: np.ndarray) -> np.ndarray:
        flat = self._model.predict(boosting_features(x_raw))
        return anchors(x_raw)[:, None, :] + flat.reshape(len(x_raw), *self._shape)
