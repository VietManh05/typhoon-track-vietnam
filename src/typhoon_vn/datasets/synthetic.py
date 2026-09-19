"""Synthetic typhoon tracks for unit tests and quick demos.

Generates physically plausible 6-hourly fixes so Phase-3 model code can be
run and tested without waiting for real ingestion data.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

from typhoon_vn.features.geo import destination_point
from typhoon_vn.features.schema import DEFAULT_SCHEMA


def _sample_intensity(wind_ms: float) -> str:
    if wind_ms < 17.0:
        return "TD"
    if wind_ms < 25.0:
        return "TS"
    if wind_ms < 33.0:
        return "STS"
    if wind_ms < 44.0:
        return "TY"
    if wind_ms < 55.0:
        return "STY"
    return "SUPERTY"


def generate_storm_track(
    storm_id: str,
    n_fixes: int = 40,
    start_lat: float = 12.0,
    start_lon: float = 125.0,
    start_time: datetime | None = None,
    seed: int | None = None,
) -> pd.DataFrame:
    """Create a single synthetic storm track."""

    rng = np.random.default_rng(seed)
    if start_time is None:
        start_time = datetime(2020, 7, 1, tzinfo=timezone.utc)

    lats, lons, winds, pressures, intensities, timestamps = [], [], [], [], [], []
    lat, lon = start_lat, start_lon
    bearing = 285.0  # WNW
    speed_kmh = 15.0
    wind = 25.0
    pressure = 990.0

    for i in range(n_fixes):
        timestamps.append(start_time + timedelta(hours=6 * i))
        lats.append(lat)
        lons.append(lon)
        winds.append(wind)
        pressures.append(pressure)
        intensities.append(_sample_intensity(wind))

        # Random walk for dynamics
        bearing += rng.normal(0, 8)
        bearing = bearing % 360
        speed_kmh = max(5.0, min(60.0, speed_kmh + rng.normal(0, 3)))
        step_km = speed_kmh * 6.0 / 24.0  # 6-hourly step in km (assuming daily avg)
        lat, lon = destination_point(lat, lon, bearing, step_km)
        wind = max(10.0, min(80.0, wind + rng.normal(0, 3)))
        pressure = max(900.0, min(1005.0, 1010.0 - 0.6 * wind + rng.normal(0, 2)))

    schema = DEFAULT_SCHEMA
    return pd.DataFrame(
        {
            schema.storm_id: [storm_id] * n_fixes,
            schema.timestamp: timestamps,
            schema.lat: lats,
            schema.lon: lons,
            schema.wind_ms: winds,
            schema.pressure_hpa: pressures,
            schema.intensity: intensities,
            schema.end_flag: ["ONGOING"] * (n_fixes - 1) + ["END"],
            schema.source: ["SYNTHETIC"] * n_fixes,
            schema.interpolated: [False] * n_fixes,
            schema.suspicious: [False] * n_fixes,
        }
    )


def generate_synthetic_catalogue(
    n_storms: int = 30,
    n_fixes: int = 40,
    start_year: int = 2015,
    seed: int = 42,
) -> pd.DataFrame:
    """Create a catalogue of synthetic storms across several years."""

    rng = np.random.default_rng(seed)
    frames: list[pd.DataFrame] = []
    for i in range(n_storms):
        year = start_year + (i % 6)
        month = 7 + (i % 4)
        day = 1 + (i % 20)
        start_time = datetime(year, month, day, tzinfo=timezone.utc)
        start_lat = float(rng.uniform(8.0, 18.0))
        start_lon = float(rng.uniform(120.0, 135.0))
        df = generate_storm_track(
            storm_id=f"WP{i+1:02d}{year}",
            n_fixes=n_fixes + rng.integers(-5, 6),
            start_lat=start_lat,
            start_lon=start_lon,
            start_time=start_time,
            seed=int(rng.integers(0, 1_000_000)),
        )
        frames.append(df)
    return pd.concat(frames, ignore_index=True)
