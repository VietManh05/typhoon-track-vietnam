"""Environmental steering features from gridded reanalysis (NCEP/NCAR R1).

Tropical-cyclone motion is governed mostly by the large-scale environmental
("steering") flow and the position of the subtropical ridge. Track-only models
cannot see either. For each fix this module samples, at the fix's own analysis
time (no future information):

* ``dlm_u``, ``dlm_v`` — deep-layer mean wind (0.25*850 + 0.5*500 + 0.25*200
  hPa), averaged over a 200-800 km annulus around the centre so the storm's own
  vortex is mostly excluded (m/s)
* ``u500``, ``v500`` — the same annulus mean at 500 hPa (m/s)
* ``shear_u``, ``shear_v`` — 200 minus 850 hPa annulus-mean wind (m/s)
* ``z500`` — 500 hPa geopotential height at the centre (m, bilinear)
* ``dz500_n/s/e/w`` — 500 hPa height 5 degrees north/south/east/west minus the
  centre value (m): where the ridge is, and how strong

Fields are read from per-year ``{uwnd,vwnd,hgt}.YYYY.npz`` files written by
``scripts/download_ncep_steering.py``. Times not on the 6-hourly analysis grid,
or outside the downloaded years/area, yield NaN rather than a guess.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ENV_COLUMNS: tuple[str, ...] = (
    "dlm_u",
    "dlm_v",
    "u500",
    "v500",
    "shear_u",
    "shear_v",
    "z500",
    "dz500_n",
    "dz500_s",
    "dz500_e",
    "dz500_w",
)
_WEIGHTS = np.array([0.25, 0.5, 0.25])  # 850, 500, 200 hPa
_EARTH_KM = 6371.0088


class SteeringFields:
    """Lazy per-year loader of u/v/height arrays (time, level, lat, lon)."""

    def __init__(self, directory: str | Path) -> None:
        self.directory = Path(directory)
        self._years: dict[int, dict | None] = {}

    def year(self, year: int) -> dict | None:
        if year not in self._years:
            # Keep one year (~45 MB) at a time; callers visit fixes in time order.
            self._years.clear()
            paths = {
                v: self.directory / f"{v}.{year}.npz" for v in ("uwnd", "vwnd", "hgt")
            }
            if not all(p.exists() for p in paths.values()):
                self._years[year] = None
            else:
                arrays = {}
                for name, path in paths.items():
                    with np.load(path, allow_pickle=False) as data:
                        if list(data["level"]) != [850, 500, 200]:
                            raise ValueError(f"{path} must hold 850/500/200 hPa")
                        arrays[name] = data["data"]
                        arrays["time"] = data["time"]
                        arrays["lat"] = data["lat"].astype(float)
                        arrays["lon"] = data["lon"].astype(float)
                arrays["index"] = {int(t): i for i, t in enumerate(arrays["time"])}
                self._years[year] = arrays
        return self._years[year]


def _bilinear(field: np.ndarray, lats: np.ndarray, lons: np.ndarray, lat, lon):
    """Bilinear sample of a regular (lat, lon) grid; NaN outside it."""

    lat_step, lon_step = lats[1] - lats[0], lons[1] - lons[0]
    fi = (lat - lats[0]) / lat_step
    fj = (lon - lons[0]) / lon_step
    i0, j0 = int(np.floor(fi)), int(np.floor(fj))
    if i0 < 0 or j0 < 0 or i0 + 1 >= len(lats) or j0 + 1 >= len(lons):
        return np.nan
    di, dj = fi - i0, fj - j0
    return float(
        field[i0, j0] * (1 - di) * (1 - dj)
        + field[i0 + 1, j0] * di * (1 - dj)
        + field[i0, j0 + 1] * (1 - di) * dj
        + field[i0 + 1, j0 + 1] * di * dj
    )


def _annulus(lats, lons, lat, lon, inner_km, outer_km) -> np.ndarray:
    la = np.radians(lats)[:, None]
    lo = np.radians(lons)[None, :]
    p, q = np.radians(lat), np.radians(lon)
    h = np.sin((la - p) / 2) ** 2 + np.cos(p) * np.cos(la) * np.sin((lo - q) / 2) ** 2
    dist = 2 * _EARTH_KM * np.arcsin(np.sqrt(np.clip(h, 0, 1)))
    return (dist >= inner_km) & (dist <= outer_km)


def steering_features(
    frame: pd.DataFrame,
    fields: SteeringFields,
    *,
    inner_km: float = 200.0,
    outer_km: float = 800.0,
    offset_deg: float = 5.0,
) -> pd.DataFrame:
    """Return ``ENV_COLUMNS`` for every row of ``frame`` (same index)."""

    out = np.full((len(frame), len(ENV_COLUMNS)), np.nan)
    times = pd.to_datetime(frame["timestamp"], utc=True)
    lats_in = frame["lat"].to_numpy(dtype=float)
    lons_in = frame["lon"].to_numpy(dtype=float)
    # Time order so each year's fields are loaded once.
    for row in np.argsort(times.to_numpy(), kind="stable"):
        when, lat, lon = times.iloc[row], lats_in[row], lons_in[row]
        arrays = fields.year(when.year)
        if arrays is None:
            continue
        t = arrays["index"].get(int(when.tz_convert(None).value // 1_000_000_000))
        if t is None:
            continue
        lats, lons = arrays["lat"], arrays["lon"]
        ring = _annulus(lats, lons, lat, lon, inner_km, outer_km)
        if not ring.any():
            continue
        u = arrays["uwnd"][t][:, ring].mean(axis=1)  # per level
        v = arrays["vwnd"][t][:, ring].mean(axis=1)
        z = arrays["hgt"][t][1]  # 500 hPa
        z0 = _bilinear(z, lats, lons, lat, lon)
        out[row] = [
            float(_WEIGHTS @ u),
            float(_WEIGHTS @ v),
            u[1],
            v[1],
            u[2] - u[0],
            v[2] - v[0],
            z0,
            _bilinear(z, lats, lons, lat + offset_deg, lon) - z0,
            _bilinear(z, lats, lons, lat - offset_deg, lon) - z0,
            _bilinear(z, lats, lons, lat, lon + offset_deg) - z0,
            _bilinear(z, lats, lons, lat, lon - offset_deg) - z0,
        ]
    return pd.DataFrame(out, index=frame.index, columns=list(ENV_COLUMNS))
