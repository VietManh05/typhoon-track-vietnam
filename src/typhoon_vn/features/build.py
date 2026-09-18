"""Feature engineering: motion, time, coast, intensity (WBS 4.x).

All builders consume the *cleaned* track table and return new columns only;
``FeatureBuilder`` assembles them into the official feature list so training
and serving share one code path.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from typhoon_vn.features import constants as C
from typhoon_vn.features.geo import bearing_change_deg, bearing_deg, haversine_km
from typhoon_vn.features.schema import TrackSchema

SCHEMA = TrackSchema()


def _cyclic(value: pd.Series, period: float) -> tuple[pd.Series, pd.Series]:
    angle = 2.0 * math.pi * value.astype(float) / period
    return np.sin(angle), np.cos(angle)


def add_motion_features(
    df: pd.DataFrame, schema: TrackSchema | None = None
) -> pd.DataFrame:
    """Per-storm kinematics: step distance, bearing, speed, accel, turning."""

    schema = schema or TrackSchema()
    out = df.copy()
    for col, default in (
        ("step_km", 0.0),
        ("bearing_deg", 0.0),
        ("speed_kmh", 0.0),
        ("accel_kmh2", 0.0),
        ("bearing_change_deg", 0.0),
        ("turn_rate_deg_per_h", 0.0),
    ):
        out[col] = default

    for _, group in out.groupby(schema.storm_id, sort=False):
        idx = group.sort_values(schema.timestamp).index.tolist()
        prev_bearing: float | None = None
        prev_speed: float | None = None
        # Index of the last *accepted* fix; duplicate-timestamp rows are never
        # used as a reference so one bad fix cannot contaminate the next step.
        prev: int | None = None
        for i in idx:
            if prev is None:
                prev = i
                continue
            lat0 = float(out.at[prev, schema.lat])
            lon0 = float(out.at[prev, schema.lon])
            lat1 = float(out.at[i, schema.lat])
            lon1 = float(out.at[i, schema.lon])
            step = haversine_km(lat0, lon0, lat1, lon1)
            bearing = bearing_deg(lat0, lon0, lat1, lon1)
            dt_h = (
                out.at[i, schema.timestamp] - out.at[prev, schema.timestamp]
            ).total_seconds() / 3600.0
            if not math.isfinite(dt_h) or dt_h <= 0.0:
                # Duplicate or out-of-order timestamps make the elapsed time
                # undefined. Leave this row at its neutral defaults and keep
                # ``prev``/``prev_speed``/``prev_bearing`` on the last real fix
                # instead of silently dividing by a fabricated 6 h interval and
                # injecting wrong speed/accel/turn values into the model.
                continue
            speed = step / dt_h
            out.at[i, "step_km"] = step
            out.at[i, "bearing_deg"] = bearing
            out.at[i, "speed_kmh"] = speed
            if prev_speed is not None:
                out.at[i, "accel_kmh2"] = (speed - prev_speed) / dt_h
            if prev_bearing is not None:
                turn = bearing_change_deg(prev_bearing, bearing)
                out.at[i, "bearing_change_deg"] = turn
                out.at[i, "turn_rate_deg_per_h"] = turn / dt_h
            prev = i
            prev_bearing, prev_speed = bearing, speed

    out["bearing_sin"], out["bearing_cos"] = _cyclic(out["bearing_deg"], 360.0)
    return out


def add_lag_features(
    df: pd.DataFrame, schema: TrackSchema | None = None, n_lags: int = 3
) -> pd.DataFrame:
    """Lagged lat/lon/deltas inside each storm (no cross-storm leakage)."""

    schema = schema or TrackSchema()
    out = df.copy()
    out["dlat"] = out.groupby(schema.storm_id)[schema.lat].diff().fillna(0.0)
    out["dlon"] = out.groupby(schema.storm_id)[schema.lon].diff().fillna(0.0)
    for lag in range(1, n_lags + 1):
        lat_lag = out.groupby(schema.storm_id)[schema.lat].shift(lag)
        out[f"lat_lag{lag}"] = lat_lag.fillna(out[schema.lat])
        lon_lag = out.groupby(schema.storm_id)[schema.lon].shift(lag)
        out[f"lon_lag{lag}"] = lon_lag.fillna(out[schema.lon])
    return out


def add_time_features(
    df: pd.DataFrame, schema: TrackSchema | None = None
) -> pd.DataFrame:
    """Calendar + cyclic encodings + Vietnam-season flag."""

    schema = schema or TrackSchema()
    out = df.copy()
    ts = pd.to_datetime(out[schema.timestamp], utc=True)
    out["hour"] = ts.dt.hour.astype(float)
    out["day"] = ts.dt.day.astype(float)
    out["month"] = ts.dt.month.astype(float)
    out["dayofyear"] = ts.dt.dayofyear.astype(float)
    out["hour_sin"], out["hour_cos"] = _cyclic(out["hour"], 24.0)
    out["day_sin"], out["day_cos"] = _cyclic(out["day"], 31.0)
    out["month_sin"], out["month_cos"] = _cyclic(out["month"], 12.0)
    out["doy_sin"], out["doy_cos"] = _cyclic(out["dayofyear"], 366.0)
    out["in_season"] = out["month"].isin(sorted(C.SEASON_MONTHS)).astype(float)
    return out


def _nearest_coast_point(lat: float, lon: float) -> tuple[float, float, float]:
    """Return ``(distance_km, bearing_deg, coast_index)`` to the VN coastline."""

    best = (math.inf, 0.0, -1)
    for k, (clat, clon) in enumerate(C.VN_COASTLINE):
        dist = haversine_km(lat, lon, clat, clon)
        if dist < best[0]:
            best = (dist, bearing_deg(lat, lon, clat, clon), k)
    return best


def add_coast_features(
    df: pd.DataFrame, schema: TrackSchema | None = None
) -> pd.DataFrame:
    """Distance/bearing to the Vietnam coastline + reference-point distances."""

    schema = schema or TrackSchema()
    out = df.copy()
    dists: list[float] = []
    bearings: list[float] = []
    for lat, lon in zip(out[schema.lat].astype(float), out[schema.lon].astype(float)):
        dist, bearing, _ = _nearest_coast_point(float(lat), float(lon))
        dists.append(dist)
        bearings.append(bearing)
    out["dist_to_coast_km"] = dists
    out["bearing_to_coast_deg"] = bearings
    out["coast_bearing_sin"], out["coast_bearing_cos"] = _cyclic(
        out["bearing_to_coast_deg"], 360.0
    )
    for name, (rlat, rlon) in C.REFERENCE_POINTS.items():
        out[f"dist_to_{name}_km"] = [
            haversine_km(float(lat), float(lon), rlat, rlon)
            for lat, lon in zip(
                out[schema.lat].astype(float), out[schema.lon].astype(float)
            )
        ]
    return out


def add_intensity_features(
    df: pd.DataFrame, schema: TrackSchema | None = None
) -> pd.DataFrame:
    """Wind/pressure changes + fixed-list one-hot intensity categories."""

    schema = schema or TrackSchema()
    out = df.copy()
    out["wind_change_ms"] = (
        out.groupby(schema.storm_id)[schema.wind_ms].diff().fillna(0.0)
    )
    out["pressure_change_hpa"] = (
        out.groupby(schema.storm_id)[schema.pressure_hpa].diff().fillna(0.0)
    )
    labels = out[schema.intensity].astype(str).str.upper()
    labels = labels.where(labels.isin(C.INTENSITY_CATEGORIES), "UNK")
    for cat in C.INTENSITY_CATEGORIES:
        out[f"intensity_{cat}"] = (labels == cat).astype(float)
    return out


#: Official model-ready feature list (fixed order, WBS 4.8 data dictionary).
FEATURE_COLUMNS: tuple[str, ...] = (
    "lat",
    "lon",
    "dlat",
    "dlon",
    "lat_lag1",
    "lon_lag1",
    "lat_lag2",
    "lon_lag2",
    "lat_lag3",
    "lon_lag3",
    "step_km",
    "bearing_deg",
    "bearing_sin",
    "bearing_cos",
    "speed_kmh",
    "accel_kmh2",
    "bearing_change_deg",
    "turn_rate_deg_per_h",
    "dist_to_coast_km",
    "bearing_to_coast_deg",
    "coast_bearing_sin",
    "coast_bearing_cos",
    *[f"dist_to_{name}_km" for name in C.REFERENCE_POINTS],
    "hour_sin",
    "hour_cos",
    "day_sin",
    "day_cos",
    "month_sin",
    "month_cos",
    "doy_sin",
    "doy_cos",
    "in_season",
    "wind_ms",
    "pressure_hpa",
    "wind_change_ms",
    "pressure_change_hpa",
    *[f"intensity_{cat}" for cat in C.INTENSITY_CATEGORIES],
)


class FeatureBuilder:
    """Assemble the full feature table with one reusable ``transform``."""

    def __init__(self, n_lags: int = 3) -> None:
        self.n_lags = n_lags

    @property
    def feature_columns(self) -> list[str]:
        return list(FEATURE_COLUMNS)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out = add_lag_features(out, SCHEMA, n_lags=self.n_lags)
        out = add_motion_features(out, SCHEMA)
        out = add_time_features(out, SCHEMA)
        out = add_coast_features(out, SCHEMA)
        out = add_intensity_features(out, SCHEMA)
        return out

    def feature_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return only the model-ready columns in canonical order."""

        return self.transform(df)[self.feature_columns]


__all__ = [
    "FEATURE_COLUMNS",
    "FeatureBuilder",
    "add_coast_features",
    "add_intensity_features",
    "add_lag_features",
    "add_motion_features",
    "add_time_features",
]
