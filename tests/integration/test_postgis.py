"""PostGIS acceptance test; enabled only with an operator-provided test URL."""

from __future__ import annotations

import os

import pytest
from sqlalchemy import create_engine, inspect, text

from typhoon_vn.operations.store import downgrade_database, migrate_database

POSTGIS_TEST_URL = os.getenv("POSTGIS_TEST_URL")
pytestmark = pytest.mark.skipif(
    not POSTGIS_TEST_URL,
    reason="POSTGIS_TEST_URL is required for the real PostGIS acceptance gate",
)


def test_postgis_migration_geometry_gist_constraints_and_downgrade() -> None:
    assert POSTGIS_TEST_URL is not None
    downgrade_database(POSTGIS_TEST_URL)
    migrate_database(POSTGIS_TEST_URL)
    engine = create_engine(POSTGIS_TEST_URL)
    schema = inspect(engine)
    observation_indexes = {item["name"] for item in schema.get_indexes("observations")}
    point_indexes = {item["name"] for item in schema.get_indexes("forecast_points")}
    assert "ix_observations_location_gist" in observation_indexes
    assert "ix_forecast_points_cone_gist" in point_indexes
    with engine.connect() as connection:
        assert connection.execute(text("SELECT PostGIS_Version()")).scalar_one()
        srids = connection.execute(
            text(
                "SELECT Find_SRID('public', 'observations', 'location'), "
                "Find_SRID('public', 'forecast_points', 'cone')"
            )
        ).one()
        assert srids == (4326, 4326)
        connection.commit()
        with connection.begin():
            connection.execute(
                text(
                    "INSERT INTO typhoons (id, name, created_at) "
                    "VALUES ('s09-storm', 'S09', '2026-09-19T00:00:00Z')"
                )
            )
            connection.execute(
                text(
                    "INSERT INTO observations "
                    "(storm_id, timestamp, source, source_revision, lat, lon, payload) "
                    "VALUES ('s09-storm', '2026-09-19T00:00:00Z', 'test', 's09-rev', 16, 108, '{}')"
                )
            )
            connection.execute(
                text(
                    "INSERT INTO model_versions "
                    "(version, dataset_version, artifact_hash, created_at) "
                    "VALUES ('s09-model', 's09-data', NULL, '2026-09-19T00:00:00Z')"
                )
            )
            connection.execute(
                text(
                    "INSERT INTO forecasts "
                    "(id, run_id, storm_id, issue_time, generated_at, model_version, "
                    "dataset_version, input_revision, payload) VALUES "
                    "('s09-forecast', 's09-run', 's09-storm', '2026-09-19T00:00:00Z', "
                    "'2026-09-19T00:00:00Z', 's09-model', 's09-data', 's09-rev', '{}')"
                )
            )
            connection.execute(
                text(
                    "INSERT INTO forecast_points "
                    "(forecast_id, horizon_hours, valid_time, lat, lon, radius_km, cone_geojson) "
                    "VALUES ('s09-forecast', 6, '2026-09-19T06:00:00Z', 16, 108, 20, "
                    '\'{"type":"Polygon","coordinates":[[[107.5,15.5],[108.5,15.5],'
                    "[108.5,16.5],[107.5,16.5],[107.5,15.5]]]}')"
                )
            )
            assert (
                connection.execute(
                    text(
                        "SELECT COUNT(*) FROM forecast_points fp "
                        "JOIN observations o ON o.storm_id = 's09-storm' "
                        "WHERE ST_Intersects(fp.cone, o.location)"
                    )
                ).scalar_one()
                == 1
            )
            assert (
                connection.execute(
                    text(
                        "SELECT ST_Intersects(fp.cone, ST_SetSRID(ST_Point(108.5, 16), 4326)) "
                        "FROM forecast_points fp WHERE fp.forecast_id = 's09-forecast'"
                    )
                ).scalar_one()
                is True
            )
    engine.dispose()
    downgrade_database(POSTGIS_TEST_URL)
