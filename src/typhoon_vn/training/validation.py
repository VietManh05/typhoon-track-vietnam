"""Season-based cross-validation and sequence-length ablation helpers."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from typing import Any

import pandas as pd

from typhoon_vn.features.schema import DEFAULT_SCHEMA, TrackSchema


def leave_one_season_out_splits(
    frame: pd.DataFrame,
    *,
    schema: TrackSchema | None = None,
) -> list[tuple[int, pd.DataFrame, pd.DataFrame]]:
    """Yield whole-storm folds keyed by each storm's final observed year."""

    schema = schema or DEFAULT_SCHEMA
    data = frame.copy()
    data[schema.timestamp] = pd.to_datetime(data[schema.timestamp], utc=True)
    data["_season"] = (
        data.groupby(schema.storm_id)[schema.timestamp].transform("max").dt.year
    )
    seasons = sorted(int(value) for value in data["_season"].unique())
    if len(seasons) < 2:
        raise ValueError("leave-one-season-out validation requires at least two seasons")
    folds: list[tuple[int, pd.DataFrame, pd.DataFrame]] = []
    for season in seasons:
        validation = data[data["_season"] == season].drop(columns="_season")
        training = data[data["_season"] != season].drop(columns="_season")
        train_ids = set(training[schema.storm_id])
        validation_ids = set(validation[schema.storm_id])
        if train_ids & validation_ids:
            raise RuntimeError("storm leakage detected across seasonal fold")
        folds.append(
            (season, training.reset_index(drop=True), validation.reset_index(drop=True))
        )
    return folds


def run_sequence_length_ablation(
    lengths: Iterable[int],
    evaluate: Callable[[int], dict[str, float]],
) -> list[dict[str, Any]]:
    """Evaluate a fixed protocol for each unique sequence length."""

    values = list(lengths)
    if not values or any(value < 2 for value in values):
        raise ValueError("sequence lengths must all be at least 2")
    if len(values) != len(set(values)):
        raise ValueError("sequence lengths must be unique")
    rows = []
    for length in values:
        metrics = evaluate(length)
        if not metrics:
            raise ValueError("ablation evaluation must return metrics")
        rows.append({"sequence_length": length, **metrics})
    return rows


def default_sequence_lengths() -> Sequence[int]:
    return (4, 6, 8)
