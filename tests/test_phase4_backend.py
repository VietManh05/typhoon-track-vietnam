"""Executable acceptance contracts for Phase 4 / backend gate M3."""

from __future__ import annotations

import fnmatch
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import inspect

from typhoon_vn.api.app import create_app
from typhoon_vn.api.schemas import Fix, ForecastRequest, ObservationBatch
from typhoon_vn.cli import main
from typhoon_vn.features.geospatial import Point
from typhoon_vn.inference.impact import assess_cone_impact, polygons_intersect
from typhoon_vn.inference.service import TyphoonForecaster
from typhoon_vn.ingestion.schedule import IngestionSchedule
from typhoon_vn.operations.cache import ForecastCache
from typhoon_vn.operations.store import Store, downgrade_database
from typhoon_vn.operations.worker import LiveWorker, update
from typhoon_vn.settings import Settings


class FakeRedis:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.reads = 0

    def get(self, key: str):
        self.reads += 1
        return self.values.get(key)

    def setex(self, key: str, ttl_seconds: int, value: str) -> None:
        assert ttl_seconds > 0
        self.values[key] = value

    def scan_iter(self, match: str):
        yield from [key for key in self.values if fnmatch.fnmatch(key, match)]

    def delete(self, *keys) -> int:
        deleted = 0
        for raw in keys:
            key = raw.decode() if isinstance(raw, bytes) else raw
            deleted += self.values.pop(key, None) is not None
        return deleted


def batch(storm_id: str = "WP012026") -> ObservationBatch:
    base = datetime.now(timezone.utc).replace(
        minute=0, second=0, microsecond=0
    ) - timedelta(hours=18)
    return ObservationBatch(
        storm_id=storm_id,
        name="Fixture storm",
        observations=[
            Fix(
                timestamp=base + timedelta(hours=6 * index),
                lat=12.0 + index * 0.2,
                lon=116.0 + index * 0.3,
                wind_ms=30,
                pressure_hpa=980,
                intensity="TY",
                source="fixture",
            )
            for index in range(4)
        ],
    )


def test_alembic_schema_has_audit_constraints_and_round_trip(tmp_path) -> None:
    database = tmp_path / "operations.db"
    url = f"sqlite:///{database.as_posix()}"
    store = Store(url)
    schema = inspect(store.engine)
    assert {
        "typhoons",
        "observations",
        "forecasts",
        "forecast_points",
        "alerts",
        "model_versions",
        "users",
        "subscriptions",
        "alembic_version",
    } <= set(schema.get_table_names())
    assert {"run_id", "issue_time", "model_version", "input_revision", "payload"} <= {
        column["name"] for column in schema.get_columns("forecasts")
    }
    assert schema.get_foreign_keys("forecast_points")
    assert schema.get_unique_constraints("observations")
    store.engine.dispose()
    downgrade_database(url)
    engine = Store(url, migrate=False).engine
    assert "forecasts" not in inspect(engine).get_table_names()
    engine.dispose()


def test_worker_is_idempotent_and_persists_forecast_audit() -> None:
    store = Store("sqlite:///:memory:")
    service = TyphoonForecaster()
    calls = 0
    original = service.forecast

    def counted(request):
        nonlocal calls
        calls += 1
        return original(request)

    service.forecast = counted
    first = update(store, service, [batch()])
    second = update(store, service, [batch()])
    assert len(first) == 1 and second == [] and calls == 1
    saved = store.latest_forecast("WP012026")
    assert saved["run_id"] == saved["forecast_id"]
    assert saved["input_revision"] and saved["model_version"] == "persistence-v1"


def test_live_worker_retries_with_bounded_exponential_backoff() -> None:
    class Provider:
        calls = 0

        def fetch_latest(self):
            self.calls += 1
            if self.calls < 3:
                raise OSError("temporary outage")
            return [batch("WP022026")]

    delays: list[float] = []
    worker = LiveWorker(
        store=Store("sqlite:///:memory:"),
        forecaster=TyphoonForecaster(),
        provider=Provider(),
        max_attempts=3,
        backoff_seconds=0.25,
        sleep=delays.append,
    )
    assert len(worker.run_once()) == 1
    assert delays == [0.25, 0.5]
    assert worker.status.failures == 2 and worker.status.last_error is None


def test_api_uses_redis_contract_and_invalidates_on_observation() -> None:
    redis = FakeRedis()
    cache = ForecastCache(redis, ttl_seconds=60)
    store = Store("sqlite:///:memory:")
    app = create_app(
        settings=Settings(
            _env_file=None,
            cache_enabled=False,
            operational_database_url="sqlite:///:memory:",
        ),
        store=store,
        forecaster=TyphoonForecaster(),
        cache=cache,
    )
    request = ForecastRequest(
        storm_id="WP032026", observations=batch("WP032026").observations
    )
    with TestClient(app) as client:
        first = client.post("/forecast", json=request.model_dump(mode="json"))
        assert first.status_code == 200
        second = client.post("/forecast", json=request.model_dump(mode="json"))
        assert second.json()["forecast_id"] == first.json()["forecast_id"]
        assert any(":forecast:" in key for key in redis.values)
        active = client.get("/typhoons/active")
        assert active.status_code == 200 and cache.active_key() in redis.values
        stored = client.post(
            "/observations", json=batch("WP032026").model_dump(mode="json")
        )
        assert stored.status_code == 200
        assert cache.active_key() not in redis.values


