"""Offline review probes. Run from repository root; no production data writes."""

import json
import logging
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ["DEBUG"] = "false"

import torch
from fastapi.testclient import TestClient
from redis.exceptions import ConnectionError as RedisConnectionError
from sqlalchemy import create_engine

from typhoon_vn.api.app import create_app
from typhoon_vn.api.schemas import ForecastRequest
from typhoon_vn.datasets.synthetic import generate_synthetic_catalogue
from typhoon_vn.datasets.typhoon_dataset import DatasetConfig, TyphoonDataset
from typhoon_vn.evaluation.backtest import backtest_storm
from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.inference.service import TyphoonForecaster
from typhoon_vn.operations.cache import ForecastCache
from typhoon_vn.operations.store import Store
from typhoon_vn.operations.worker import demo_batches, update
from typhoon_vn.settings import Settings
from typhoon_vn.training.registry import PromotionPolicy
from typhoon_vn.weather.cache import WeatherCache


def outcome(call):
    try:
        value = call()
        if isinstance(value, Store):
            value.engine.dispose()
            value = "Store initialized successfully"
        return {"returned": value}
    except Exception as exc:
        return {"exception": type(exc).__name__, "message": str(exc).splitlines()[0]}


class BrokenRedis:
    def get(self, *args, **kwargs):
        raise RedisConnectionError("offline review fixture")

    setex = scan_iter = delete = get


class MemoryRedis:
    def __init__(self):
        self.values = {}

    def get(self, key):
        return self.values.get(key)

    def setex(self, key, ttl, value):
        self.values[key] = value

    def scan_iter(self, match):
        return iter(())

    def delete(self, *keys):
        return 0


