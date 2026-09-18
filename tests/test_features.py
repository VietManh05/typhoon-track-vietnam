"""Regression tests for the Phase-2 feature pipeline and raw Parquet storage.

Covers the critical fixes:

* ``FeatureScaler`` must stay finite when a training column has no finite value.
* Motion features must not fabricate a 6 h interval for duplicate timestamps.
* The bridge uses ``JMA_ARCHIVE_START_YEAR`` for JMA coverage and maps
  intensity without ``Series.apply``.
* Raw Parquet writes are atomic (``.tmp`` + rename).
"""

from __future__ import annotations

import shutil
import tempfile
import warnings
from collections.abc import Iterator
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from typhoon_vn.features import build as features
from typhoon_vn.features.bridge import JMA_ARCHIVE_START_YEAR, to_canonical_frame
from typhoon_vn.features.geo import haversine_km
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.ingestion.models import Observation
from typhoon_vn.ingestion.storage import write_observations


def _track_frame(
    timestamps: list[str],
    lats: list[float],
    lons: list[float],
    storm_id: str = "WP012024",
) -> pd.DataFrame:
    """Minimal cleaned-schema frame accepted by ``add_motion_features``."""

    return pd.DataFrame(
        {
            "storm_id": [storm_id] * len(timestamps),
            "timestamp": pd.to_datetime(list(timestamps), utc=True),
            "lat": lats,
            "lon": lons,
            "wind_ms": [25.0] * len(timestamps),
            "pressure_hpa": [990.0] * len(timestamps),
            "intensity": ["TS"] * len(timestamps),
            "end_flag": ["ONGOING"] * len(timestamps),
            "source": ["jma"] * len(timestamps),
            "interpolated": [False] * len(timestamps),
            "suspicious": [False] * len(timestamps),
        }
    )


def _raw_frame(intensity_codes: list[object], sources: list[str]) -> pd.DataFrame:
    """Raw Phase-1-shaped rows (knots + intensity codes) for the bridge."""

    n = len(intensity_codes)
    return pd.DataFrame(
        {
            "storm_id": ["WP012024"] * n,
            "timestamp": pd.to_datetime(["2024-07-01T00:00"] * n, utc=True),
            "latitude": [10.0] * n,
            "longitude": [120.0] * n,
            "wind": [35.0] * n,
            "wind_unit": ["kt"] * n,
            "pressure_hpa": [990.0] * n,
            "intensity_code": intensity_codes,
            "source": sources,
        }
    )


def _observation(**overrides: object) -> Observation:
    base: dict[str, object] = {
        "source": "jma",
        "source_storm_id": "2401",
        "storm_id": "WP012024",
        "timestamp": datetime(2024, 7, 1, tzinfo=timezone.utc),
        "latitude": 10.0,
        "longitude": 120.0,
        "source_url": "https://example.test/jma.txt",
        "source_file_checksum": "a" * 64,
    }
    base.update(overrides)
    return Observation(**base)  # type: ignore[arg-type]


@pytest.fixture()
def workdir() -> Iterator[Path]:
    """Private temp directory for artefact round-trips.

    The shared ``tmp_path`` base directory is not readable in this environment,
    so create and clean up an isolated directory under the OS temp root.
    """

    path = Path(tempfile.mkdtemp(prefix="typhoon-vn-test-"))
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


# --------------------------------------------------------------------------- #
# Bug #1 - FeatureScaler must not be corrupted by an all-NaN column
# --------------------------------------------------------------------------- #
def test_scaler_handles_all_nan_column() -> None:
    train = pd.DataFrame({"lat": [1.0, 2.0, 3.0], "wind_shear": [np.nan] * 3})
    scaler = FeatureScaler(feature_columns=["lat", "wind_shear"])

    with pytest.warns(RuntimeWarning, match="no finite training values"):
        scaler.fit(train)

    out = scaler.transform(train)
    assert np.isfinite(out.to_numpy()).all()
    assert out["wind_shear"].tolist() == [0.0, 0.0, 0.0]
    # A fitted-but-degenerate column must not poison the healthy column either.
    assert np.isfinite(out["lat"].to_numpy()).all()


