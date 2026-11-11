"""Regression coverage for the cross-module findings of 2026-09-23."""

import json
from datetime import timedelta

import numpy as np
import pytest
import torch
from fastapi.testclient import TestClient
from redis.exceptions import ConnectionError as RedisConnectionError
from redis.exceptions import TimeoutError as RedisTimeoutError
from sqlalchemy import create_engine, inspect, text

from typhoon_vn.api.app import create_app
from typhoon_vn.api.schemas import ForecastRequest, Subscription
from typhoon_vn.datasets.synthetic import generate_storm_track
from typhoon_vn.datasets.typhoon_dataset import DatasetConfig, TyphoonDataset
from typhoon_vn.evaluation.backtest import backtest_bundle, backtest_storm
from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.inference.service import TyphoonForecaster
from typhoon_vn.operations.cache import ForecastCache
from typhoon_vn.operations.store import Store
from typhoon_vn.operations.worker import demo_batches, run_worker
from typhoon_vn.settings import Settings
from typhoon_vn.training.registry import PromotionPolicy
from typhoon_vn.weather.cache import WeatherCache


def test_input_scaling_never_changes_targets_or_source():
    frame = generate_storm_track("fixture", n_fixes=20)
    original = frame.copy(deep=True)
    scaler = FeatureScaler(list(FEATURE_COLUMNS)).fit(
        FeatureBuilder().feature_matrix(frame)
    )
    config = DatasetConfig(input_len=4, horizon=(1, 2))
    raw = TyphoonDataset(frame, config)
    scaled = TyphoonDataset(frame, config, scaler=scaler)
    assert len(raw) == len(scaled) > 0
    for before, after in zip(raw, scaled):
        np.testing.assert_array_equal(before["y_reg"], after["y_reg"])
        np.testing.assert_array_equal(before["y_cls"], after["y_cls"])
        assert not np.allclose(before["x"], after["x"])
    assert frame.equals(original)


def test_bundle_backtest_matches_serving_and_requires_scaler(tmp_path):
    from test_model_bundle import frame_to_fixes, make_bundle
    from typhoon_vn.training.pipeline import load_bundle, predict_bundle

    root, frame = make_bundle(tmp_path)
    bundle = load_bundle(root)
    with pytest.raises(ValueError, match="scaler"):
        backtest_storm(bundle["model"], frame)
    detail, _ = backtest_bundle(bundle, frame)
    # A later window also checks motion/lag features retain preceding history.
    at = detail.issue_time.unique()[2]
    window = frame[frame.timestamp <= at]
    horizons = bundle["manifest"]["horizons_hours"]
    expected, _ = predict_bundle(bundle, frame_to_fixes(window), horizons)
    actual = detail[detail.issue_time == at].sort_values("horizon_h")
    np.testing.assert_allclose(actual[["pred_lat", "pred_lon"]], expected, atol=1e-6)


LEGACY_DDL = [
    "CREATE TABLE typhoons (id VARCHAR(80) PRIMARY KEY, name VARCHAR(120) NOT NULL)",
    "CREATE TABLE observations (storm_id VARCHAR(80), timestamp VARCHAR(40), payload TEXT NOT NULL, PRIMARY KEY(storm_id,timestamp))",
    "CREATE TABLE forecasts (id VARCHAR(64) PRIMARY KEY, storm_id VARCHAR(80), issue_time VARCHAR(40), generated_at VARCHAR(40), payload TEXT NOT NULL)",
    "CREATE TABLE subscriptions (id VARCHAR(40) PRIMARY KEY, payload TEXT NOT NULL)",
    "CREATE TABLE alerts (id VARCHAR(64) PRIMARY KEY, subscription_id VARCHAR(40), storm_id VARCHAR(80), created_at VARCHAR(40), payload TEXT)",
    "CREATE TABLE schema_versions (version INTEGER PRIMARY KEY)",
]


