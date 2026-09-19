"""Inference service and API acceptance tests for R13."""

from datetime import datetime, timedelta, timezone

import pytest
import torch
from fastapi.testclient import TestClient

from typhoon_vn.api.app import create_app
from typhoon_vn.api.schemas import Fix, ForecastRequest
from typhoon_vn.datasets.synthetic import generate_storm_track
from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.inference.service import TyphoonForecaster
from typhoon_vn.models.lstm import LSTMTrackForecaster
from typhoon_vn.operations.store import Store
from typhoon_vn.settings import Settings
from typhoon_vn.training.pipeline import export_bundle


def fixes(*, stale: bool = False, future: bool = False):
    base = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    if stale:
        base -= timedelta(days=3)
    if future:
        base += timedelta(hours=2)
    return [
        Fix(
            timestamp=base - timedelta(hours=(5 - i) * 6),
            lat=12 + i * 0.1,
            lon=120 + i * 0.1,
            wind_ms=25,
            pressure_hpa=980,
            intensity="TY",
            source="jma",
        )
        for i in range(6)
    ]


def bundle_path(tmp_path):
    frame = generate_storm_track("WP012024", n_fixes=20)
    scaler = FeatureScaler(list(FEATURE_COLUMNS)).fit(
        FeatureBuilder().feature_matrix(frame)
    )
    config = {
        "n_features": len(FEATURE_COLUMNS),
        "n_horizons": 5,
        "n_classes": 7,
        "hidden_size": 8,
        "num_layers": 1,
        "dropout": 0.0,
    }
    model = LSTMTrackForecaster(**config)
    for parameter in model.parameters():
        torch.nn.init.zeros_(parameter)
    return export_bundle(
        tmp_path / "bundle",
        model,
        scaler,
        version="trained-test",
        dataset_version="d1",
        dataset_sha256="a" * 64,
        model_config=config,
        input_len=4,
        horizons_hours=[6, 12, 24, 48, 72],
        validation_radius_km={str(h): float(h) for h in [6, 12, 24, 48, 72]},
        split_manifest={"train": ["WP012024"], "val": [], "test": [], "seed": 1},
        synthetic=True,
    )


def test_trained_bundle_forecast_has_provenance_and_loads_once(
    tmp_path, monkeypatch
) -> None:
    import typhoon_vn.training.pipeline as pipeline

    original = pipeline.load_bundle
    calls = []
    monkeypatch.setattr(
        pipeline, "load_bundle", lambda path: (calls.append(path), original(path))[1]
    )
    service = TyphoonForecaster(bundle_path(tmp_path), allow_baseline=False)
    request = ForecastRequest(storm_id="WP012024", observations=fixes())
    first = service.forecast(request)
    second = service.forecast(request)
    assert len(calls) == 1
    assert first.forecast_id == second.forecast_id
    assert first.model_kind == "trained-model"
    assert first.model_version == "trained-test" and first.dataset_version == "d1"
    assert first.sources == ["jma"] and len(first.points) == 5
    assert all(
        torch.isfinite(torch.tensor([p.lat, p.lon, p.radius_km])).all()
        for p in first.points
    )
    assert "not an official weather warning" in first.disclaimer
    assert first.uncertainty_method


def test_missing_artifact_and_time_freshness_fail_or_warn(tmp_path) -> None:
    with pytest.raises(FileNotFoundError):
        TyphoonForecaster(tmp_path / "missing", allow_baseline=False)
    baseline = TyphoonForecaster()
    stale = baseline.forecast(
        ForecastRequest(storm_id="S", observations=fixes(stale=True))
    )
    assert any("older than 24 hours" in warning for warning in stale.warnings)
    with pytest.raises(ValueError, match="future"):
        baseline.forecast(
            ForecastRequest(storm_id="S", observations=fixes(future=True))
        )


def test_api_auth_validation_and_rate_limit() -> None:
    settings = Settings(
        _env_file=None,
        api_key="secret",
        requests_per_minute=1,
        cache_enabled=False,
        operational_database_url="sqlite:///:memory:",
    )
    app = create_app(
        settings=settings,
        store=Store("sqlite:///:memory:"),
        forecaster=TyphoonForecaster(),
    )
    body = ForecastRequest(storm_id="S", observations=fixes()).model_dump(mode="json")
    with TestClient(app) as client:
        assert client.post("/forecast", json=body).status_code == 401
        headers = {"X-API-Key": "secret"}
        response = client.post("/forecast", json=body, headers=headers)
        assert response.status_code == 200
        assert response.json()["model_kind"] == "motion-baseline"
        limited = client.post("/forecast", json=body, headers=headers)
        assert limited.status_code == 429


def test_api_returns_422_for_invalid_observation_interval() -> None:
    settings = Settings(
        _env_file=None,
        cache_enabled=False,
        operational_database_url="sqlite:///:memory:",
    )
    app = create_app(
        settings=settings,
        store=Store("sqlite:///:memory:"),
        forecaster=TyphoonForecaster(),
    )
    bad = fixes()
    bad[-1] = bad[-1].model_copy(
        update={"timestamp": bad[-2].timestamp + timedelta(hours=25)}
    )
    with TestClient(app) as client:
        response = client.post(
            "/forecast",
            json=ForecastRequest(storm_id="S", observations=bad).model_dump(
                mode="json"
            ),
        )
    assert response.status_code == 422


def test_forecast_route_runs_blocking_inference_off_event_loop() -> None:
    import inspect

    app = create_app(
        settings=Settings(
            _env_file=None,
            operational_database_url="sqlite:///:memory:",
        ),
        store=Store("sqlite:///:memory:"),
        forecaster=TyphoonForecaster(),
    )
    route = next(
        route for route in app.routes if getattr(route, "path", None) == "/forecast"
    )
    # A synchronous endpoint is intentionally dispatched by Starlette's thread pool,
    # keeping pandas/PyTorch/database work out of the asyncio event loop.
    assert not inspect.iscoroutinefunction(route.endpoint)
