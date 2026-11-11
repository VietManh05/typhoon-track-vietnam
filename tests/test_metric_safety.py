"""Safety and edge-case contracts for evaluation metrics."""

import numpy as np
import pytest
import torch

from typhoon_vn.evaluation.metrics import (
    intensity_accuracy,
    regression_mae,
    regression_rmse,
)


@pytest.mark.parametrize(
    ("metric", "expected"),
    [
        (regression_mae, [1.0, 2.5]),
        (regression_rmse, [1.0, np.sqrt(6.5)]),
    ],
)
def test_regression_metrics_normal_values(metric, expected) -> None:
    pred = np.array([[2.0, 1.0], [4.0, -1.0]])
    actual = np.array([[1.0, 3.0], [3.0, 2.0]])
    np.testing.assert_allclose(metric(pred, actual), expected)


@pytest.mark.parametrize("metric", [regression_mae, regression_rmse])
def test_regression_metrics_identical_negative_values(metric) -> None:
    values = np.array([[-5.0, -1.5], [-2.0, -8.0]])
    np.testing.assert_array_equal(metric(values, values), np.zeros(2))


@pytest.mark.parametrize("metric", [regression_mae, regression_rmse])
def test_regression_metrics_accept_singleton_and_trailing_scalar_dimension(
    metric,
) -> None:
    pred = torch.tensor([[[-3.0]]])
    actual = torch.tensor([[[-5.0]]])
    np.testing.assert_allclose(metric(pred, actual), [2.0])


@pytest.mark.parametrize("metric", [regression_mae, regression_rmse])
def test_regression_metrics_reject_empty_inputs(metric) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        metric(np.empty((0, 2)), np.empty((0, 2)))


@pytest.mark.parametrize("metric", [regression_mae, regression_rmse])
@pytest.mark.parametrize("invalid", [np.nan, np.inf, -np.inf])
def test_regression_metrics_reject_all_invalid_inputs(metric, invalid) -> None:
    values = np.full((2, 2), invalid)
    with pytest.raises(ValueError, match="must be finite"):
        metric(values, values)


@pytest.mark.parametrize("metric", [regression_mae, regression_rmse])
@pytest.mark.parametrize("invalid", [np.nan, np.inf])
def test_regression_metrics_reject_mixed_finite_and_invalid_inputs(
    metric, invalid
) -> None:
    pred = np.array([[1.0, invalid], [2.0, 3.0]])
    actual = np.ones((2, 2))
    with pytest.raises(ValueError, match="must be finite"):
        metric(pred, actual)


@pytest.mark.parametrize("metric", [regression_mae, regression_rmse])
def test_regression_metrics_reject_shape_mismatch(metric) -> None:
    with pytest.raises(ValueError, match="shapes must match"):
        metric(np.ones((2, 1)), np.ones((1, 2)))


@pytest.mark.parametrize("metric", [regression_mae, regression_rmse])
def test_regression_metrics_reject_non_horizon_shapes(metric) -> None:
    with pytest.raises(ValueError, match=r"shape \(B, H\)"):
        metric(np.ones(2), np.ones(2))


@pytest.mark.parametrize(
    ("pred", "target", "message"),
    [
        (np.empty((0, 2)), np.empty((0, 2)), "must not be empty"),
        (np.array([[0.0, np.nan]]), np.array([[0.0, 1.0]]), "must be finite"),
        (np.array([[0.0, np.inf]]), np.array([[0.0, 1.0]]), "must be finite"),
        (np.zeros((2, 1)), np.zeros((1, 2)), "compatible shapes"),
    ],
)
def test_intensity_accuracy_rejects_unsafe_inputs(pred, target, message) -> None:
    with pytest.raises(ValueError, match=message):
        intensity_accuracy(pred, target)