def legacy_database(path, *, corrupt=False):
    url = f"sqlite:///{path.as_posix()}"
    engine = create_engine(url)
    batch = demo_batches()[0]
    forecast = TyphoonForecaster().forecast(
        ForecastRequest(storm_id=batch.storm_id, observations=batch.observations)
    )
    subscription = Subscription(label="review", lat=15, lon=115)
    with engine.begin() as conn:
        for statement in LEGACY_DDL:
            conn.exec_driver_sql(statement)
        conn.exec_driver_sql("INSERT INTO schema_versions VALUES (1)")
        conn.execute(
            text("INSERT INTO typhoons VALUES (:id, :name)"),
            {"id": batch.storm_id, "name": batch.name},
        )
        for fix in batch.observations:
            conn.execute(
                text("INSERT INTO observations VALUES (:id, :time, :payload)"),
                {
                    "id": batch.storm_id,
                    "time": fix.timestamp.isoformat(),
                    "payload": "bad-json" if corrupt else fix.model_dump_json(),
                },
            )
        conn.execute(
            text(
                "INSERT INTO forecasts VALUES (:id, :storm, :issue, :created, :payload)"
            ),
            {
                "id": forecast.forecast_id,
                "storm": forecast.storm_id,
                "issue": forecast.issue_time.isoformat(),
                "created": forecast.generated_at.isoformat(),
                "payload": forecast.model_dump_json(),
            },
        )
        conn.execute(
            text("INSERT INTO subscriptions VALUES ('subscription', :payload)"),
            {"payload": subscription.model_dump_json()},
        )
        conn.execute(
            text(
                "INSERT INTO alerts VALUES ('alert', 'subscription', :storm, :created, :payload)"
            ),
            {
                "storm": forecast.storm_id,
                "created": forecast.generated_at.isoformat(),
                "payload": json.dumps(
                    {"forecast_id": forecast.forecast_id, "message": "preserve me"}
                ),
            },
        )
    engine.dispose()
    return url, batch, forecast


def test_legacy_adoption_preserves_data_archives_and_is_repeatable(
    tmp_path, monkeypatch
):
    url, batch, forecast = legacy_database(tmp_path / "old.db")
    monkeypatch.chdir(tmp_path)
    for _ in range(2):
        store = Store(url)
        assert store.track(batch.storm_id) == batch.observations
        assert store.cached(forecast.forecast_id)["forecast_id"] == forecast.forecast_id
        assert len(store.list_subscriptions()) == 1
        assert store.alert_drafts()[0]["message"] == "preserve me"
        with store.engine.connect() as conn:
            assert (
                conn.exec_driver_sql("SELECT count(*) FROM forecast_points").scalar()
                == 5
            )
            assert (
                conn.exec_driver_sql(
                    "SELECT count(*) FROM legacy_v1_observations"
                ).scalar()
                == 8
            )
            assert conn.exec_driver_sql("PRAGMA foreign_key_check").all() == []
        store.engine.dispose()


def test_failed_legacy_adoption_rolls_back_even_ddl(tmp_path):
    url, _, _ = legacy_database(tmp_path / "corrupt.db", corrupt=True)
    with pytest.raises(ValueError):
        Store(url)
    engine = create_engine(url)
    assert set(inspect(engine).get_table_names()) == {
        "typhoons",
        "observations",
        "forecasts",
        "subscriptions",
        "alerts",
        "schema_versions",
    }
    with engine.connect() as conn:
        assert conn.exec_driver_sql("SELECT count(*) FROM observations").scalar() == 8
    engine.dispose()


def test_legacy_adoption_recovers_empty_alembic_table_and_rejects_downgrade(tmp_path):
    from typhoon_vn.operations.store import downgrade_database

    url, batch, _ = legacy_database(tmp_path / "interrupted.db")
    engine = create_engine(url)
    with engine.begin() as conn:
        conn.exec_driver_sql(
            "CREATE TABLE alembic_version (version_num VARCHAR(32) PRIMARY KEY)"
        )
    engine.dispose()
    store = Store(url)
    assert len(store.track(batch.storm_id)) == 8
    store.engine.dispose()
    with pytest.raises(RuntimeError, match="forward-only"):
        downgrade_database(url)


def test_unknown_legacy_schema_is_not_renamed(tmp_path):
    url, _, _ = legacy_database(tmp_path / "unknown.db")
    engine = create_engine(url)
    with engine.begin() as conn:
        conn.exec_driver_sql("ALTER TABLE typhoons ADD COLUMN unexpected TEXT")
    with pytest.raises(ValueError, match="Unrecognized legacy schema"):
        Store(url)
    assert "legacy_v1_typhoons" not in inspect(engine).get_table_names()
    engine.dispose()


