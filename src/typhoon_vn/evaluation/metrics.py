"""Track-forecast evaluation metrics.

Implements standard meteorological verification measures: great-circle track
error, along-track / cross-track decomposition, and intensity classification
accuracy by horizon.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np
import torch

from typhoon_vn.features.geo import bearing_change_deg, bearing_deg, destination_point, haversine_km


def _to_numpy(t: torch.Tensor | np.ndarray) -> np.ndarray:
    if isinstance(t, torch.Tensor):
        return t.detach().cpu().numpy()
    return np.asarray(t)


def track_error_km(
    pred: torch.Tensor | np.ndarray,
    actual: torch.Tensor | np.ndarray,
) -> np.ndarray:
    """Great-circle distance between predicted and actual lat/lon positions.

    Inputs shape ``(..., 2)``; output has the same leading shape in kilometres.
    """

    pred = _to_numpy(pred)
    actual = _to_numpy(actual)
    if pred.shape[-1] != 2 or actual.shape[-1] != 2:
        raise ValueError("Last dimension must be (lat, lon)")
    pred_flat = pred.reshape(-1, 2)
    actual_flat = actual.reshape(-1, 2)
    errors = np.array(
        [
            haversine_km(p[0], p[1], a[0], a[1])
            for p, a in zip(pred_flat, actual_flat)
        ]
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

    pred = _to_numpy(pred)
    actual = _to_numpy(actual)
    prev = _to_numpy(prev)

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
    if pred.shape != target.shape:
        pred = np.argmax(pred, axis=-1)
    horizons = pred.shape[1] if pred.ndim > 1 else 1
    if pred.ndim == 1:
        pred = pred.reshape(-1, 1)
        target = target.reshape(-1, 1)
    acc = np.array([np.mean(pred[:, h] == target[:, h]) for h in range(horizons)])
    return acc
