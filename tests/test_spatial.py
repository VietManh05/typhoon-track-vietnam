"""A29-016: spatial storage and radius queries (PostGIS when available)."""

import os
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text

from typhoon_vn.api.app import create_app
from typhoon_vn.api.schemas import Fix, ObservationBatch
from typhoon_vn.inference.service import TyphoonForecaster
from typhoon_vn.operations.store import Store
from typhoon_vn.settings import Settings

NOW = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
DA_NANG = (16.05, 108.2)


def _batch(storm, positions):
    fixes = [
        Fix(
            timestamp=NOW - timedelta(hours=6 * (len(positions) - 1 - i)),
            lat=lat,
            lon=lon,
            source="test",
        )
        for i, (lat, lon) in enumerate(positions)
    ]
    return ObservationBatch(storm_id=storm, name=storm, observations=fixes)


def _seed(store):
    # NEAR ends ~200 km from Da Nang; FAR ends ~1500 km away; OLD is near but stale.
    store.upsert_observations(_batch("NEAR", [(16.5, 112.0), (16.2, 110.1)]))
    store.upsert_observations(_batch("FAR", [(20.0, 125.0), (21.0, 122.0)]))
    old = _batch("OLD", [(16.0, 108.5)])
    old.observations[0].timestamp = NOW - timedelta(days=10)
    store.upsert_observations(old)


def _check(store):
    near = store.storms_near(*DA_NANG, radius_km=500)
    assert [s["storm_id"] for s in near] == ["NEAR"]
    assert 150 < near[0]["distance_km"] < 260
    assert near[0]["lat"] == 16.2 and near[0]["lon"] == 110.1
    assert store.storms_near(*DA_NANG, radius_km=50) == []
    both = store.storms_near(*DA_NANG, radius_km=2000)
    assert [s["storm_id"] for s in both] == ["NEAR", "FAR"]  # nearest first
    with_old = store.storms_near(*DA_NANG, radius_km=500, max_age_hours=24 * 30)
    assert {s["storm_id"] for s in with_old} == {"NEAR", "OLD"}


def test_sqlite_radius_query_uses_latest_position(tmp_path) -> None:
    store = Store(f"sqlite:///{tmp_path / 's.db'}")
    _seed(store)
    _check(store)
    columns = {c["name"] for c in inspect(store.engine).get_columns("observations")}
    assert {"lat", "lon"} <= columns


def test_near_endpoint_is_public_read_and_validated(tmp_path) -> None:
    settings = Settings(
        _env_file=None,
        api_key="k",
        operational_database_url=f"sqlite:///{tmp_path / 'n.db'}",
    )
    store = Store(settings.operational_database_url)
    _seed(store)
    app = create_app(settings=settings, store=store, forecaster=TyphoonForecaster())
    with TestClient(app) as client:
        body = client.get("/typhoons/near", params={"lat": 16.05, "lon": 108.2}).json()
        assert [s["storm_id"] for s in body["typhoons"]] == ["NEAR"]
        assert body["radius_km"] == 500 and "NCHMF" in body["disclaimer"]
        bad = client.get("/typhoons/near", params={"lat": 95, "lon": 108})
        assert bad.status_code == 422
        too_big = client.get(
            "/typhoons/near", params={"lat": 16, "lon": 108, "radius_km": 5000}
        )
        assert too_big.status_code == 422


@pytest.mark.skipif(
    not os.getenv("TEST_POSTGRES_URL"),
    reason="set TEST_POSTGRES_URL to run against PostgreSQL/PostGIS",
)
def test_postgis_geography_index_and_st_dwithin() -> None:
    url = os.environ["TEST_POSTGRES_URL"]
    engine = create_engine(url)
    with engine.begin() as conn:
        for table in (
            "typhoons observations forecasts subscriptions alerts "
            "schema_versions alembic_version"
        ).split():
            conn.exec_driver_sql(f"DROP TABLE IF EXISTS {table} CASCADE")
    store = Store(url)
    _seed(store)
    _check(store)  # served by ST_DWithin on the geography column
    with store.engine.connect() as conn:
        kind = conn.execute(
            text(
                "SELECT udt_name FROM information_schema.columns "
                "WHERE table_name='observations' AND column_name='geog'"
            )
        ).scalar()
        index = conn.execute(
            text(
                "SELECT indexdef FROM pg_indexes "
                "WHERE tablename='observations' AND indexname='ix_observations_geog'"
            )
        ).scalar()
    assert kind == "geography"
    assert index and "gist" in index.lower()
    assert store.spatial_backend == "postgis"
