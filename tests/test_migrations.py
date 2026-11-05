"""G18: Alembic migrations own the operational schema."""

import os

import pytest
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, inspect, select

from typhoon_vn.operations.migrations import HEAD, upgrade
from typhoon_vn.operations.store import Store, metadata, schema_versions

TABLES = {"typhoons", "observations", "forecasts", "subscriptions", "alerts"}


def _revision(engine) -> str | None:
    with engine.connect() as conn:
        return MigrationContext.configure(conn).get_current_revision()


def _diff(engine) -> list:
    def own_tables(name, type_, parent_names) -> bool:
        return type_ != "table" or name in metadata.tables

    with engine.connect() as conn:
        context = MigrationContext.configure(conn, opts={"include_name": own_tables})
        return compare_metadata(context, metadata)


def test_fresh_database_is_migrated_to_head(tmp_path) -> None:
    url = f"sqlite:///{tmp_path / 'fresh.db'}"
    store = Store(url)
    assert _revision(store.engine) == HEAD
    assert TABLES <= set(inspect(store.engine).get_table_names())
    assert _diff(store.engine) == [], "models and migrations drifted"


def test_legacy_create_all_database_is_stamped_without_data_loss(tmp_path) -> None:
    url = f"sqlite:///{tmp_path / 'legacy.db'}"
    engine = create_engine(url)
    metadata.create_all(engine)  # how Store built schemas before Alembic
    with engine.begin() as conn:
        conn.execute(schema_versions.insert().values(version=1))
        conn.exec_driver_sql("INSERT INTO typhoons (id, name) VALUES ('S1', 'Kept')")
    engine.dispose()

    store = Store(url)
    assert _revision(store.engine) == HEAD
    with store.engine.connect() as conn:
        assert conn.exec_driver_sql("SELECT name FROM typhoons").scalar() == "Kept"


def test_upgrade_is_idempotent(tmp_path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'twice.db'}")
    upgrade(engine)
    upgrade(engine)
    assert _revision(engine) == HEAD
    with engine.connect() as conn:
        assert conn.execute(select(schema_versions)).all() == []


@pytest.mark.skipif(
    not os.getenv("TEST_POSTGRES_URL"),
    reason="set TEST_POSTGRES_URL to run against PostgreSQL/PostGIS",
)
def test_postgres_migrates_and_matches_models() -> None:
    engine = create_engine(os.environ["TEST_POSTGRES_URL"])
    with engine.begin() as conn:
        for table in [*TABLES, "schema_versions", "alembic_version"]:
            conn.exec_driver_sql(f"DROP TABLE IF EXISTS {table} CASCADE")
    store = Store(os.environ["TEST_POSTGRES_URL"])
    assert _revision(store.engine) == HEAD
    assert _diff(store.engine) == []
