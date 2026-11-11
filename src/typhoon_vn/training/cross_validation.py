"""Leakage-safe leave-one-season-out folds with train-only scalers."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

import pandas as pd

from typhoon_vn.features.build import FEATURE_COLUMNS
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.features.schema import DEFAULT_SCHEMA, TrackSchema
from typhoon_vn.training.validation import leave_one_season_out_splits


@dataclass(frozen=True, slots=True)
class SeasonalFold:
    """One validation season and its independently fitted preprocessing state."""

    season: int
    training: pd.DataFrame
    validation: pd.DataFrame
    scaler: FeatureScaler
    scaler_fingerprint: str
    train_ids: tuple[str, ...]
    validation_ids: tuple[str, ...]


def _fingerprint_scaler(scaler: FeatureScaler) -> str:
    payload = {
        "features": scaler.feature_columns,
        "fill": scaler._fill_values.tolist(),
        "mean": scaler._scaler.mean_.tolist(),
        "scale": scaler._scaler.scale_.tolist(),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def build_seasonal_folds(
    frame: pd.DataFrame,
    *,
    feature_columns: tuple[str, ...] = tuple(FEATURE_COLUMNS),
    schema: TrackSchema | None = None,
    sealed_test_ids: tuple[str, ...] = (),
) -> list[SeasonalFold]:
    """Build whole-storm folds and fit a fresh scaler on each training fold."""

    schema = schema or DEFAULT_SCHEMA
    sealed = set(map(str, sealed_test_ids))
    data = frame[~frame[schema.storm_id].astype(str).isin(sealed)].copy()
    if data.empty:
        raise ValueError("seasonal validation has no data outside sealed final test")
    missing = sorted(set(feature_columns).difference(frame.columns))
    if missing:
        raise ValueError(f"seasonal validation is missing features: {missing}")
    result: list[SeasonalFold] = []
    for season, training, validation in leave_one_season_out_splits(
        data, schema=schema
    ):
        scaler = FeatureScaler(list(feature_columns)).fit(
            training[list(feature_columns)]
        )
        train_ids = tuple(sorted(map(str, training[schema.storm_id].unique())))
        validation_ids = tuple(sorted(map(str, validation[schema.storm_id].unique())))
        if set(train_ids) & set(validation_ids):
            raise RuntimeError("storm leakage detected after scaler fitting")
        result.append(
            SeasonalFold(
                season=season,
                training=training,
                validation=validation,
                scaler=scaler,
                scaler_fingerprint=_fingerprint_scaler(scaler),
                train_ids=train_ids,
                validation_ids=validation_ids,
            )
        )
    return result
