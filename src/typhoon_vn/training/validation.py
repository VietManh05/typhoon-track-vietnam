"""Season-based cross-validation and sequence-length ablation helpers."""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Any

import pandas as pd

from typhoon_vn.contracts.track import DEFAULT_SCHEMA, TrackSchema


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
        raise ValueError(
            "leave-one-season-out validation requires at least two seasons"
        )
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
    evaluate: Callable[[int, tuple[str, ...] | None], dict[str, Any]],
    *,
    seed: int,
    split_id: str,
    budget: str,
) -> list[dict[str, Any]]:
    """Compare lengths on the intersection of identical validation windows."""

    values = list(lengths)
    if not values or any(value < 2 for value in values):
        raise ValueError("sequence lengths must all be at least 2")
    if len(values) != len(set(values)):
        raise ValueError("sequence lengths must be unique")
    if not split_id or not budget:
        raise ValueError("ablation requires a fixed split_id and budget")
    discovered: list[set[str]] = []
    for length in values:
        metrics = evaluate(length, None)
        sample_ids = metrics.get("sample_ids")
        if not sample_ids:
            raise ValueError("ablation discovery must return non-empty sample_ids")
        discovered.append(set(map(str, sample_ids)))
    common = tuple(sorted(set.intersection(*discovered)))
    if not common:
        raise ValueError("sequence lengths have no common validation windows")
    rows = []
    for length in values:
        metrics = evaluate(length, common)
        if set(map(str, metrics.get("sample_ids", ()))) != set(common):
            raise ValueError("ablation evaluator must use exactly the common windows")
        rows.append(
            {
                "sequence_length": length,
                "seed": seed,
                "split_id": split_id,
                "budget": budget,
                "n_available_samples": len(discovered[len(rows)]),
                "n_common_samples": len(common),
                **metrics,
            }
        )
    return rows


def save_ablation_report(path: str | Path, rows: Sequence[dict[str, Any]]) -> Path:
    """Persist the validation-only ablation table with protocol metadata."""

    if not rows:
        raise ValueError("ablation report requires at least one row")
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(
        json.dumps(list(rows), indent=2, sort_keys=True), encoding="utf-8"
    )
    temporary.replace(destination)
    return destination


def default_sequence_lengths() -> Sequence[int]:
    return (4, 6, 8)
