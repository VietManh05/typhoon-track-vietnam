"""Acceptance and integration tests for Gate G21: Frontend and Dashboard."""

import json
from pathlib import Path

from fastapi.testclient import TestClient

from typhoon_vn.api.app import create_app
from typhoon_vn.settings import Settings


def test_dashboard_static_files_served_by_fastapi():
    """Test that FastAPI cleanly serves the compiled dashboard, assets, and geojson data."""
    app = create_app()
    client = TestClient(app)

    # 1. Health check
    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "ok"

    # 2. Root dashboard page (index.html)
    res_home = client.get("/")
    assert res_home.status_code == 200
    assert "TYPHOON" in res_home.text or "Hệ thống" in res_home.text
    assert "text/html" in res_home.headers["content-type"]

    # 3. Favicon
    res_fav = client.get("/favicon.svg")
    assert res_fav.status_code == 200
    assert "svg" in res_fav.headers["content-type"]

    # 4. GeoJSON data route
    res_geo = client.get("/data/vietnam_provinces.geojson")
    assert res_geo.status_code == 200
    geo_data = res_geo.json()
    assert geo_data["type"] == "FeatureCollection"
    assert len(geo_data["features"]) == 63  # 63 Vietnam provinces

    # 5. Islands data route
    res_islands = client.get("/data/vietnam_islands.json")
    assert res_islands.status_code == 200
    islands_data = res_islands.json()
    assert any("Hoàng Sa" in item["name_vi"] for item in islands_data)
    assert any("Trường Sa" in item["name_vi"] for item in islands_data)
