"""Hindcast export: issue-time selection uses only regular, verifiable windows."""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from export_hindcast import choose_issue  # noqa: E402


def _track(lons, hours=None):
    hours = hours if hours is not None else [6 * i for i in range(len(lons))]
    start = pd.Timestamp("2024-09-01", tz="UTC")
    return pd.DataFrame(
        {
            "timestamp": [start + pd.Timedelta(hours=h) for h in hours],
            "lat": [18.0] * len(lons),
            "lon": lons,
        }
    )


def test_picks_issue_whose_72h_position_is_closest_to_vietnam() -> None:
    # Westward track towards the coast (~106-108E at 18N).
    lons = [130 - i for i in range(30)]
    index = choose_issue(_track(lons))
    assert index is not None
    target = index + 12  # +72 h at 6-hourly steps
    assert abs(lons[target] - 107) <= 1


def test_requires_regular_input_window_and_all_horizons() -> None:
    assert choose_issue(_track([120.0] * 16)) is not None  # 4 inputs + 12 steps
    # 3-hourly spacing never forms a regular 6-hourly input window.
    assert choose_issue(_track([120.0] * 40, hours=[3 * i for i in range(40)])) is None
    # One fix short of verifying +72 h.
    assert choose_issue(_track([120.0] * 15)) is None
