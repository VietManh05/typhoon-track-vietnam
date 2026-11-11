"""Public JMA adapter and protected stored route boundaries."""

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from typhoon_vn.api.app import create_app
from typhoon_vn.inference.service import TyphoonForecaster
from typhoon_vn.operations.store import Store
from typhoon_vn.settings import Settings
from typhoon_vn.weather import jma_live


def bulletin():
    issued = datetime.now(timezone.utc).isoformat()
    target = [{"tropicalCyclone": "TC2632", "issue": issued}]
    analysis = {
        "advancedHours": 0,
        "validtime": {"UTC": issued},
        "position": {"deg": [23.6, 127.0]},
        "maximumWind": {"sustained": {"m/s": 30}},
        "pressure": 985,
        "category": {"en": "STS"},
    }
    forecast = {
        "advancedHours": 12,
        "validtime": {"UTC": issued},
        "position": {"deg": [24.6, 127.8]},
        "probabilityCircleRadius": {"km": 55},
        "category": {"en": "TY"},
    }
    specifications = [
        {"issue": {"UTC": issued}, "name": {"en": "Fixture"}},
        analysis,
        forecast,
    ]
    return target, specifications


def test_jma_adapter_preserves_source_and_forecast_kind(monkeypatch):
    target, specifications = bulletin()
    monkeypatch.setattr(
        jma_live,
        "_read",
        lambda path: target if path == "targetTc.json" else specifications,
    )
    active = jma_live.active_typhoons()
    track = jma_live.storm_track("TC2632")
    assert active["feedAvailable"] is True
    assert active["typhoons"][0]["latest"]["source_url"].startswith(
        "https://www.jma.go.jp/"
    )
    assert track["forecast"]["model_kind"] == "external guidance"
    assert len(track["forecast"]["points"][0]["cone"]["coordinates"][0]) == 37


def test_jma_adapter_rejects_stale_bulletin(monkeypatch):
    target, _ = bulletin()
    target[0]["issue"] = "2020-01-01T00:00:00Z"
    monkeypatch.setattr(jma_live, "_read", lambda path: target)
    with pytest.raises(jma_live.JmaLiveError):
        jma_live.active_typhoons()


def test_public_jma_route_does_not_expose_protected_store(monkeypatch):
    target, specifications = bulletin()
    monkeypatch.setattr(
        jma_live,
        "_read",
        lambda path: target if path == "targetTc.json" else specifications,
    )
    app = create_app(
        settings=Settings(
            _env_file=None,
            api_key="review-secret",
            cache_enabled=False,
            operational_database_url="sqlite:///:memory:",
        ),
        store=Store("sqlite:///:memory:"),
        forecaster=TyphoonForecaster(),
    )
    with TestClient(app) as client:
        public = client.get("/typhoons/active?source=jma")
        protected = client.get("/typhoons/active")
    assert public.status_code == 200
    assert protected.status_code == 401
