"""Calibration and uncertainty contracts for Phase 3."""

import numpy as np
import pytest
import torch

from typhoon_vn.models.lstm import LSTMTrackForecaster
from typhoon_vn.models.uncertainty import (
    CalibratedCone,
    DeepEnsemble,
    quantile_calibration_report,
)


def test_calibrated_cone_round_trip_and_geojson(tmp_path) -> None:
    errors = np.array([[10, 20], [20, 30], [30, 40], [40, 50]], dtype=float)
    cone = CalibratedCone.fit(errors, [6, 12], coverage=0.75)
    restored = CalibratedCone.load(cone.save(tmp_path / "cone.json"))
    assert restored == cone
    geojson = restored.to_geojson([(10.0, 179.5), (11.0, -179.5)], n_points=8)
    assert geojson["properties"]["calibrated_coverage"] == 0.75
    polygons = [f for f in geojson["features"] if f["geometry"]["type"] == "Polygon"]
    assert len(polygons) == 2
    assert (
        polygons[0]["geometry"]["coordinates"][0][0]
        == polygons[0]["geometry"]["coordinates"][0][-1]
    )


def test_quantile_calibration_reports_coverage_width_and_crossing() -> None:
    targets = np.array([[[0.0, 0.0]], [[1.0, 1.0]]])
    predictions = np.array(
        [
            [[[-1.0, 0.0, 1.0], [-1.0, 0.0, 1.0]]],
            [[[0.0, 1.0, 2.0], [0.0, 1.0, 2.0]]],
        ]
    )
    report = quantile_calibration_report(predictions, targets, (0.1, 0.5, 0.9))
    assert report["interval_coverage"] == pytest.approx([1.0])
    assert report["mean_width"] == pytest.approx([2.0])
    assert report["crossing_rate"] == 0.0


def test_deep_ensemble_rejects_member_contract_mismatch() -> None:
    first = LSTMTrackForecaster(3, 2, 4, hidden_size=4, num_layers=1)
    second = LSTMTrackForecaster(3, 3, 4, hidden_size=4, num_layers=1)
    third = LSTMTrackForecaster(3, 2, 4, hidden_size=4, num_layers=1)
    with pytest.raises(ValueError, match="contract"):
        DeepEnsemble([first, second, third])


def test_mc_dropout_activates_lstm_dropout_and_restores_mode() -> None:
    from typhoon_vn.models.uncertainty import mc_dropout_predict

    model = LSTMTrackForecaster(
        3, 2, 4, hidden_size=8, num_layers=2, dropout=0.5
    ).train()
    result = mc_dropout_predict(
        model, torch.randn(2, 4, 3), torch.ones(2, 4), n_samples=8
    )
    assert torch.any(result["reg_std"] > 0)
    assert model.training is True


def test_deep_ensemble_requires_three_versioned_members_and_restores_modes() -> None:
    models = [
        LSTMTrackForecaster(3, 2, 4, hidden_size=4, num_layers=1).train()
        for _ in range(3)
    ]
    ensemble = DeepEnsemble(models, member_versions=("seed-1", "seed-2", "seed-3"))
    ensemble.predict(torch.randn(1, 4, 3), torch.ones(1, 4))
    assert all(model.training for model in models)
    with pytest.raises(ValueError, match="at least three"):
        DeepEnsemble(models[:2])


def test_attention_rejects_fully_masked_sequence() -> None:
    from typhoon_vn.models.lstm import AttentionLSTMTrackForecaster

    model = AttentionLSTMTrackForecaster(3, 2, 4, hidden_size=4, num_layers=1)
    with pytest.raises(ValueError, match="valid timestep"):
        model(torch.zeros(1, 4, 3), torch.zeros(1, 4))
