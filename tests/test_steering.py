"""Steering-flow features from gridded reanalysis fields."""

import numpy as np
import pandas as pd
import pytest

from typhoon_vn.features.steering import ENV_COLUMNS, SteeringFields, steering_features

LAT = np.arange(52.5, -2.6, -2.5, dtype=np.float32)
LON = np.arange(92.5, 182.6, 2.5, dtype=np.float32)
TIMES = pd.date_range("2020-09-01", periods=8, freq="6h", tz="UTC")


def _write(directory, variable, field):
    data = np.broadcast_to(field, (len(TIMES), 3, len(LAT), len(LON))).astype(
        np.float32
    )
    np.savez(
        directory / f"{variable}.2020.npz",
        data=data,
        time=(TIMES.tz_convert(None).values.astype("datetime64[s]").astype(np.int64)),
        level=np.array([850, 500, 200], dtype=np.int16),
        lat=LAT,
        lon=LON,
    )


@pytest.fixture()
def fields(tmp_path):
    levels = np.array([1.0, 2.0, 3.0])[:, None, None]  # 850, 500, 200 hPa
    _write(tmp_path, "uwnd", np.ones((3, len(LAT), len(LON))) * levels * 4)
    _write(tmp_path, "vwnd", -np.ones((3, len(LAT), len(LON))) * levels)
    # 500 hPa height rising northward by 10 m per degree latitude.
    hgt = np.zeros((3, len(LAT), len(LON))) + 5800 + 10 * LAT[None, :, None]
    _write(tmp_path, "hgt", hgt)
    return SteeringFields(tmp_path)


def _frame(**overrides):
    row = {"storm_id": "S", "timestamp": TIMES[2], "lat": 18.0, "lon": 120.0}
    row.update(overrides)
    return pd.DataFrame([row])


def test_uniform_flow_gives_layer_means_and_shear(fields) -> None:
    env = steering_features(_frame(), fields)
    assert list(env.columns) == list(ENV_COLUMNS)
    row = env.iloc[0]
    # Deep-layer mean weights 0.25/0.5/0.25 over 850/500/200 hPa.
    assert row["dlm_u"] == pytest.approx(4 * (0.25 * 1 + 0.5 * 2 + 0.25 * 3))
    assert row["dlm_v"] == pytest.approx(-(0.25 * 1 + 0.5 * 2 + 0.25 * 3))
    assert row["u500"] == pytest.approx(8) and row["v500"] == pytest.approx(-2)
    assert row["shear_u"] == pytest.approx(4 * (3 - 1))
    assert row["shear_v"] == pytest.approx(-(3 - 1))


def test_height_gradient_shows_ridge_direction(fields) -> None:
    row = steering_features(_frame(lat=17.3, lon=121.1), fields).iloc[0]
    assert row["z500"] == pytest.approx(5800 + 173, abs=1e-3)  # bilinear
    assert row["dz500_n"] == pytest.approx(50, abs=1e-3)  # 5 degrees north
    assert row["dz500_s"] == pytest.approx(-50, abs=1e-3)
    assert row["dz500_e"] == pytest.approx(0, abs=1e-3)
    assert row["dz500_w"] == pytest.approx(0, abs=1e-3)


def test_missing_time_or_year_is_nan_not_guessed(fields) -> None:
    off_grid = _frame(timestamp=TIMES[2] + pd.Timedelta(hours=3))
    other_year = _frame(timestamp=pd.Timestamp("2019-09-01", tz="UTC"))
    env = steering_features(pd.concat([off_grid, other_year]), fields)
    assert env.isna().all().all()


def test_index_is_preserved_for_joining(fields) -> None:
    frame = pd.concat([_frame(), _frame(lat=10.0)]).set_axis([7, 3])
    env = steering_features(frame, fields)
    assert list(env.index) == [7, 3]
