"""Auditable evaluation reports for Phase-3 model comparisons."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def build_case_report(detail: pd.DataFrame, top_n: int = 5) -> dict[str, Any]:
    """Summarise best/worst storms without hiding the per-horizon table."""

    required = {"storm_id", "horizon_h", "track_error_km"}
    missing = sorted(required.difference(detail.columns))
    if missing:
        raise ValueError(f"detail frame is missing columns: {missing}")
    if detail.empty:
        raise ValueError("detail frame must not be empty")
    if top_n < 1:
        raise ValueError("top_n must be positive")

    by_storm = (
        detail.groupby("storm_id", as_index=False)["track_error_km"]
        .agg(["mean", "median", "max", "count"])
        .reset_index()
        .rename(
            columns={
                "mean": "mean_error_km",
                "median": "median_error_km",
                "max": "max_error_km",
                "count": "n_forecasts",
            }
        )
        .sort_values(["mean_error_km", "storm_id"])
    )
    best = by_storm.head(top_n).to_dict(orient="records")
    worst = by_storm.tail(top_n).sort_values("mean_error_km", ascending=False)
    return {
        "n_storms": int(by_storm.shape[0]),
        "n_forecasts": int(detail.shape[0]),
        "best_cases": best,
        "worst_cases": worst.to_dict(orient="records"),
    }


def save_evaluation_report(
    path: str | Path,
    *,
    summary: pd.DataFrame,
    cases: dict[str, Any],
    metadata: dict[str, Any],
) -> Path:
    """Write a stable JSON report with model/data provenance."""

    required_metadata = {"model_name", "dataset_version", "split_policy"}
    missing = sorted(required_metadata.difference(metadata))
    if missing:
        raise ValueError(f"evaluation metadata is missing: {missing}")
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": metadata,
        "summary_by_horizon": summary.to_dict(orient="records"),
        "cases": cases,
    }
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str),
        encoding="utf-8",
    )
    temporary.replace(destination)
    return destination
