"""Validation-only Optuna search with a sealed final-test boundary."""

from __future__ import annotations

import json
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


@dataclass(frozen=True, slots=True)
class SearchSpace:
    hidden_size: tuple[int, ...]
    num_layers: tuple[int, ...]
    dropout: tuple[float, ...]
    learning_rate: tuple[float, ...]
    batch_size: tuple[int, ...]
    sequence_length: tuple[int, ...] = (4, 6, 8)
    horizon_weights: tuple[tuple[float, ...], ...] = ((1.0,),)

    def __post_init__(self) -> None:
        values = (
            self.hidden_size,
            self.num_layers,
            self.dropout,
            self.learning_rate,
            self.batch_size,
            self.sequence_length,
            self.horizon_weights,
        )
        if any(not value for value in values):
            raise ValueError("search-space dimensions must be non-empty")
        if any(
            value < 1 for value in self.hidden_size + self.num_layers + self.batch_size
        ):
            raise ValueError("integer search-space values must be positive")
        if any(value not in {4, 6, 8} for value in self.sequence_length):
            raise ValueError("sequence_length search is limited to 4, 6, and 8")


@dataclass(slots=True)
class SearchResult:
    best_params: dict[str, Any]
    best_validation_score: float
    trials: list[dict[str, Any]]
    seed: int
    final_test_metrics: dict[str, float] | None = None
    test_evaluations: int = 0

    def record_final_test(self, metrics: dict[str, float]) -> None:
        if self.test_evaluations:
            raise RuntimeError("final test may be evaluated exactly once")
        if not metrics or not all(np.isfinite(value) for value in metrics.values()):
            raise ValueError("final-test metrics must be finite and non-empty")
        self.final_test_metrics = {key: float(value) for key, value in metrics.items()}
        self.test_evaluations = 1

    def save(self, path: str | Path) -> Path:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(
                {
                    "best_params": self.best_params,
                    "best_validation_score": self.best_validation_score,
                    "trials": self.trials,
                    "seed": self.seed,
                    "final_test_metrics": self.final_test_metrics,
                    "test_evaluations": self.test_evaluations,
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        return destination


def run_search(
    search_space: SearchSpace,
    *,
    folds: Sequence[Any],
    objective: Callable[[dict[str, Any], Any], float],
    n_trials: int,
    seed: int,
) -> SearchResult:
    """Minimise mean fold validation score; the callback never receives test data."""

    if n_trials < 1:
        raise ValueError("n_trials must be positive")
    if not folds:
        raise ValueError("at least one validation fold is required")
    try:
        import optuna
    except ImportError as exc:
        raise RuntimeError("Optuna tuning requires the training extra") from exc

    sampler = optuna.samplers.RandomSampler(seed=seed)
    study = optuna.create_study(direction="minimize", sampler=sampler)

    def evaluate_trial(trial: Any) -> float:
        params = {
            "hidden_size": trial.suggest_categorical(
                "hidden_size", list(search_space.hidden_size)
            ),
            "num_layers": trial.suggest_categorical(
                "num_layers", list(search_space.num_layers)
            ),
            "dropout": trial.suggest_categorical("dropout", list(search_space.dropout)),
            "learning_rate": trial.suggest_categorical(
                "learning_rate", list(search_space.learning_rate)
            ),
            "batch_size": trial.suggest_categorical(
                "batch_size", list(search_space.batch_size)
            ),
            "sequence_length": trial.suggest_categorical(
                "sequence_length", list(search_space.sequence_length)
            ),
            "horizon_weights_index": trial.suggest_int(
                "horizon_weights_index", 0, len(search_space.horizon_weights) - 1
            ),
        }
        params["horizon_weights"] = list(
            search_space.horizon_weights[params.pop("horizon_weights_index")]
        )
        scores = [float(objective(dict(params), fold)) for fold in folds]
        if not scores or not np.isfinite(scores).all():
            raise ValueError("tuning objective must return finite fold scores")
        trial.set_user_attr("fold_scores", scores)
        trial.set_user_attr("resolved_params", params)
        return float(np.mean(scores))

    study.optimize(evaluate_trial, n_trials=n_trials)
    trials = [
        {
            "number": trial.number,
            "validation_score": trial.value,
            "params": trial.user_attrs["resolved_params"],
            "fold_scores": trial.user_attrs["fold_scores"],
        }
        for trial in study.trials
    ]
    best = study.best_trial
    return SearchResult(
        best_params=dict(best.user_attrs["resolved_params"]),
        best_validation_score=float(best.value),
        trials=trials,
        seed=seed,
    )