def test_scaler_fills_partial_nan_with_train_mean() -> None:
    train = pd.DataFrame({"lat": [1.0, np.nan, 3.0]})
    scaler = FeatureScaler(feature_columns=["lat"]).fit(train)

    out = scaler.transform(pd.DataFrame({"lat": [np.nan, 1.0]}))

    # NaN -> train mean (2.0) -> z-score 0; the spread is the train population
    # std of the mean-filled column ([1, 2, 3] -> sqrt(2/3)).
    expected_std = float(np.std([1.0, 2.0, 3.0]))
    assert out["lat"].iloc[0] == pytest.approx(0.0)
    assert out["lat"].iloc[1] == pytest.approx((1.0 - 2.0) / expected_std)


def test_scaler_degenerate_column_survives_save_and_load(workdir: Path) -> None:
    train = pd.DataFrame({"lat": [1.0, 2.0, 3.0], "wind_shear": [np.nan] * 3})
    with pytest.warns(RuntimeWarning):
        scaler = FeatureScaler(feature_columns=["lat", "wind_shear"]).fit(train)

    path = scaler.save(workdir / "scaler.joblib")
    reloaded = FeatureScaler.load(path)
    scaled = reloaded.transform(train)

    assert np.isfinite(scaled.to_numpy()).all()
    restored = reloaded.inverse_transform(scaled)
    assert restored["lat"].to_numpy() == pytest.approx([1.0, 2.0, 3.0])
    assert restored["wind_shear"].tolist() == [0.0, 0.0, 0.0]


def test_scaler_masks_inf_out_of_train_mean_without_warning() -> None:
    train = pd.DataFrame({"x": [1.0, 2.0, np.inf]})
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # a finite column must not warn
        scaler = FeatureScaler(feature_columns=["x"]).fit(train)

    out = scaler.transform(pd.DataFrame({"x": [np.inf, -np.inf]}))

    assert np.isfinite(out.to_numpy()).all()
    # inf is masked from the mean (1.5) and replaced by it at transform time.
    assert out["x"].tolist() == pytest.approx([0.0, 0.0])


# --------------------------------------------------------------------------- #
# Bug #2 - no fabricated 6 h interval for duplicate timestamps
# --------------------------------------------------------------------------- #
def test_motion_features_skip_duplicate_timestamp() -> None:
    df = _track_frame(
        [
            "2024-07-01T00:00",
            "2024-07-01T06:00",
            "2024-07-01T06:00",  # duplicate timestamp, conflicting fix
            "2024-07-01T12:00",
        ],
        [10.0, 11.0, 11.5, 12.0],
        [120.0, 121.0, 121.5, 122.0],
    )
    out = features.add_motion_features(df).reset_index(drop=True)

    duplicate = out.iloc[2]
    # No fabricated dt: the duplicate row keeps neutral defaults instead of
    # reporting a bogus speed/accel computed over an invented 6 h interval.
    assert duplicate["step_km"] == 0.0
    assert duplicate["speed_kmh"] == 0.0
    assert duplicate["accel_kmh2"] == 0.0

    speed_first = haversine_km(10.0, 120.0, 11.0, 121.0) / 6.0
    assert out.iloc[1]["speed_kmh"] == pytest.approx(speed_first)

    # The duplicate is also never used as the reference for the next fix.
    expected_speed = haversine_km(11.0, 121.0, 12.0, 122.0) / 6.0
    assert out.iloc[3]["speed_kmh"] == pytest.approx(expected_speed)
    assert out.iloc[3]["accel_kmh2"] == pytest.approx(
        (expected_speed - speed_first) / 6.0
    )


