"""A29-024: live skill monitoring of issued forecasts and Prometheus metrics."""

from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from typhoon_vn.api.app import create_app
from typhoon_vn.api.schemas import Fix, ForecastRequest, ObservationBatch
from typhoon_vn.inference.service import TyphoonForecaster
from typhoon_vn.operations.monitoring import assess, verify_forecasts
from typhoon_vn.operations.store import Store
from typhoon_vn.settings import Settings

START = datetime(2025, 9, 1, tzinfo=timezone.utc)


def _fixes(n, lon_step=-0.5):
    return [
        Fix(
            timestamp=START + timedelta(hours=6 * i),
            lat=15.0,
            lon=120.0 + lon_step * i,
            wind_ms=30,
            pressure_hpa=980,
            intensity="TY",
            source="test",
        )
        for i in range(n)
    ]


def test_issued_forecasts_are_verified_against_later_observations(tmp_path) -> None:
    store = Store(f"sqlite:///{tmp_path / 'm.db'}")
    fixes = _fixes(10)
    forecast = TyphoonForecaster().forecast(
        ForecastRequest(storm_id="S", observations=fixes[:4])
    )
    store.save_forecast(forecast)
    store.upsert_observations(
        ObservationBatch(storm_id="S", name="S", observations=fixes)
    )

    report = verify_forecasts(store)
    by_h = {row["horizon_h"]: row for row in report["horizons"]}
    # Issue at fix 3; observations reach +36 h, so 6/12/24 h verify, 48/72 h not yet.
    assert [by_h[h]["n"] for h in (6, 12, 24, 48, 72)] == [1, 1, 1, 0, 0]
    # Constant-motion baseline on a constant-motion track: tiny errors, in cone.
    assert by_h[24]["mean_error_km"] < 5 and by_h[24]["cone_coverage"] == 1.0
    assert report["forecasts_checked"] == 1


def test_assess_flags_degraded_skill_only_with_enough_samples() -> None:
    healthy = {"horizons": [{"horizon_h": 24, "n": 50, "cone_coverage": 0.82}]}
    degraded = {"horizons": [{"horizon_h": 24, "n": 50, "cone_coverage": 0.40}]}
    too_few = {"horizons": [{"horizon_h": 24, "n": 3, "cone_coverage": 0.0}]}
    assert assess(healthy)["status"] == "ok"
    result = assess(degraded)
    assert result["status"] == "degraded" and "24" in result["reasons"][0]
    assert assess(too_few)["status"] == "insufficient-data"


def test_metrics_are_prometheus_text_with_latency_and_skill(tmp_path) -> None:
    settings = Settings(
        _env_file=None,
        api_key="k",
        requests_per_minute=100,
        operational_database_url=f"sqlite:///{tmp_path / 'api.db'}",
    )
    store = Store(settings.operational_database_url)
    app = create_app(settings=settings, store=store, forecaster=TyphoonForecaster())
    headers = {"X-API-Key": "k"}
    fixes = _fixes(10)
    with TestClient(app) as client:
        body = ForecastRequest(storm_id="S", observations=fixes[:4]).model_dump(
            mode="json"
        )
        response = client.post("/forecast", json=body, headers=headers)
        assert response.status_code == 200
        assert response.headers["X-Request-ID"]
        store.upsert_observations(
            ObservationBatch(storm_id="S", name="S", observations=fixes)
        )
        text = client.get("/metrics", headers=headers).text
    assert "# TYPE typhoon_http_request_duration_seconds histogram" in text
    assert 'typhoon_http_request_duration_seconds_bucket{le="+Inf"}' in text
    assert "typhoon_forecasts_issued_total 1" in text
    assert 'typhoon_forecast_cone_coverage{horizon_h="24"} 1.0' in text
    assert 'typhoon_forecast_verified{horizon_h="72"} 0' in text
