"""Load ingested IBTrACS WP partitions as cleaned 6-hourly tracks."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from typhoon_vn.features.bridge import load_raw_observations, to_canonical_frame
from typhoon_vn.features.cleaning import clean_tracks


def load_ibtracs(data_root: Path, years: tuple[int, int]) -> pd.DataFrame:
    """Raw IBTrACS rows for ``years`` (inclusive), synoptic 6-hourly only."""

    raw = load_raw_observations(data_root)
    raw = raw[
        (raw["source"] == "ibtracs")
        & ~raw["storm_id"].astype(str).str.contains("UNRESOLVED")
    ].copy()
    raw["timestamp"] = pd.to_datetime(raw["timestamp"], utc=True)
    return raw[
        raw["timestamp"].dt.year.between(*years) & (raw["timestamp"].dt.hour % 6 == 0)
    ]


def load_ibtracs_tracks(
    data_root: Path,
    years: tuple[int, int],
    bounds: tuple[float, float, float, float] | None = None,
):
    """Return ``(raw, cleaned, quality_report)`` for the benchmark scripts."""

    raw = load_ibtracs(data_root, years)
    cleaned, quality = clean_tracks(to_canonical_frame(raw), bounds=bounds)
    return raw, cleaned, quality
