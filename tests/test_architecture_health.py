"""Architecture health tests: contracts, providers, configuration, and flow."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pytest
from pydantic import ValidationError

from typhoon_vn.datasets.typhoon_dataset import DatasetConfig, TyphoonDataset
from typhoon_vn.features.bridge import to_canonical_frame
from typhoon_vn.features.geo import bearing_deg, destination_point, haversine_km
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.ingestion.errors import ProviderSchemaError, UnsupportedProviderError
from typhoon_vn.ingestion.models import Observation
from typhoon_vn.ingestion.providers.strategies import (
    ParsedPayload,
    ProviderFactory,
    ProviderStrategy,
)
from typhoon_vn.settings import Settings
from typhoon_vn.training.config_loader import PipelineConfig


class EmptyProvider(ProviderStrategy):
    source = "empty"

    def parse(
        self, input_path: Path, *, source_url: str, checksum: str
    ) -> ParsedPayload:
        return self._checked([], input_path)


def test_provider_factory_isolates_unknown_and_schema_drift(tmp_path: Path) -> None:
    factory = ProviderFactory((EmptyProvider(),))
    assert factory.sources == ("empty",)
    with pytest.raises(UnsupportedProviderError, match="unsupported parser source"):
        factory.create("changed-provider")
    with pytest.raises(ProviderSchemaError, match="schema may have changed"):
        factory.create("EMPTY").parse(
            tmp_path / "payload.txt",
            source_url="https://example.test",
            checksum="a" * 64,
        )


def test_settings_and_pipeline_configuration_fail_fast() -> None:
    with pytest.raises(ValidationError, match="requests_per_minute"):
        Settings(_env_file=None, requests_per_minute=0)
    with pytest.raises(ValidationError, match="Production requires"):
        Settings(_env_file=None, app_env="PRODUCTION")
    production = Settings(
        _env_file=None,
        app_env="PRODUCTION",
        api_key="secret",
        allow_baseline=False,
    )
    assert production.app_env == "production"

    payload = {
        "experiment": {"name": "test", "device": "cpu"},
        "dataset": {"horizon": [2, 1], "val_ratio": 0.1, "test_ratio": 0.1},
        "model": {"type": "LSTMTrackForecaster"},
        "training": {},
        "loss": {},
        "checkpoint": {},
        "mlflow": {},
    }
    with pytest.raises(ValidationError, match="unique, increasing and positive"):
        PipelineConfig.model_validate(payload)


def test_geo_reference_values_and_antimeridian_round_trip() -> None:
    assert haversine_km(0, 0, 0, 1) == pytest.approx(111.195, rel=1e-4)
    assert haversine_km(21.0278, 105.8342, 10.8231, 106.6297) == pytest.approx(
        1137.0, rel=0.01
    )
    assert bearing_deg(0, 0, 0, 1) == pytest.approx(90.0)
    lat, lon = destination_point(10.0, 179.5, 90.0, 200.0)
    assert -180 <= lon <= 180
    assert haversine_km(10.0, 179.5, lat, lon) == pytest.approx(200.0, rel=1e-6)


def test_scaler_rejects_use_before_fit_and_preserves_training_statistics() -> None:
    frame = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [10.0, 20.0, 30.0]})
    scaler = FeatureScaler(["a", "b"])
    with pytest.raises(RuntimeError, match="must be fitted"):
        scaler.transform(frame)
    scaled = scaler.fit_transform(frame)
    assert scaled.mean().abs().max() < 1e-12
    held_out = scaler.transform(pd.DataFrame({"a": [1000.0], "b": [-1000.0]}))
    assert held_out.iloc[0, 0] > 100
    assert scaler._scaler.mean_.tolist() == pytest.approx([2.0, 20.0])


def test_ingestion_features_dataset_contract_end_to_end() -> None:
    observations = []
    start = datetime(2024, 7, 1, tzinfo=timezone.utc)
    for index in range(10):
        observations.append(
            Observation(
                source="jma",
                source_storm_id="2401",
                storm_id="WP012024",
                timestamp=start + pd.Timedelta(hours=6 * index),
                latitude=10.0 + index * 0.1,
                longitude=120.0 + index * 0.1,
                wind=30.0,
                wind_unit="kt",
                pressure_hpa=990.0,
                intensity_code="2",
                source_url="https://example.test/jma",
                source_file_checksum="a" * 64,
                dataset_version="v1",
            )
        )
    canonical = to_canonical_frame(
        pd.DataFrame([item.to_row() for item in observations])
    )
    dataset = TyphoonDataset(
        canonical,
        config=DatasetConfig(input_len=4, horizon=(1, 2), feature_cols=("lat", "lon")),
    )
    assert len(dataset) == 5
    assert dataset[0]["x"].shape == (4, 2)
    assert dataset[0]["y_reg"].shape == (2, 2)
    assert canonical["wind_ms"].iloc[0] == pytest.approx(30.0 * 0.514444)


def test_schema_drift_fails_before_feature_or_training_work() -> None:
    with pytest.raises(ValueError, match="raw observation schema missing"):
        to_canonical_frame(pd.DataFrame({"storm_id": ["S"]}))
    with pytest.raises(ValueError, match="canonical track schema missing"):
        TyphoonDataset(pd.DataFrame({"storm_id": ["S"]}))
