"""Point-in-time environmental feature extraction for gridded fields."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

import numpy as np
import pandas as pd


@dataclass(frozen=True, slots=True)
class GridMatch:
    value: float
    valid_time: pd.Timestamp
    available_at: pd.Timestamp
    latitude: float
    longitude: float


def _utc(value: object) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        timestamp = timestamp.tz_localize("UTC")
    return timestamp.tz_convert("UTC")


def sample_grid_point(
    data,
    *,
    variable: str,
    issue_time: object,
    latitude: float,
    longitude: float,
    available_at: object | None = None,
    max_age: timedelta = timedelta(days=2),
) -> GridMatch:
    """Select the latest field available at issue time and nearest grid cell.

    ``data`` is an xarray Dataset.  ``available_at`` may be passed for archive
    products (for example final ERA5); values published after ``issue_time``
    are rejected so they cannot leak into a simulated real-time forecast.
    """

    issue = _utc(issue_time)
    availability = _utc(available_at) if available_at is not None else issue
    if availability > issue:
        raise ValueError("environment field was not available at issue_time")
    if variable not in data:
        raise KeyError(variable)
    time_name = "time" if "time" in data.coords else "valid_time"
    field_times = pd.to_datetime(data[time_name].values, utc=True)
    eligible = field_times[field_times <= issue]
    if len(eligible) == 0:
        raise ValueError("no environmental field at or before issue_time")
    valid_time = pd.Timestamp(eligible[-1])
    if issue - valid_time > max_age:
        raise ValueError("environment field is too old for issue_time")
    selected = data[variable].sel(
        {time_name: valid_time.to_datetime64(), "lat": latitude, "lon": longitude},
        method="nearest",
    )
    value = float(selected.values)
    if not np.isfinite(value):
        raise ValueError(f"non-finite {variable} value")
    return GridMatch(
        value=value,
        valid_time=valid_time,
        available_at=availability,
        latitude=float(selected["lat"].values),
        longitude=float(selected["lon"].values),
    )


def sst_features(
    data,
    *,
    issue_time: object,
    latitude: float,
    longitude: float,
    variable: str = "sst",
    offset_degrees: float = 1.0,
) -> dict[str, float]:
    """Sample centre SST and a symmetric spatial gradient magnitude."""

    centre = sample_grid_point(
        data,
        variable=variable,
        issue_time=issue_time,
        latitude=latitude,
        longitude=longitude,
    )
    north = sample_grid_point(
        data,
        variable=variable,
        issue_time=issue_time,
        latitude=latitude + offset_degrees,
        longitude=longitude,
    ).value
    south = sample_grid_point(
        data,
        variable=variable,
        issue_time=issue_time,
        latitude=latitude - offset_degrees,
        longitude=longitude,
    ).value
    east = sample_grid_point(
        data,
        variable=variable,
        issue_time=issue_time,
        latitude=latitude,
        longitude=longitude + offset_degrees,
    ).value
    west = sample_grid_point(
        data,
        variable=variable,
        issue_time=issue_time,
        latitude=latitude,
        longitude=longitude - offset_degrees,
    ).value
    gradient = float(np.hypot(east - west, north - south) / (2 * offset_degrees))
    return {"sst_c": centre.value, "sst_gradient_c_per_degree": gradient}


def atmospheric_features(
    data,
    *,
    issue_time: object,
    latitude: float,
    longitude: float,
) -> dict[str, float]:
    """Extract MSLP, 850/200 hPa winds, humidity, and vertical shear."""

    names = ("mslp_hpa", "u850_ms", "v850_ms", "u200_ms", "v200_ms")
    values = {
        name: sample_grid_point(
            data,
            variable=name,
            issue_time=issue_time,
            latitude=latitude,
            longitude=longitude,
        ).value
        for name in names
    }
    if "humidity_pct" in data:
        values["humidity_pct"] = sample_grid_point(
            data,
            variable="humidity_pct",
            issue_time=issue_time,
            latitude=latitude,
            longitude=longitude,
        ).value
    du = values["u200_ms"] - values["u850_ms"]
    dv = values["v200_ms"] - values["v850_ms"]
    values["wind_shear_ms"] = float(np.hypot(du, dv))
    return values


__all__ = [
    "GridMatch",
    "atmospheric_features",
    "sample_grid_point",
    "sst_features",
]
