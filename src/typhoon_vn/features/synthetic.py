"""Synthetic best-track generator for Phase 2 development and demos.

Produces CMA-shaped 6-hourly fixes for a few fictitious storms heading toward
the Vietnam coast, with deliberately injected defects (missing wind/pressure,
a duplicate fix, an out-of-range coordinate, an implausible jump) so the
cleaning pipeline has something to detect. NOT for model training.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from typhoon_vn.features.geo import destination_point

rng = np.random.default_rng(20260913)


def make_synthetic_tracks(n_storms: int = 4, steps: int = 20) -> pd.DataFrame:
    """Build a raw-shaped frame with the canonical schema columns."""

    rows: list[dict] = []
    starts = [
        (12.0, 125.0, 290.0),  # East Sea approach, heading WNW
        (18.0, 128.0, 280.0),  # Luzon strait, heading W
        (9.0, 118.0, 300.0),  # South, heading WNW
        (21.0, 122.0, 265.0),  # North, heading W
    ]
    intensities = ["TD", "TS", "STS", "TY", "STY"]
    for s in range(n_storms):
        lat, lon, bearing = starts[s % len(starts)]
        ts = pd.Timestamp("2024-09-01", tz="UTC") + pd.Timedelta(days=7 * s)
        wind = 18.0 + 4.0 * s
        pressure = 1000.0 - 4.0 * s
        for k in range(steps):
            wind = float(np.clip(wind + rng.normal(1.2, 2.0), 10.0, 65.0))
            pressure = float(np.clip(pressure + rng.normal(-1.5, 1.0), 920.0, 1005.0))
            grade = intensities[min(4, int((wind - 10) // 10))]
            rows.append(
                {
                    "storm_id": f"SYN{2024}{s + 1:02d}",
                    "timestamp": ts + pd.Timedelta(hours=6 * k),
                    "lat": round(lat, 2),
                    "lon": round(lon, 2),
                    "wind_ms": round(wind, 1),
                    "pressure_hpa": round(pressure, 1),
                    "intensity": grade,
                    "end_flag": "END" if k == steps - 1 else "ONGOING",
                    "source": "CMA" if s % 2 == 0 else "JMA",
                    "interpolated": False,
                    "suspicious": False,
                }
            )
            step_km = float(rng.normal(140.0, 25.0))
            bearing = (bearing + float(rng.normal(0.0, 6.0))) % 360.0
            lat, lon = destination_point(lat, lon, bearing, step_km)

    df = pd.DataFrame(rows)

    # --- Inject defects ------------------------------------------------------
    # 1. Interior missing values (must be interpolated).
    df.loc[5, "wind_ms"] = np.nan
    df.loc[6, "pressure_hpa"] = np.nan
    # 2. Duplicate fix from a second source (must be deduped).
    dup = df.iloc[10].copy()
    dup["source"] = "JTWC"
    df = pd.concat([df, dup.to_frame().T], ignore_index=True)
    # 3. Out-of-range coordinate (must be dropped).
    df.loc[15, "lat"] = 55.0
    # 4. Implausible jump (must be flagged, not deleted).
    df.loc[30, "lat"] = df.loc[30, "lat"] + 12.0
    # 5. Unphysical wind (must be dropped).
    df.loc[40, "wind_ms"] = 500.0
    return df.reset_index(drop=True)


if __name__ == "__main__":
    frame = make_synthetic_tracks()
    frame.to_csv("data/raw/synthetic_raw.csv", index=False)
    print(f"wrote data/raw/synthetic_raw.csv with {len(frame)} rows")