@pytest.mark.parametrize("failure", [RedisConnectionError, RedisTimeoutError])
def test_real_redis_exceptions_fail_open_through_api_and_weather(failure):
    class BrokenRedis:
        def get(self, *args, **kwargs):
            raise failure("review fixture")

        setex = scan_iter = delete = get

    cache = ForecastCache(BrokenRedis())
    assert cache.get("key") is None
    assert not cache.put("key", {"ok": True})
    assert cache.invalidate_model("v1") == cache.invalidate_storm("s1") == 0
    weather = WeatherCache(BrokenRedis())
    weather.put("key", {"cached": True}, 60)
    assert weather.get("key")[0] == {"cached": True}
    store = Store("sqlite:///:memory:")
    batch = demo_batches()[0]
    app = create_app(
        Settings(_env_file=None, cache_enabled=False), store=store, cache=cache
    )
    with TestClient(app) as client:
        payload = ForecastRequest(
            storm_id=batch.storm_id, observations=batch.observations
        ).model_dump(mode="json")
        first = client.post("/forecast", json=payload)
        assert first.status_code == 200
        assert (
            client.post("/forecast", json=payload).json()["forecast_id"]
            == first.json()["forecast_id"]
        )
        assert client.get("/typhoons/active").status_code == 200
    store.engine.dispose()


def test_snapshot_worker_invalidates_active_and_populates_api_key(tmp_path):
    from test_cache import FakeRedis

    store = Store("sqlite:///:memory:")
    service = TyphoonForecaster()
    cache = ForecastCache(FakeRedis())
    cache.put(cache.active_key(), {"typhoons": []})
    batch = demo_batches()[0]
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text(json.dumps([batch.model_dump(mode="json")]), encoding="utf-8")
    run_worker(store, service, snapshot, once=True, cache=cache)
    assert cache.get(cache.active_key()) is None
    request = ForecastRequest(storm_id=batch.storm_id, observations=batch.observations)
    key = cache.key(
        storm_id=batch.storm_id,
        input_revision=request.model_dump(mode="json"),
        model_revision=service.version,
    )
    assert cache.get(key)["forecast_id"] == service.key(request)
    store.engine.dispose()


def test_weather_bundle_and_scoped_monitoring_token(tmp_path):
    token_file = tmp_path / "metrics-token"
    token_file.write_text("monitor-only\n", encoding="utf-8")
    store = Store("sqlite:///:memory:")
    settings = Settings(
        _env_file=None,
        cache_enabled=False,
        api_key="app-only",
        metrics_token_file=token_file,
    )
    app = create_app(settings, store=store)

    class Weather:
        def get(self, kind, location):
            assert location == "da-nang"
            return {"location": location} if kind == "current" else [{"kind": kind}]

    with TestClient(app) as client:
        app.state.services["weather"] = Weather()
        response = client.get("/api/weather/bundle?location_id=da-nang")
        assert response.status_code == 200
        assert set(response.json()) == {"current", "hourly", "daily"}
        assert response.json()["daily"] == [{"kind": "daily"}]
        assert client.get("/metrics").status_code == 401
        headers = {"Authorization": "Bearer monitor-only"}
        assert client.get("/metrics", headers=headers).status_code == 200
        assert client.get("/typhoons/active", headers=headers).status_code == 401
        assert (
            client.get(
                "/typhoons/active", headers={"X-API-Key": "app-only"}
            ).status_code
            == 200
        )
    store.engine.dispose()


@pytest.mark.parametrize(
    "error,coverage", [(float("nan"), 0.9), (1, float("inf")), (-1, 0.9), (1, 1.1)]
)
def test_promotion_rejects_invalid_metrics(error, coverage):
    with pytest.raises(ValueError, match="promotion gate"):
        PromotionPolicy(100, 0.8).validate(
            {"mean_error_km": error, "calibration_coverage": coverage}
        )


