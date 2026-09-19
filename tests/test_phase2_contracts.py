"""Contract tests for the Phase-2 data, feature and scaling boundary."""

from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import pytest
from pydantic import ValidationError

from typhoon_vn.api.schemas import Fix, ForecastPoint, ForecastResponse
from typhoon_vn.datasets.synthetic import generate_storm_track
from typhoon_vn.datasets.typhoon_dataset import (
    DatasetConfig,
    TyphoonDataset,
    split_by_storm_or_year,
)
from typhoon_vn.features.bridge import to_canonical_frame
from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.ingestion.models import Observation


def _raw(unit: str = "kt") -> pd.DataFrame:
    return pd.DataFrame(
        {
            "storm_id": ["WP012024"],
            "timestamp": ["2024-07-01T07:00:00+07:00"],
            "latitude": [10.0],
            "longitude": [120.0],
            "wind": [20.0],
            "wind_unit": [unit],
            "pressure_hpa": [990.0],
            "intensity_code": ["2"],
            "source": ["jma"],
            "source_url": ["https://example.test/source"],
            "source_file_checksum": ["a" * 64],
            "dataset_version": ["v1"],
            "downloaded_at": ["2024-07-01T08:00:00+07:00"],
        }
    )


def test_observation_to_feature_to_api_preserves_contract() -> None:
    obs = Observation(
        source="JMA",
        source_storm_id="2401",
        storm_id="WP012024",
        timestamp=datetime(2024, 7, 1, 7, tzinfo=timezone(timedelta(hours=7))),
        latitude=10.0,
        longitude=120.0,
        wind=20.0,
        wind_unit="kt",
        pressure_hpa=990.0,
        source_url="https://example.test/source",
        source_file_checksum="a" * 64,
        dataset_version="v1",
        downloaded_at=datetime(2024, 7, 1, 8, tzinfo=timezone(timedelta(hours=7))),
    )
    frame = to_canonical_frame(pd.DataFrame([obs.to_row()]))
    row = frame.iloc[0]
    fix = Fix(
        timestamp=row["timestamp"],
        lat=row["lat"],
        lon=row["lon"],
        wind_ms=row["wind_ms"],
        pressure_hpa=row["pressure_hpa"],
        intensity=row["intensity"],
        source=row["source"],
        source_url=row["source_url"],
    )
    assert fix.timestamp == datetime(2024, 7, 1, tzinfo=timezone.utc)
    assert fix.wind_ms == pytest.approx(20.0 * 0.514444)
    assert row["source_file_checksum"] == "a" * 64
    assert row["dataset_version"] == "v1"
    assert pd.Timestamp(row["downloaded_at"]) == pd.Timestamp("2024-07-01T01:00:00Z")


@pytest.mark.parametrize("latitude,longitude", [(np.nan, 120.0), (10.0, np.inf)])
def test_observation_rejects_nonfinite_coordinates(
    latitude: float, longitude: float
) -> None:
    with pytest.raises(ValueError):
        Observation(
            "jma",
            "1",
            "WP012024",
            datetime.now(timezone.utc),
            latitude,
            longitude,
            "https://example.test",
            "a" * 64,
        )


def test_contract_rejects_naive_time_and_unknown_wind_unit() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        Observation(
            "jma",
            "1",
            "WP012024",
            datetime(2024, 1, 1),
            10.0,
            120.0,
            "https://example.test",
            "a" * 64,
        )
    with pytest.raises(ValueError, match="unsupported wind unit"):
        to_canonical_frame(_raw("mph"))
    with pytest.raises(ValidationError):
        Fix(timestamp=datetime(2024, 1, 1), lat=10, lon=120, source="jma")