results = {}
temporary_root = ROOT / ".pytest-temp"
temporary_root.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix="review-probes-", dir=temporary_root) as work:
    work = Path(work)
    wheels = sorted((temporary_root / "improved-wheel").glob("*.whl"))
    if not wheels:
        wheels = sorted((temporary_root / "review-20260923-wheel").glob("*.whl"))
    if wheels:
        wheel_root = work / "installed-wheel"
        with zipfile.ZipFile(wheels[-1]) as archive:
            resources = [
                name
                for name in archive.namelist()
                if "migration" in name or name.endswith("alembic.ini")
            ]
            archive.extractall(wheel_root)
        program = (
            "import sys; sys.path.insert(0, " + repr(str(wheel_root)) + "); "
            "from typhoon_vn.operations.store import Store; "
            "Store('sqlite:///:memory:')"
        )
        process = subprocess.run(
            [sys.executable, "-I", "-c", program],
            cwd=work,
            capture_output=True,
            text=True,
        )
        results["built_wheel_startup"] = {
            "migration_resources": resources,
            "returncode": process.returncode,
            "last_error": process.stderr.splitlines()[-1] if process.stderr else None,
        }
    old_source = subprocess.check_output(
        ["rtk", "proxy", "git", "show", "main:src/typhoon_vn/operations/store.py"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )
    legacy = {}
    exec(old_source.split("class Store:", 1)[0], legacy)
    legacy_url = "sqlite:///" + (work / "legacy.db").as_posix()
    engine = create_engine(legacy_url)
    legacy["metadata"].create_all(engine)
    engine.dispose()
    results["legacy_database_upgrade"] = outcome(lambda: Store(legacy_url))

    previous_cwd = Path.cwd()
    try:
        os.chdir(work)
        results["outside_repository_cwd"] = outcome(lambda: Store("sqlite:///:memory:"))
    finally:
        os.chdir(previous_cwd)

    cache = ForecastCache(BrokenRedis())
    results["redis_fail_open"] = {
        "read": outcome(lambda: cache.get("test")),
        "write": outcome(lambda: cache.put("test", {"ok": True})),
        "invalidate_storm": outcome(lambda: cache.invalidate_storm("TEST")),
        "invalidate_model": outcome(lambda: cache.invalidate_model("v1")),
    }
    weather = WeatherCache(BrokenRedis())
    weather.memory["test"] = (float("inf"), {"cached": True})
    results["weather_redis_fail_open"] = {
        "read_with_memory_fallback": outcome(lambda: weather.get("test")),
        "write": outcome(lambda: weather.put("test", {"cached": True}, 600)),
    }

    frame = generate_synthetic_catalogue(n_storms=2, n_fixes=20, seed=42)
    scaler = FeatureScaler(list(FEATURE_COLUMNS)).fit(
        FeatureBuilder().feature_matrix(frame)
    )
    config = DatasetConfig(input_len=4, horizon=(1,))
    plain = TyphoonDataset(frame, config)
    scaled = TyphoonDataset(frame, config, scaler=scaler)
    results["target_coordinate_scaling"] = {
        "raw_target_lat_lon": plain[0]["y_reg"].tolist(),
        "scaled_target_lat_lon": scaled[0]["y_reg"].tolist(),
    }

    class CaptureModel(torch.nn.Module):
        def forward(self, x, mask):
            self.first = x[0, 0, :2].tolist()
            return {
                "reg": torch.zeros((len(x), 1, 2)),
                "cls": torch.zeros((len(x), 1, 7)),
            }

    capture = CaptureModel()
    one_storm = frame[frame.storm_id == frame.storm_id.iloc[0]]
    backtest_storm(capture, one_storm, config=config, scaler=scaler)
    results["backtest_feature_scaling"] = {
        "backtest_first_lat_lon_features": capture.first,
        "training_first_lat_lon_features": scaled[0]["x"][0, :2].tolist(),
    }
    results["promotion_nan_metrics"] = outcome(
        lambda: PromotionPolicy(100, 0.8).validate(
            {"mean_error_km": float("nan"), "calibration_coverage": float("nan")}
        )
    )

    batch = demo_batches()[0]
    request = ForecastRequest(storm_id=batch.storm_id, observations=batch.observations)
    manifest = {
        "version": "review-v1",
        "dataset_version": "synthetic-review",
        "feature_schema_sha256": "real-feature-hash",
        "files": {"scaler.json": "real-scaler-hash"},
        "validation_radius_km": {str(h): h * 5 for h in request.horizons},
        "uncertainty_method": "illustrative heuristic; not calibrated coverage",
    }
    service = TyphoonForecaster(
        artifact=Path("injected-fixture"),
        bundle_loader=lambda _: {"manifest": manifest},
        bundle_predictor=lambda bundle, fixes, horizons: (
            [(fixes[-1].lat, fixes[-1].lon)] * len(horizons),
            ["TS"] * len(horizons),
        ),
    )
    response = service.forecast(request)
    results["model_response_metadata"] = {
        "manifest_uncertainty": manifest["uncertainty_method"],
        "response_uncertainty": response.uncertainty_method,
        "response_feature_schema": response.feature_schema_version,
        "response_scaler": response.scaler_version,
    }

    store = Store("sqlite:///:memory:")
    memory = MemoryRedis()
    worker_cache = ForecastCache(memory)
    baseline = TyphoonForecaster()
    update(store, baseline, [batch], cache=worker_cache)
    api_key = worker_cache.key(
        storm_id=request.storm_id,
        input_revision=request.model_dump(mode="json"),
        model_revision=baseline.version,
    )
    results["worker_api_cache_key"] = {
        "worker_entries": len(memory.values),
        "api_key_found": api_key in memory.values,
    }
    app = create_app(
        Settings(_env_file=None, cache_enabled=False, api_key="review-only"),
        store=store,
        forecaster=baseline,
    )
    logging.disable(logging.CRITICAL)
    with TestClient(app) as client:
        results["deployment_api_contract"] = {
            "weather_bundle": client.get(
                "/api/weather/bundle?location_id=da-nang"
            ).status_code,
            "ai_chat": client.post(
                "/api/ai/chat", json={"question": "test"}
            ).status_code,
            "metrics_without_auth": client.get("/metrics").status_code,
            "storms_without_auth": client.get("/typhoons/active").status_code,
            "storms_with_auth": client.get(
                "/typhoons/active", headers={"X-API-Key": "review-only"}
            ).status_code,
        }
    store.engine.dispose()

print(json.dumps(results, indent=2, ensure_ascii=True))
