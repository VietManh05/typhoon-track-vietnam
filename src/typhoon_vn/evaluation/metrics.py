"""Track-forecast evaluation metrics.

Implements standard meteorological verification measures: great-circle track
error, along-track / cross-track decomposition, and intensity classification
accuracy by horizon.
"""

from __future__ import annotations

import math

import numpy as np
import torch

from typhoon_vn.features.geo import bearing_change_deg, bearing_deg, haversine_km


def _to_numpy(t: torch.Tensor | np.ndarray) -> np.ndarray:
    if isinstance(t, torch.Tensor):
        return t.detach().cpu().numpy()
    return np.asarray(t)


def _matching_arrays(
    pred: torch.Tensor | np.ndarray,
    actual: torch.Tensor | np.ndarray,
    *,
    last_size: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    pred_array = _to_numpy(pred)
    actual_array = _to_numpy(actual)
    if pred_array.shape != actual_array.shape:
        raise ValueError("prediction and target shapes must match")
    if last_size is not None and (
        pred_array.ndim == 0 or pred_array.shape[-1] != last_size
    ):
        raise ValueError(f"last dimension must have size {last_size}")
    if not np.isfinite(pred_array).all() or not np.isfinite(actual_array).all():
        raise ValueError("prediction and target values must be finite")
    return pred_array, actual_array


def track_error_km(
    pred: torch.Tensor | np.ndarray,
    actual: torch.Tensor | np.ndarray,
) -> np.ndarray:
    """Great-circle distance between predicted and actual lat/lon positions.

    Inputs shape ``(..., 2)``; output has the same leading shape in kilometres.
    """

    pred, actual = _matching_arrays(pred, actual, last_size=2)
    pred_flat = pred.reshape(-1, 2)
    actual_flat = actual.reshape(-1, 2)
    errors = np.array(
        [haversine_km(p[0], p[1], a[0], a[1]) for p, a in zip(pred_flat, actual_flat)]
    )
    return errors.reshape(pred.shape[:-1])


def along_cross_track_errors(
    pred: torch.Tensor | np.ndarray,
    actual: torch.Tensor | np.ndarray,
    prev: torch.Tensor | np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Decompose track error into along-track and cross-track components.

    ``prev`` is the position before the verification point; the along-track
    axis is the bearing from ``prev`` to ``actual``.
    """

    pred, actual = _matching_arrays(pred, actual, last_size=2)
    prev = _to_numpy(prev)
    if prev.shape != pred.shape or not np.isfinite(prev).all():
        raise ValueError("previous positions must be finite and match track shape")

    def components(p, a, pr):
        bearing_pa = bearing_deg(pr[0], pr[1], a[0], a[1])
        # Project pred onto the along-track axis from prev
        dist_pr_p = haversine_km(pr[0], pr[1], p[0], p[1])
        bearing_pr_p = bearing_deg(pr[0], pr[1], p[0], p[1])
        deviation = bearing_change_deg(bearing_pa, bearing_pr_p)
        # Cross-track is roughly the lateral deviation; along-track is the
        # difference in distance along the true bearing.
        dist_pr_a = haversine_km(pr[0], pr[1], a[0], a[1])
        cross = dist_pr_p * math.sin(math.radians(deviation))
        along = dist_pr_p * math.cos(math.radians(deviation)) - dist_pr_a
        return along, cross

    pred_flat = pred.reshape(-1, 2)
    actual_flat = actual.reshape(-1, 2)
    prev_flat = prev.reshape(-1, 2)
    along_list: list[float] = []
    cross_list: list[float] = []
    for p, a, pr in zip(pred_flat, actual_flat, prev_flat):
        al, cr = components(p, a, pr)
        along_list.append(al)
        cross_list.append(cr)
    shape = pred.shape[:-1]
    return np.array(along_list).reshape(shape), np.array(cross_list).reshape(shape)


def intensity_accuracy(
    pred_cls: torch.Tensor | np.ndarray,
    target_cls: torch.Tensor | np.ndarray,
) -> np.ndarray:
    """Per-horizon classification accuracy.

    Inputs shape ``(B, H)`` of class indices; output shape ``(H,)``.
    """

    pred = _to_numpy(pred_cls)
    target = _to_numpy(target_cls)
    if pred.ndim == target.ndim + 1:
        pred = np.argmax(pred, axis=-1)
    if pred.shape != target.shape:
        raise ValueError("class predictions and targets must have compatible shapes")
    horizons = pred.shape[1] if pred.ndim > 1 else 1
    if pred.ndim == 1:
        pred = pred.reshape(-1, 1)
        target = target.reshape(-1, 1)
    acc = np.array([np.mean(pred[:, h] == target[:, h]) for h in range(horizons)])
    return acc


def regression_mae(
    pred: torch.Tensor | np.ndarray,
    actual: torch.Tensor | np.ndarray,
) -> np.ndarray:
    """Per-horizon mean absolute error for scalar intensity variables."""

    pred_array, actual_array = _matching_arrays(pred, actual)
    if pred_array.ndim == 3 and pred_array.shape[-1] == 1:
        pred_array = pred_array[..., 0]
        actual_array = actual_array[..., 0]
    if pred_array.ndim != 2:
        raise ValueError("scalar regression inputs must have shape (B, H) or (B, H, 1)")
    return np.mean(np.abs(pred_array - actual_array), axis=0)


def intensity_classification_scores(
    pred_cls: torch.Tensor | np.ndarray,
    target_cls: torch.Tensor | np.ndarray,
    *,
    n_classes: int | None = None,
) -> dict[str, np.ndarray]:
    """Return per-horizon accuracy and macro precision/recall/F1."""

    pred = _to_numpy(pred_cls)
    target = _to_numpy(target_cls)
    if pred.ndim == target.ndim + 1:
        inferred_classes = pred.shape[-1]
        pred = np.argmax(pred, axis=-1)
    else:
        inferred_classes = int(max(pred.max(initial=0), target.max(initial=0))) + 1
    if pred.shape != target.shape:
        raise ValueError("class predictions and targets must have compatible shapes")
    if pred.ndim == 1:
        pred = pred[:, None]
        target = target[:, None]
    if pred.ndim != 2:
        raise ValueError("class inputs must resolve to shape (B, H)")
    class_count = n_classes or inferred_classes
    if class_count < 1:
        raise ValueError("n_classes must be positive")

    accuracy: list[float] = []
    precision: list[float] = []
    recall: list[float] = []
    f1: list[float] = []
    for horizon in range(pred.shape[1]):
        p_h = pred[:, horizon]
        t_h = target[:, horizon]
        accuracy.append(float(np.mean(p_h == t_h)))
        per_class: list[tuple[float, float, float]] = []
        for class_id in range(class_count):
            true_positive = np.sum((p_h == class_id) & (t_h == class_id))
            false_positive = np.sum((p_h == class_id) & (t_h != class_id))
            false_negative = np.sum((p_h != class_id) & (t_h == class_id))
            p_score = float(true_positive / (true_positive + false_positive)) if (
                true_positive + false_positive
            ) else 0.0
            r_score = float(true_positive / (true_positive + false_negative)) if (
                true_positive + false_negative
            ) else 0.0
            f_score = (
                2 * p_score * r_score / (p_score + r_score)
                if p_score + r_score
                else 0.0
            )
            per_class.append((p_score, r_score, f_score))
        precision.append(float(np.mean([value[0] for value in per_class])))
        recall.append(float(np.mean([value[1] for value in per_class])))
        f1.append(float(np.mean([value[2] for value in per_class])))
    return {
        "accuracy": np.asarray(accuracy),
        "precision_macro": np.asarray(precision),
        "recall_macro": np.asarray(recall),
        "f1_macro": np.asarray(f1),
    }
