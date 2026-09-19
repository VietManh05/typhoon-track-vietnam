"""Backtesting helpers for post-hoc model evaluation.

Provides two main functions:

* ``backtest_storm`` — runs rolling-window forecasts across all valid anchor
  points of a single storm and returns a tidy DataFrame of predicted vs actual
  positions.
* ``backtest_catalogue`` — runs ``backtest_storm`` over a collection of storms
  and aggregates track-error metrics by forecast horizon.

These helpers are intentionally dependency-light (no DB, no API) so they can
be used in notebooks, CI jobs, and offline reporting.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

from typhoon_vn.datasets.typhoon_dataset import (
    DatasetConfig,
    TyphoonDataset,
    collate_fn,
)
from typhoon_vn.evaluation.metrics import along_cross_track_errors, track_error_km
from typhoon_vn.features.schema import DEFAULT_SCHEMA, TrackSchema
from typhoon_vn.models.base import TrackForecaster


def backtest_storm(
    model: TrackForecaster,
    storm_df: pd.DataFrame,
    config: DatasetConfig | None = None,
    schema: TrackSchema | None = None,
    device: str | torch.device = "cpu",
    batch_size: int = 64,
) -> pd.DataFrame:
    """Run rolling-window inference over all valid anchor points of one storm.

    Args:
        model: trained ``TrackForecaster`` (set to eval mode inside).
        storm_df: observations for a **single** storm (must contain schema columns).
        config: dataset config (window size, horizons).  Defaults to the standard
            4-step / 5-horizon setup.
        schema: column name mapping.
        device: PyTorch device for inference.
        batch_size: mini-batch size (tune for GPU memory).

    Returns:
        DataFrame with columns:
        ``storm_id``, ``issue_time``, ``horizon_h``,
        ``pred_lat``, ``pred_lon``, ``actual_lat``, ``actual_lon``,
        ``track_error_km``.
        Returns an empty DataFrame if the storm has too few observations.
    """
    if config is None:
        config = DatasetConfig()
    schema = schema or DEFAULT_SCHEMA
    device = torch.device(device) if isinstance(device, str) else device

    ds = TyphoonDataset(storm_df, config=config, schema=schema)
    if len(ds) == 0:
        return pd.DataFrame()

    loader = DataLoader(ds, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)
    model.eval()
    model.to(device)

    records: list[dict[str, Any]] = []
    h_steps = list(config.horizon)
    h_hours = [h * config.time_step_hours for h in h_steps]
    source = storm_df.copy()
    source[schema.timestamp] = pd.to_datetime(source[schema.timestamp], utc=True)
    issue_positions = {
        pd.Timestamp(row[schema.timestamp]): (
            float(row[schema.lat]),
            float(row[schema.lon]),
        )
        for _, row in source.iterrows()
    }

    with torch.no_grad():
        for batch in loader:
            x = batch["x"].to(device)
            mask = batch["mask"].to(device)
            y_reg = batch["y_reg"].cpu().numpy()  # (B, H, 2)
            y_cls = batch["y_cls"].cpu().numpy()
            out = model(x, mask)
            pred_reg = out["reg"].cpu().numpy()  # (B, H, 2)
            pred_cls = out["cls"].argmax(dim=-1).cpu().numpy()
            errors = track_error_km(pred_reg, y_reg)  # (B, H)

            metas = batch["meta"]
            for i, meta in enumerate(metas):
                issue_time = pd.Timestamp(meta["issue_time"])
                origin = np.asarray(issue_positions[issue_time], dtype=float)
                for j, (hours, step) in enumerate(zip(h_hours, h_steps)):
                    along, cross = along_cross_track_errors(
                        pred_reg[i, j][None, :],
                        y_reg[i, j][None, :],
                        origin[None, :],
                    )
                    records.append(
                        {
                            "storm_id": meta["storm_id"],
                            "issue_time": issue_time,
                            "horizon_h": int(hours),
                            "pred_lat": float(pred_reg[i, j, 0]),
                            "pred_lon": float(pred_reg[i, j, 1]),
                            "actual_lat": float(y_reg[i, j, 0]),
                            "actual_lon": float(y_reg[i, j, 1]),
                            "track_error_km": float(errors[i, j]),
                            "along_track_error_km": float(along[0]),
                            "cross_track_error_km": float(cross[0]),
                            "pred_intensity_class": int(pred_cls[i, j]),
                            "actual_intensity_class": int(y_cls[i, j]),
                        }
                    )

    return pd.DataFrame(records)


def backtest_catalogue(
    model: TrackForecaster,
    df: pd.DataFrame,
    config: DatasetConfig | None = None,
    schema: TrackSchema | None = None,
    device: str | torch.device = "cpu",
    batch_size: int = 64,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run backtest over all storms in ``df`` and aggregate metrics.

    Args:
        model: trained ``TrackForecaster``.
        df: full catalogue DataFrame (multiple storms).
        config: dataset config.
        schema: column name mapping.
        device: PyTorch device.
        batch_size: inference batch size.

    Returns:
        Tuple of:
        - ``detail_df``: per-forecast-point results (same schema as
          ``backtest_storm`` output), concatenated across all storms.
        - ``summary_df``: per-horizon aggregated metrics with columns
          ``horizon_h``, ``mean_error_km``, ``median_error_km``,
          ``rmse_km``, ``p90_km``, ``n_forecasts``.
    """
    if config is None:
        config = DatasetConfig()
    schema = schema or DEFAULT_SCHEMA

    storm_ids = df[schema.storm_id].unique()
    all_frames: list[pd.DataFrame] = []

    for sid in storm_ids:
        storm_df = df[df[schema.storm_id] == sid].reset_index(drop=True)
        result = backtest_storm(
            model,
            storm_df,
            config=config,
            schema=schema,
            device=device,
            batch_size=batch_size,
        )
        if not result.empty:
            all_frames.append(result)

    if not all_frames:
        return pd.DataFrame(), pd.DataFrame()

    detail_df = pd.concat(all_frames, ignore_index=True)

    # Aggregate per horizon
    summary_records: list[dict[str, Any]] = []
    for h, group in detail_df.groupby("horizon_h"):
        errs = group["track_error_km"].values
        summary_records.append(
            {
                "horizon_h": int(h),
                "mean_error_km": float(np.mean(errs)),
                "median_error_km": float(np.median(errs)),
                "rmse_km": float(np.sqrt(np.mean(errs**2))),
                "p90_km": float(np.percentile(errs, 90)),
                "mean_along_track_error_km": float(
                    np.mean(group["along_track_error_km"])
                ),
                "mean_cross_track_error_km": float(
                    np.mean(group["cross_track_error_km"])
                ),
                "intensity_accuracy": float(
                    np.mean(
                        group["pred_intensity_class"]
                        == group["actual_intensity_class"]
                    )
                ),
                "n_forecasts": len(errs),
            }
        )
    summary_df = (
        pd.DataFrame(summary_records).sort_values("horizon_h").reset_index(drop=True)
    )

    return detail_df, summary_df
