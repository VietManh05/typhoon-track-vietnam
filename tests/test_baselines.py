"""Contracts for classical Phase-3 baselines."""

import json

import numpy as np
import pandas as pd
import pytest
import torch

from typhoon_vn.models.baselines import (
    ClimatologyPersistenceBaseline,
    PersistenceForecaster,
)


HORIZONS = [1, 2, 4, 8, 12]


def test_persistence_uses_short_dateline_motion_and_wraps_outputs() -> None:
    model = PersistenceForecaster(5, 7, horizon_steps=HORIZONS)
    x = torch.tensor([[[10.0, 179.0], [11.0, -179.0]]])
    output = model(x)["reg"][0]

    assert output[:, 0].tolist() == pytest.approx([12.0, 13.0, 15.0, 19.0, 23.0])
    assert output[:, 1].tolist() == pytest.approx([-177.0, -175.0, -171.0, -163.0, -155.0])
    assert torch.all((output[:, 1] >= -180.0) & (output[:, 1] <= 180.0))


def test_persistence_uses_last_two_valid_masked_positions() -> None:
    model = PersistenceForecaster(1, 3, horizon_steps=[1])
    x = torch.tensor([[[10.0, 100.0], [11.0, 101.0], [99.0, 99.0]]])
    mask = torch.tensor([[1.0, 1.0, 0.0]])
    assert model(x, mask)["reg"][0, 0].tolist() == pytest.approx([12.0, 102.0])

    with pytest.raises(ValueError, match="two valid"):
        model(x, torch.tensor([[1.0, 0.0, 0.0]]))


def test_climatology_baseline_is_train_only_serializable_and_dateline_safe(tmp_path) -> None:
    timestamps = pd.date_range("2025-01-01", periods=14, freq="6h", tz="UTC")
    frame = pd.DataFrame(
        {
            "storm_id": ["A"] * len(timestamps),
            "timestamp": timestamps,
            "lat": np.arange(len(timestamps), dtype=float),
            "lon": [((179.0 + 2 * index + 180) % 360) - 180 for index in range(len(timestamps))],
        }
    )
    baseline = ClimatologyPersistenceBaseline.fit(frame)
    forecast = baseline.predict(np.array([[0.0, 179.0], [1.0, -179.0]]))
    assert np.all((forecast[:, 1] >= -180.0) & (forecast[:, 1] <= 180.0))

    path = baseline.save(tmp_path / "baseline.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["method"] == "train-only climatology residual + persistence"
    assert ClimatologyPersistenceBaseline.load(path) == baseline
