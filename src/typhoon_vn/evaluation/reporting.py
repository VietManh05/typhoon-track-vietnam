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

    required_metadata = {
        "model_version",
        "dataset_version",
        "split_policy",
        "run_id",
        "checkpoint_sha256",
    }
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


def save_track_error_plot(path: str | Path, summary: pd.DataFrame) -> Path:
    """Write a dependency-free SVG of mean track error by horizon."""

    required = {"horizon_h", "mean_error_km"}
    missing = sorted(required.difference(summary.columns))
    if missing:
        raise ValueError(f"summary frame is missing columns: {missing}")
    if summary.empty:
        raise ValueError("summary frame must not be empty")
    values = summary.sort_values("horizon_h")
    if (values["mean_error_km"] < 0).any():
        raise ValueError("track errors must be non-negative")
    width, height, margin = 640, 360, 50
    maximum = max(float(values["mean_error_km"].max()), 1.0)
    step = (width - 2 * margin) / max(len(values) - 1, 1)
    points = []
    labels = []
    for index, row in enumerate(values.to_dict(orient="records")):
        x = margin + index * step
        y = (
            height
            - margin
            - float(row["mean_error_km"]) / maximum * (height - 2 * margin)
        )
        points.append(f"{x:.1f},{y:.1f}")
        labels.append(
            f'<text x="{x:.1f}" y="{height - 20}" text-anchor="middle">{int(row["horizon_h"])}h</text>'
        )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
        '<rect width="100%" height="100%" fill="white"/>'
        f'<polyline fill="none" stroke="#1261a0" stroke-width="3" points="{" ".join(points)}"/>'
        + "".join(labels)
        + '<text x="20" y="20">Mean track error (km)</text></svg>'
    )
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(svg, encoding="utf-8")
    temporary.replace(destination)
    return destination
