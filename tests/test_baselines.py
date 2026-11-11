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
    assert output[:, 1].tolist() == pytest.approx(
        [-177.0, -175.0, -171.0, -163.0, -155.0]
    )
    assert torch.all((output[:, 1] >= -180.0) & (output[:, 1] <= 180.0))


def test_persistence_uses_last_two_valid_masked_positions() -> None:
    model = PersistenceForecaster(1, 3, horizon_steps=[1])
    x = torch.tensor([[[10.0, 100.0], [11.0, 101.0], [99.0, 99.0]]])
    mask = torch.tensor([[1.0, 1.0, 0.0]])
    assert model(x, mask)["reg"][0, 0].tolist() == pytest.approx([12.0, 102.0])

    with pytest.raises(ValueError, match="two valid"):
        model(x, torch.tensor([[1.0, 0.0, 0.0]]))


def test_climatology_baseline_is_train_only_serializable_and_dateline_safe(
    tmp_path,
) -> None:
    timestamps = pd.date_range("2025-01-01", periods=14, freq="6h", tz="UTC")
    frame = pd.DataFrame(
        {
            "storm_id": ["A"] * len(timestamps),
            "timestamp": timestamps,
            "lat": np.arange(len(timestamps), dtype=float),
            "lon": [
                ((179.0 + 2 * index + 180) % 360) - 180
                for index in range(len(timestamps))
            ],
        }
    )
    baseline = ClimatologyPersistenceBaseline.fit(frame)
    forecast = baseline.predict(np.array([[0.0, 179.0], [1.0, -179.0]]))
    assert np.all((forecast[:, 1] >= -180.0) & (forecast[:, 1] <= 180.0))

    path = baseline.save(tmp_path / "baseline.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["method"] == "train-only climatology residual + persistence"
    assert ClimatologyPersistenceBaseline.load(path) == baseline


@pytest.mark.parametrize(
    "positions, mask, current, hourly_motion",
    [
        (
            [[10.0, 100.0], [10.0, 100.0], [10.0, 100.0]],
            [1, 1, 1],
            [10.0, 100.0],
            [0.0, 0.0],
        ),
        (
            [[10.0, 100.0], [11.0, 101.0], [12.0, 102.0]],
            [1, 1, 1],
            [12.0, 102.0],
            [1 / 6, 1 / 6],
        ),
        (
            [[10.0, 100.0], [0.0, 0.0], [12.0, 102.0]],
            [1, 0, 1],
            [12.0, 102.0],
            [1 / 6, 1 / 6],
        ),
        (
            [[10.0, 179.0], [0.0, 0.0], [12.0, -179.0]],
            [1, 0, 1],
            [12.0, -179.0],
            [1 / 6, 1 / 6],
        ),
        (
            [[10.0, -179.0], [0.0, 0.0], [12.0, 179.0]],
            [1, 0, 1],
            [12.0, 179.0],
            [1 / 6, -1 / 6],
        ),
    ],
)
def test_persistence_elapsed_time_contract(
    positions, mask, current, hourly_motion
) -> None:
    model = PersistenceForecaster(5, 7, horizon_steps=HORIZONS)
    output = model(torch.tensor([positions]), torch.tensor([mask]))
    # Independent velocity in degrees/hour, integrated over forecast hours.
    hours = np.array([6, 12, 24, 48, 72])
    expected = np.array(current) + hours[:, None] * np.array(hourly_motion)
    expected[:, 1] = (expected[:, 1] + 180) % 360 - 180
    np.testing.assert_allclose(output["reg"][0].numpy(), expected, atol=1e-5)
    assert output["cls"].shape == (1, 5, 7)


def test_persistence_batch_uses_each_samples_elapsed_time() -> None:
    model = PersistenceForecaster(1, 3, horizon_steps=[1])
    x = torch.tensor(
        [
            [[10.0, 100.0], [0.0, 0.0], [12.0, 102.0]],
            [[0.0, 0.0], [11.0, 101.0], [12.0, 102.0]],
        ]
    )
    output = model(x, torch.tensor([[1, 0, 1], [0, 1, 1]]))["reg"]
    torch.testing.assert_close(
        output[:, 0], torch.tensor([[13.0, 103.0], [13.0, 103.0]])
    )


def test_damped_persistence_preserves_elapsed_time() -> None:
    from typhoon_vn.models.baselines import CLIPERForecaster

    model = CLIPERForecaster(1, 3, horizon_steps=[1])
    x = torch.tensor([[[10.0, 100.0], [0.0, 0.0], [12.0, 102.0]]])
    result = model(x, torch.tensor([[1, 0, 1]]))["reg"][0, 0]
    torch.testing.assert_close(result, torch.tensor([12.92, 102.92]))
