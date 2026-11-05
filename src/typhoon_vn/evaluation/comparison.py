"""Shared windows, errors and subsets for comparing forecasting methods.

Every method is scored on exactly the same forecast windows: windows are
built once without the scaler (physical units, used by baselines/classical
models) and once with the train-fitted scaler (used by neural models), and
the two are checked to describe identical (storm, issue time) samples.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from typhoon_vn.datasets.typhoon_dataset import DatasetConfig, TyphoonDataset
from typhoon_vn.evaluation.metrics import track_error_km
from typhoon_vn.features.build import FeatureBuilder
from typhoon_vn.features.scaling import FeatureScaler


@dataclass
class Windows:
    x_raw: np.ndarray  # (N, T, F) physical units
    x_scaled: np.ndarray | None  # (N, T, F) train-scaled
    y: np.ndarray  # (N, H, 2) degrees
    storm_ids: np.ndarray
    issue_times: np.ndarray

    def __len__(self) -> int:
        return len(self.y)


def build_windows(
    frame: pd.DataFrame,
    config: DatasetConfig,
    scaler: FeatureScaler | None = None,
) -> Windows:
    raw = TyphoonDataset(frame, config)
    meta = [(s["meta"]["storm_id"], s["meta"]["issue_time"]) for s in raw.samples]
    x_scaled = None
    if scaler is not None:
        scaled = TyphoonDataset(frame, config, scaler=scaler)
        scaled_meta = [
            (s["meta"]["storm_id"], s["meta"]["issue_time"]) for s in scaled.samples
        ]
        if scaled_meta != meta:
            raise RuntimeError("scaled and raw windows are not aligned")
        x_scaled = np.stack([s["x"] for s in scaled.samples])
    return Windows(
        x_raw=np.stack([s["x"] for s in raw.samples]),
        x_scaled=x_scaled,
        y=np.stack([s["y_reg"] for s in raw.samples]),
        storm_ids=np.asarray([m[0] for m in meta]),
        issue_times=np.asarray([m[1] for m in meta], dtype=object),
    )


def errors_km(predicted: np.ndarray, windows: Windows) -> np.ndarray:
    """Great-circle error per window and horizon, shape ``(N, H)``."""

    return np.asarray(track_error_km(predicted, windows.y), dtype=float)


def vietnam_storms(frame: pd.DataFrame, within_km: float = 300.0) -> set[str]:
    """Storms whose track comes within ``within_km`` of Vietnam's coastline."""

    features = FeatureBuilder().transform(frame)
    closest = features.groupby("storm_id")["dist_to_coast_km"].min()
    return set(map(str, closest[closest <= within_km].index))


def summarise(errors: np.ndarray, horizons_h: list[int]) -> dict[str, float]:
    return {
        str(h): float(np.mean(errors[:, index])) for index, h in enumerate(horizons_h)
    }