def test_motion_features_regular_series_uses_real_dt() -> None:
    df = _track_frame(
        ["2024-07-01T00:00", "2024-07-01T06:00", "2024-07-01T12:00"],
        [10.0, 11.0, 12.0],
        [120.0, 121.0, 122.0],
    )
    out = features.add_motion_features(df).reset_index(drop=True)

    assert out.iloc[0]["speed_kmh"] == 0.0
    speed_1 = haversine_km(10.0, 120.0, 11.0, 121.0) / 6.0
    speed_2 = haversine_km(11.0, 121.0, 12.0, 122.0) / 6.0
    assert out.iloc[1]["speed_kmh"] == pytest.approx(speed_1)
    assert out.iloc[2]["speed_kmh"] == pytest.approx(speed_2)
    assert out.iloc[2]["accel_kmh2"] == pytest.approx((speed_2 - speed_1) / 6.0)


# --------------------------------------------------------------------------- #
# Medium - bridge uses JMA_ARCHIVE_START_YEAR and vectorised np.select mapping
# --------------------------------------------------------------------------- #
def test_bridge_drops_only_pre_archive_jma_rows() -> None:
    raw = pd.DataFrame(
        {
            "storm_id": ["WP011900", "WP021949", "WP031980"],
            "timestamp": pd.to_datetime(
                ["1900-01-01T00:00", "1949-07-01T00:00", "1980-07-01T00:00"], utc=True
            ),
            "latitude": [10.0, 12.0, 14.0],
            "longitude": [120.0, 122.0, 124.0],
            "wind": [50.0, 60.0, 70.0],
            "wind_unit": ["kt", "kt", "kt"],
            "pressure_hpa": [990.0, 985.0, 980.0],
            "intensity_code": ["3", "5", "9"],
            "source": ["jma", "ibtracs", "jma"],
        }
    )

    out = to_canonical_frame(raw)

    assert JMA_ARCHIVE_START_YEAR == 1951
    # Pre-1951 JMA row dropped; the pre-1951 IBTrACS row is preserved.
    assert out["timestamp"].dt.year.tolist() == [1949, 1980]
    assert out["source"].tolist() == ["ibtracs", "jma"]


def test_bridge_maps_intensity_per_source_and_code() -> None:
    raw = _raw_frame(["5", "2", "TS", None], ["jma", "jma", "cma", "cma"])

    out = to_canonical_frame(raw)

    assert out["intensity"].tolist() == ["TY", "TS", "TS", "UNK"]
    assert out["wind_ms"].iloc[0] == pytest.approx(35.0 * 0.514444)


def test_bridge_intensity_mapping_does_not_use_row_apply(monkeypatch) -> None:
    raw = _raw_frame(["5", "2", "TS", None], ["jma", "jma", "cma", "cma"])

    def _forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("to_canonical_frame must not call DataFrame.apply")

    monkeypatch.setattr(pd.DataFrame, "apply", _forbidden)

    out = to_canonical_frame(raw)

    assert out["intensity"].tolist() == ["TY", "TS", "TS", "UNK"]


# --------------------------------------------------------------------------- #
# Medium - raw Parquet writes must be atomic
# --------------------------------------------------------------------------- #
def test_storage_writes_readable_part_atomically(workdir: Path) -> None:
    paths = write_observations([_observation()], data_root=workdir)

    assert len(paths) == 1
    part = paths[0]
    assert part.name == "part-00000.parquet"
    assert part.exists()
    assert not list(workdir.rglob("*.tmp"))
    assert pd.read_parquet(part).shape[0] == 1


def test_storage_leaves_no_partial_part_on_failure(workdir: Path, monkeypatch) -> None:
    def _explode(self, path, *args: object, **kwargs: object) -> None:
        Path(path).write_bytes(b"partial")  # truncated staging file
        raise OSError("simulated disk failure")

    monkeypatch.setattr(pd.DataFrame, "to_parquet", _explode)

    with pytest.raises(OSError):
        write_observations([_observation()], data_root=workdir)

    # No final part and no leftover staging file: the partition stays re-runnable.
    assert list(workdir.rglob("part-*.parquet")) == []
    assert list(workdir.rglob("*.tmp")) == []