def test_forecast_times_are_utc_and_match_horizons() -> None:
    issue = datetime(2024, 7, 1, tzinfo=timezone.utc)
    point = ForecastPoint(
        horizon_hours=6,
        valid_time=issue + timedelta(hours=6),
        lat=10,
        lon=120,
        intensity="TS",
        radius_km=50,
        cone={},
    )
    ForecastResponse(
        forecast_id="f1",
        storm_id="WP012024",
        issue_time=issue,
        generated_at=issue,
        model_version="v1",
        model_kind="baseline",
        dataset_version="d1",
        sources=["jma"],
        uncertainty_method="none",
        warnings=[],
        points=[point],
    )
    with pytest.raises(ValidationError, match="valid_time"):
        ForecastResponse(
            forecast_id="f1",
            storm_id="WP012024",
            issue_time=issue,
            generated_at=issue,
            model_version="v1",
            model_kind="baseline",
            dataset_version="d1",
            sources=["jma"],
            uncertainty_method="none",
            warnings=[],
            points=[point.model_copy(update={"valid_time": issue})],
        )


def test_dataset_targets_exact_times_and_skips_gap() -> None:
    frame = generate_storm_track("WP012024", n_fixes=8)
    frame["lat"] = np.arange(8, dtype=float)
    config = DatasetConfig(input_len=2, horizon=(1, 2), feature_cols=("lat", "lon"))
    dataset = TyphoonDataset(frame, config=config)
    assert dataset[0]["y_reg"][:, 0].tolist() == [2.0, 3.0]

    gap = frame.drop(index=3).reset_index(drop=True)  # +12 target absent, +18 exists
    gap_dataset = TyphoonDataset(gap, config=config)
    assert all(
        sample["meta"]["issue_time"] != frame.loc[1, "timestamp"]
        for sample in gap_dataset.samples
    )


def test_dataset_rejects_duplicate_timestamp() -> None:
    frame = generate_storm_track("WP012024", n_fixes=8)
    frame.loc[2, "timestamp"] = frame.loc[1, "timestamp"]
    with pytest.raises(ValueError, match="duplicate timestamps"):
        TyphoonDataset(frame, config=DatasetConfig(input_len=2, horizon=(1, 2)))


def test_split_zero_ratios_and_cross_year_storm() -> None:
    frame = generate_storm_track(
        "WP012024", n_fixes=8, start_time=datetime(2024, 12, 31, tzinfo=timezone.utc)
    )
    train, val, test = split_by_storm_or_year(
        frame, val_ratio=0, test_ratio=0, by_year=True
    )
    assert len(train) == len(frame)
    assert val.empty and test.empty
    with pytest.raises(ValueError, match="less than 1"):
        split_by_storm_or_year(frame, val_ratio=0.5, test_ratio=0.5)


def test_dataset_uses_canonical_feature_order() -> None:
    frame = generate_storm_track("WP012024", n_fixes=20)
    dataset = TyphoonDataset(frame, config=DatasetConfig(input_len=4, horizon=(1, 2)))
    assert dataset.feature_cols == list(FEATURE_COLUMNS)
    assert dataset[0]["x"].shape[1] == len(FEATURE_COLUMNS)
    assert FeatureBuilder().feature_columns == dataset.feature_cols


def test_scaler_is_train_only_and_enforces_order(tmp_path) -> None:
    train = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [10.0, 20.0, 30.0]})
    held_out = pd.DataFrame({"a": [1e9], "b": [-1e9]})
    scaler = FeatureScaler(["a", "b"]).fit(train)
    mean_before = scaler._scaler.mean_.copy()
    scaler.transform(held_out)
    assert scaler._scaler.mean_ == pytest.approx(mean_before)

    restored = FeatureScaler.load(scaler.save(tmp_path / "scaler.joblib"))
    round_trip = restored.inverse_transform(restored.transform(train))
    assert np.max(np.abs(round_trip[["a", "b"]].to_numpy() - train.to_numpy())) <= 1e-6
    with pytest.raises(ValueError, match="missing feature columns"):
        restored.transform(train[["a"]])
    with pytest.raises(ValueError, match="reordered"):
        restored.transform(train[["b", "a"]])
    with pytest.raises(ValueError, match="unexpected feature columns"):
        restored.transform(train.assign(c=0.0))