def test_model_promotion_invalidation_is_revision_scoped() -> None:
    redis = FakeRedis()
    cache = ForecastCache(redis, ttl_seconds=60)
    old_a = cache.key(storm_id="A", input_revision=1, model_revision="old")
    old_b = cache.key(storm_id="B", input_revision=2, model_revision="old")
    current = cache.key(storm_id="A", input_revision=1, model_revision="current")
    for key in (old_a, old_b, current):
        assert cache.put(key, {"key": key})
    assert cache.invalidate_model("old") == 2
    assert cache.get(old_a) is None and cache.get(old_b) is None
    assert cache.get(current) == {"key": current}


def test_api_error_matrix_and_openapi_contract() -> None:
    store = Store("sqlite:///:memory:")
    app = create_app(
        settings=Settings(
            _env_file=None,
            cache_enabled=False,
            operational_database_url="sqlite:///:memory:",
        ),
        store=store,
        forecaster=TyphoonForecaster(),
    )
    with TestClient(app) as client:
        missing = client.get("/typhoons/unknown/track")
        invalid = client.post("/forecast", json={"storm_id": "bad id"})
        assert missing.status_code == 404
        assert missing.json()["error"]["code"] == "not_found"
        assert invalid.status_code == 422
        assert invalid.json()["error"]["code"] == "validation_error"
        document = client.get("/openapi.json").json()
        responses = document["paths"]["/forecast"]["post"]["responses"]
        assert {"200", "401", "404", "422", "429", "503"} <= set(responses)
        schema = document["components"]["schemas"]["ForecastResponse"]["properties"]
        assert {
            "model_version",
            "dataset_version",
            "input_revision",
            "issue_time",
            "uncertainty_method",
            "disclaimer",
        } <= set(schema)

    class BrokenEngine:
        def connect(self):
            raise OSError("database unavailable")

        def dispose(self):
            return None

    broken = Store("sqlite:///:memory:")
    broken.engine = BrokenEngine()
    unavailable_app = create_app(
        settings=Settings(
            _env_file=None,
            cache_enabled=False,
            operational_database_url="sqlite:///:memory:",
        ),
        store=broken,
        forecaster=TyphoonForecaster(),
    )
    with TestClient(unavailable_app, raise_server_exceptions=False) as client:
        response = client.get("/ready")
        assert response.status_code == 503
        assert response.json()["error"]["code"] == "unavailable"


def test_impact_geometry_distinguishes_intersection_from_hazard_probability() -> None:
    forecast = TyphoonForecaster().forecast(
        ForecastRequest(
            storm_id="WP042026", observations=batch("WP042026").observations
        )
    )
    point = forecast.points[0]
    province: list[Point] = [
        (point.lon - 0.2, point.lat - 0.2),
        (point.lon + 0.2, point.lat - 0.2),
        (point.lon + 0.2, point.lat + 0.2),
        (point.lon - 0.2, point.lat + 0.2),
    ]
    coastline: list[Point] = [
        (point.lon, point.lat - 2),
        (point.lon, point.lat + 2),
    ]
    assessment = assess_cone_impact(
        forecast.points, province=province, coastline=coastline
    )
    assert assessment.intersects_province and assessment.intersects_coastline
    assert assessment.first_intersection_hours == 6
    assert assessment.hazard_probability is None
    touching = [(1.0, 0.0), (2.0, 0.0), (2.0, 1.0), (1.0, 1.0)]
    assert polygons_intersect(
        [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)], touching
    )


def test_inference_is_thread_safe_and_explicitly_flags_environment_fallback() -> None:
    service = TyphoonForecaster()
    request = ForecastRequest(
        storm_id="WP052026", observations=batch("WP052026").observations
    )
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: service.forecast(request), range(24)))
    assert len({result.forecast_id for result in results}) == 1
    assert service.cache_hits == 23

    service.bundle = {"manifest": {"required_environmental_features": ["sst_c"]}}
    service.version = "trained-requires-environment"
    service.kind = "trained-model"
    service.clear_cache()
    fallback = service.forecast(request)
    assert fallback.fallback_used is True
    assert fallback.fallback_reason == "required environmental features unavailable"
    assert fallback.model_kind == "motion-baseline"


def test_season_schedule_handles_timezone_year_boundary_and_outage() -> None:
    schedule = IngestionSchedule(live_hour_utc=0, max_backfill_runs=10)
    assert schedule.is_due(datetime(2026, 7, 1, 7, tzinfo=timezone(timedelta(hours=7))))
    assert not schedule.is_due(datetime(2026, 12, 1, tzinfo=timezone.utc))
    runs = schedule.due_runs(
        last_success=datetime(2026, 12, 27, tzinfo=timezone.utc),
        now=datetime(2027, 1, 5, tzinfo=timezone.utc),
    )
    assert runs == (
        datetime(2026, 12, 28, tzinfo=timezone.utc),
        datetime(2027, 1, 4, tzinfo=timezone.utc),
    )


def test_clean_data_cli_preserves_raw_hash_and_writes_provenance(
    tmp_path, capsys
) -> None:
    source = tmp_path / "track.csv"
    source.write_bytes(
        (Path(__file__).parent / "fixtures" / "phase2_track.csv").read_bytes()
    )
    original = source.read_bytes()
    destination = tmp_path / "output"
    assert (
        main(
            [
                "clean-data",
                "--input",
                str(source),
                "--output-dir",
                str(destination),
            ]
        )
        == 0
    )
    assert source.read_bytes() == original
    assert (destination / "features.parquet").is_file()
    provenance = (destination / "provenance.json").read_text(encoding="utf-8")
    assert "input_sha256" in provenance and "features.parquet" in provenance
    assert '"status": "ok"' in capsys.readouterr().out
