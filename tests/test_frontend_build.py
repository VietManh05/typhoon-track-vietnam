"""Acceptance and integration tests for Gate G21: Frontend and Dashboard."""

import re
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from typhoon_vn.api.app import create_app
from typhoon_vn.inference.service import TyphoonForecaster
from typhoon_vn.operations.store import Store
from typhoon_vn.settings import Settings


def test_dashboard_static_files_served_by_fastapi():
    """FastAPI serves the compiled dashboard, assets, and geographic data."""
    app = create_app()
    client = TestClient(app)

    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "ok"

    res_home = client.get("/")
    assert res_home.status_code == 200
    assert "TYPHOON" in res_home.text or "Hệ thống" in res_home.text
    assert "text/html" in res_home.headers["content-type"]
    asset_paths = re.findall(r'(?:src|href)="(/assets/[^"]+)"', res_home.text)
    assert asset_paths
    for asset_path in asset_paths:
        assert client.get(asset_path).status_code == 200

    res_fav = client.get("/favicon.svg")
    assert res_fav.status_code == 200
    assert "svg" in res_fav.headers["content-type"]

    res_geo = client.get("/data/vietnam_provinces.geojson")
    assert res_geo.status_code == 200
    assert "application/geo+json" in res_geo.headers["content-type"]
    geo_data = res_geo.json()
    assert geo_data["type"] == "FeatureCollection"
    assert len(geo_data["features"]) == 63

    res_font = client.get("/fonts/BeVietnamPro-400-vietnamese.woff2")
    assert res_font.status_code == 200
    assert "font/woff2" in res_font.headers["content-type"]

    res_islands = client.get("/data/vietnam_islands.json")
    assert res_islands.status_code == 200
    islands_data = res_islands.json()
    assert any("Hoàng Sa" in item["name_vi"] for item in islands_data)
    assert any("Trường Sa" in item["name_vi"] for item in islands_data)


def test_dashboard_api_vertical_slice_returns_persisted_track(tmp_path):
    """A local observation write reaches both dashboard read endpoints."""
    store = Store(f"sqlite:///{(tmp_path / 'dashboard.db').as_posix()}")
    app = create_app(
        Settings(cache_enabled=False),
        store=store,
        forecaster=TyphoonForecaster(),
    )
    base = datetime.now(timezone.utc).replace(
        minute=0, second=0, microsecond=0
    ) - timedelta(hours=18)
    body = {
        "storm_id": "WP-DASH-E2E",
        "name": "Dashboard integration fixture",
        "observations": [
            {
                "timestamp": (base + timedelta(hours=index * 6)).isoformat(),
                "lat": 13.0 + index * 0.25,
                "lon": 115.0 + index * 0.4,
                "wind_ms": 25.0 + index,
                "pressure_hpa": 990.0 - index,
                "intensity": "TS",
                "source": "local-integration-fixture",
            }
            for index in range(4)
        ],
    }

    with TestClient(app) as client:
        stored = client.post("/observations", json=body)
        assert stored.status_code == 200
        assert stored.json()["forecast_ids"]

        active = client.get("/typhoons/active")
        assert active.status_code == 200
        storm = next(
            item for item in active.json()["typhoons"] if item["id"] == body["storm_id"]
        )
        assert storm["observation_count"] == 4
        assert storm["latest"]["source"] == "local-integration-fixture"

        track = client.get(f"/typhoons/{body['storm_id']}/track")
        assert track.status_code == 200
        payload = track.json()
        assert payload["storm_id"] == body["storm_id"]
        assert len(payload["observations"]) == 4
        assert payload["forecast"]["model_kind"] == "motion-baseline"
        assert len(payload["forecast"]["points"]) == 5

    store.engine.dispose()
