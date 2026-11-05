"""Method comparison: residual wrapper, analog k-NN, boosting, shared windows."""

import numpy as np
import pandas as pd
import torch

from typhoon_vn.datasets.synthetic import (
    generate_storm_track,
    generate_synthetic_catalogue,
)
from typhoon_vn.datasets.typhoon_dataset import DatasetConfig
from typhoon_vn.evaluation.comparison import build_windows, errors_km, vietnam_storms
from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.models.base import TrackForecaster
from typhoon_vn.models.classical import (
    AnalogForecaster,
    GradientBoostingForecaster,
    displacement_targets,
)
from typhoon_vn.models.residual import ResidualTrackForecaster

CONFIG = DatasetConfig(feature_cols=tuple(FEATURE_COLUMNS))


class _Zero(TrackForecaster):
    def __init__(self) -> None:
        super().__init__()
        self._n_horizons, self._n_classes = 2, 3

    def forward(self, x, mask=None):
        return {"reg": torch.zeros(x.shape[0], 2, 2), "cls": torch.zeros(1)}


def test_residual_wrapper_anchors_on_last_valid_physical_position() -> None:
    model = ResidualTrackForecaster(_Zero(), [15.0, 120.0], [5.0, 10.0])
    x = torch.zeros(1, 3, 4)
    x[0, 1, :2] = torch.tensor([1.0, -1.0])
    reg = model(x, torch.tensor([[1.0, 1.0, 0.0]]))["reg"]
    assert torch.allclose(reg, torch.tensor([[[20.0, 110.0], [20.0, 110.0]]]))
    assert model.n_horizons == 2 and model.n_classes == 3


def _windows(seed: int = 1, n_storms: int = 6):
    frame = generate_synthetic_catalogue(n_storms=n_storms, n_fixes=24, seed=seed)
    scaler = FeatureScaler(list(FEATURE_COLUMNS)).fit(
        FeatureBuilder().feature_matrix(frame)
    )
    return build_windows(frame, CONFIG, scaler)


def test_windows_are_aligned_and_targets_physical() -> None:
    windows = _windows()
    assert windows.x_raw.shape == windows.x_scaled.shape
    assert len(windows) == len(windows.storm_ids) == len(windows.issue_times)
    assert np.abs(windows.y[..., 0]).max() > 5  # degrees, not z-scores
    assert np.abs(windows.x_scaled[..., 0]).max() < 5


def test_analog_with_k1_reuses_the_matching_historical_case() -> None:
    windows = _windows()
    model = AnalogForecaster(k=1).fit(
        windows.x_raw, windows.y, windows.storm_ids, windows.issue_times
    )
    prediction = model.predict(windows.x_raw[:3])
    assert np.allclose(prediction, windows.y[:3], atol=1e-4)
    explanation = model.explain(windows.x_raw[:1], top=1)[0]
    assert explanation[0]["storm_id"] == windows.storm_ids[0]
    assert explanation[0]["distance"] < 1e-3


def test_analog_steering_columns_with_nan_add_no_distance() -> None:
    windows = _windows()
    steering = np.random.default_rng(0).normal(size=(*windows.x_raw.shape[:2], 2))
    steering[::2] = np.nan  # half the library has no reanalysis coverage
    x_raw = np.concatenate([windows.x_raw, steering], axis=2)
    model = AnalogForecaster(
        k=1, weights={"track": 1.0, "position": 1.0, "season": 0.5, "steering": 1.0}
    ).fit(x_raw, windows.y, windows.storm_ids, windows.issue_times)
    prediction = model.predict(x_raw[:4])
    assert np.isfinite(prediction).all()
    assert np.allclose(prediction, windows.y[:4], atol=1e-4)
    assert model.explain(x_raw[:1], top=1)[0][0]["distance"] < 1e-3


def test_analog_explain_lists_distinct_storms() -> None:
    windows = _windows(n_storms=8)
    model = AnalogForecaster(k=30).fit(
        windows.x_raw, windows.y, windows.storm_ids, windows.issue_times
    )
    names = [item["storm_id"] for item in model.explain(windows.x_raw[:1], top=4)[0]]
    assert len(names) == len(set(names)) >= 2


def test_boosting_learns_motion_better_than_standing_still() -> None:
    train, test = _windows(seed=1, n_storms=10), _windows(seed=2, n_storms=4)
    model = GradientBoostingForecaster(max_iter=60).fit(train.x_raw, train.y)
    predicted = model.predict(test.x_raw)
    assert predicted.shape == test.y.shape
    still = test.x_raw[:, -1, None, :2].repeat(test.y.shape[1], axis=1)
    assert (
        errors_km(predicted, test)[:, -1].mean() < errors_km(still, test)[:, -1].mean()
    )
    assert np.allclose(
        displacement_targets(test.x_raw, test.y) + test.x_raw[:, -1, None, :2], test.y
    )


def test_vietnam_subset_uses_distance_to_vietnam_coast() -> None:
    near = generate_storm_track("NEAR", n_fixes=8).assign(lat=16.0, lon=109.0)
    far = generate_storm_track("FAR", n_fixes=8).assign(lat=20.0, lon=138.0)
    frame = pd.concat([near, far], ignore_index=True)
    assert vietnam_storms(frame, within_km=300) == {"NEAR"}