def test_response_preserves_bundle_metadata_and_rejects_old_bundles(tmp_path):
    from test_model_bundle import make_bundle
    from typhoon_vn.training.pipeline import load_bundle

    root, _ = make_bundle(tmp_path)
    path = root / "manifest.json"
    manifest = json.loads(path.read_text())
    manifest["uncertainty_method"] = "illustrative heuristic; not calibrated coverage"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    forecaster = TyphoonForecaster(root)
    batch = demo_batches()[0]
    response = forecaster.forecast(
        ForecastRequest(storm_id=batch.storm_id, observations=batch.observations)
    )
    assert response.uncertainty_method == manifest["uncertainty_method"]
    assert response.feature_schema_version == manifest["feature_schema_sha256"]
    assert response.scaler_version == manifest["files"]["scaler.json"]
    manifest["dataset_version"] = "retrained-same-display-version"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    replacement = TyphoonForecaster(root)
    assert replacement.version == forecaster.version
    assert replacement.cache_revision != forecaster.cache_revision
    request = ForecastRequest(storm_id=batch.storm_id, observations=batch.observations)
    assert replacement.key(request) != forecaster.key(request)
    manifest["bundle_schema_version"] = 1
    path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="unsupported bundle"):
        load_bundle(root)


def test_training_exports_best_weights_instead_of_last(tmp_path, monkeypatch):
    from test_training_pipeline import write_config
    from typhoon_vn.training.config_loader import load_config
    from typhoon_vn.training.run import run_training
    from typhoon_vn.training.trainer import Trainer

    config_path = tmp_path / "config.yaml"
    write_config(config_path)
    config = load_config(config_path)
    config = config.model_copy(
        update={"training": config.training.model_copy(update={"epochs": 2})}
    )

    def controlled_epoch(self, loader, training=True):
        if training:
            with torch.no_grad():
                next(self.model.parameters()).fill_(self.start_epoch)
        return {"loss": float(self.start_epoch), "reg_loss": 1.0, "cls_loss": 1.0}

    monkeypatch.setattr(Trainer, "_run_epoch", controlled_epoch)
    run_training(config, output_dir=tmp_path / "run")
    checkpoint_dir = tmp_path / "run" / config.checkpoint.dir
    best = torch.load(checkpoint_dir / "best.pt", weights_only=False)[
        "model_state_dict"
    ]
    last = torch.load(checkpoint_dir / "last.pt", weights_only=False)[
        "model_state_dict"
    ]
    exported = torch.load(tmp_path / "run/bundle/weights.pt", weights_only=True)
    assert all(torch.equal(exported[key], best[key]) for key in best)
    assert any(not torch.equal(exported[key], last[key]) for key in last)


def test_redis_cache_hit_refreshes_stale_warning():
    from test_cache import FakeRedis

    batch = demo_batches()[0]
    observations = [
        fix.model_copy(update={"timestamp": fix.timestamp - timedelta(days=3)})
        for fix in batch.observations
    ]
    request = ForecastRequest(storm_id=batch.storm_id, observations=observations)
    service = TyphoonForecaster()
    response = service.forecast(request).model_dump(mode="json")
    response["warnings"] = []  # Represents a response cached before the age threshold.
    cache = ForecastCache(FakeRedis())
    key = cache.key(
        storm_id=batch.storm_id,
        input_revision=request.model_dump(mode="json"),
        model_revision=service.cache_revision,
    )
    cache.put(key, response)
    store = Store("sqlite:///:memory:")
    with TestClient(
        create_app(
            Settings(_env_file=None, cache_enabled=False),
            store=store,
            forecaster=service,
            cache=cache,
        )
    ) as client:
        result = client.post("/forecast", json=request.model_dump(mode="json"))
        assert result.status_code == 200
        assert "Observations are older than 24 hours" in result.json()["warnings"]
    store.engine.dispose()


def test_reverted_observation_revision_wins_again():
    store = Store("sqlite:///:memory:")
    original = demo_batches()[0]
    first = original.observations[0]
    corrected = original.model_copy(
        update={
            "observations": [
                first.model_copy(update={"lat": first.lat + 0.5}),
                *original.observations[1:],
            ]
        }
    )
    assert store.upsert_observations(original) is True
    assert store.upsert_observations(original) is False
    assert store.upsert_observations(corrected) is True
    assert store.upsert_observations(original) is True
    assert store.track(original.storm_id)[0].lat == first.lat
    store.engine.dispose()


def test_worker_evaluates_new_subscription_for_stored_forecast():
    from typhoon_vn.operations.worker import update

    store = Store("sqlite:///:memory:")
    service = TyphoonForecaster()
    batch = demo_batches()[0]
    update(store, service, [batch])
    last = batch.observations[-1]
    store.subscribe(
        Subscription(label="late", lat=last.lat, lon=last.lon, radius_km=2000)
    )
    assert update(store, service, [batch]) == []
    assert len(store.alert_drafts()) == 1
    store.engine.dispose()
