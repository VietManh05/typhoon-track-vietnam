"""Portable transactional storage; SQLite locally, PostgreSQL in deployment."""

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import RLock
from uuid import uuid4

from sqlalchemy import (
    CheckConstraint,
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    UniqueConstraint,
    create_engine,
    delete,
    event,
    insert,
    inspect,
    select,
)
from sqlalchemy.pool import StaticPool

metadata = MetaData()
storms = Table(
    "typhoons",
    metadata,
    Column("id", String(80), primary_key=True),
    Column("name", String(120), nullable=False),
    Column("created_at", String(40), nullable=False),
)
observations = Table(
    "observations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "storm_id",
        String(80),
        ForeignKey("typhoons.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("timestamp", String(40), nullable=False),
    Column("source", String(200), nullable=False),
    Column("source_revision", String(64), nullable=False),
    Column("lat", Float, nullable=False),
    Column("lon", Float, nullable=False),
    Column("payload", Text, nullable=False),
    CheckConstraint("lat >= -90 AND lat <= 90", name="ck_observation_lat"),
    CheckConstraint("lon >= -180 AND lon <= 180", name="ck_observation_lon"),
    UniqueConstraint(
        "storm_id",
        "timestamp",
        "source",
        "source_revision",
        name="uq_observation_revision",
    ),
)
forecasts = Table(
    "forecasts",
    metadata,
    Column("id", String(64), primary_key=True),
    Column("run_id", String(64), nullable=False, unique=True),
    Column(
        "storm_id",
        String(80),
        ForeignKey("typhoons.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("issue_time", String(40), nullable=False),
    Column("generated_at", String(40), nullable=False),
    Column(
        "model_version",
        String(120),
        ForeignKey("model_versions.version"),
        nullable=False,
    ),
    Column("dataset_version", String(120), nullable=False),
    Column("input_revision", String(64), nullable=False),
    Column("payload", Text, nullable=False),
)
forecast_points = Table(
    "forecast_points",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "forecast_id",
        String(64),
        ForeignKey("forecasts.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("horizon_hours", Integer, nullable=False),
    Column("valid_time", String(40), nullable=False),
    Column("lat", Float, nullable=False),
    Column("lon", Float, nullable=False),
    Column("radius_km", Float, nullable=False),
    Column("cone_geojson", Text, nullable=False),
    CheckConstraint("horizon_hours > 0", name="ck_forecast_horizon"),
    CheckConstraint("radius_km >= 0", name="ck_forecast_radius"),
    UniqueConstraint("forecast_id", "horizon_hours", name="uq_forecast_point_horizon"),
)
model_versions = Table(
    "model_versions",
    metadata,
    Column("version", String(120), primary_key=True),
    Column("dataset_version", String(120), nullable=False),
    Column("artifact_hash", String(64)),
    Column("created_at", String(40), nullable=False),
)
users = Table(
    "users",
    metadata,
    Column("id", String(40), primary_key=True),
    Column("subject", String(200), nullable=False, unique=True),
    Column("created_at", String(40), nullable=False),
)
subscriptions = Table(
    "subscriptions",
    metadata,
    Column("id", String(40), primary_key=True),
    Column("owner_id", String(40), ForeignKey("users.id", ondelete="CASCADE")),
    Column("payload", Text, nullable=False),
    Column("created_at", String(40), nullable=False),
)
alerts = Table(
    "alerts",
    metadata,
    Column("id", String(64), primary_key=True),
    Column(
        "subscription_id",
        String(40),
        ForeignKey("subscriptions.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "forecast_id",
        String(64),
        ForeignKey("forecasts.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("storm_id", String(80), nullable=False),
    Column("created_at", String(40), nullable=False),
    Column("payload", Text, nullable=False),
)


def _migration_config(url, connection=None, *, legacy=False):
    from alembic.config import Config

    config = Config()
    folder = "legacy_migrations" if legacy else "migrations"
    config.set_main_option(
        "script_location", str(Path(__file__).parent / folder).replace("%", "%%")
    )
    config.set_main_option("sqlalchemy.url", url.replace("%", "%%"))
    if connection is not None:
        config.attributes["connection"] = connection
    if legacy:
        config.attributes["version_table"] = "legacy_alembic_version"
    return config


def migrate_database(url: str, revision: str = "head", *, connection=None) -> None:
    """Upgrade a database through versioned migrations, never ``create_all``."""

    from alembic import command

    if connection is None:
        engine = create_engine(url)
        try:
            with engine.connect() as conn:
                migrate_database(url, revision, connection=conn)
        finally:
            engine.dispose()
        return

    # Own one transaction across archival DDL, schema creation and data import.
    with connection.begin():
        if connection.dialect.name == "sqlite":
            connection.exec_driver_sql("PRAGMA foreign_keys=ON")
            connection.exec_driver_sql("BEGIN IMMEDIATE")
        elif connection.dialect.name == "postgresql":
            connection.exec_driver_sql("SELECT pg_advisory_xact_lock(84739201)")
        tables = set(inspect(connection).get_table_names())
        versioned = (
            "alembic_version" in tables
            and connection.exec_driver_sql(
                "SELECT version_num FROM alembic_version"
            ).first()
            is not None
        )
        legacy = "legacy_alembic_version" in tables or (
            "schema_versions" in tables and not versioned
        )
        if legacy and revision != "head":
            raise ValueError("Legacy database adoption requires revision=head")
        if legacy:
            legacy_config = _migration_config(url, connection, legacy=True)
            # Separate versioned schema and data steps; original rows stay archived.
            if "legacy_alembic_version" not in tables:
                command.upgrade(legacy_config, "legacy_0001_archive")
        command.upgrade(_migration_config(url, connection), revision)
        if legacy:
            command.upgrade(legacy_config, "head")


def downgrade_database(url: str, revision: str = "base") -> None:
    """Downgrade a test/local database to a named Alembic revision."""

    from alembic import command

    engine = create_engine(url)
    try:
        if "legacy_alembic_version" in inspect(engine).get_table_names():
            raise RuntimeError(
                "Legacy adoption is forward-only; restore a verified backup"
            )
    finally:
        engine.dispose()
    command.downgrade(_migration_config(url), revision)


class Store:
    def __init__(self, url: str, *, migrate: bool = True):
        options = {}
        if url.startswith("sqlite"):
            options["connect_args"] = {"check_same_thread": False}
            if url.endswith(":memory:"):
                options["poolclass"] = StaticPool
            else:
                Path(url.split("///", 1)[1]).parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(url, **options)
        if self.engine.dialect.name == "sqlite":
            event.listen(
                self.engine,
                "connect",
                lambda connection, _: connection.execute("PRAGMA foreign_keys=ON"),
            )
        self.lock = RLock()
        if migrate:
            if url.endswith(":memory:"):
                with self.engine.connect() as connection:
                    migrate_database(url, connection=connection)
            else:
                self.engine.dispose()
                migrate_database(url)

    def upsert_observations(self, batch):
        # SQL upserts are atomic across API/worker processes.
        from sqlalchemy.dialects.postgresql import insert as pg_insert
        from sqlalchemy.dialects.sqlite import insert as sqlite_insert

        upsert = sqlite_insert if self.engine.dialect.name == "sqlite" else pg_insert
        changed = False
        with self.lock, self.engine.begin() as conn:
            statement = upsert(storms).values(
                id=batch.storm_id,
                name=batch.name,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
            conn.execute(
                statement.on_conflict_do_update(
                    index_elements=["id"], set_={"name": batch.name}
                )
            )
            for fix in batch.observations:
                source_revision = hashlib.sha256(
                    fix.model_dump_json().encode("utf-8")
                ).hexdigest()
                key = (
                    observations.c.storm_id == batch.storm_id,
                    observations.c.timestamp == fix.timestamp.isoformat(),
                    observations.c.source == fix.source,
                )
                current = conn.execute(
                    select(observations.c.source_revision)
                    .where(*key)
                    .order_by(observations.c.id.desc())
                ).scalar()
                if current == source_revision:
                    continue
                changed = True
                # track() serves the newest row, so a revision that returns
                # (A -> B -> A) must be re-inserted rather than left behind B.
                conn.execute(
                    delete(observations).where(
                        *key, observations.c.source_revision == source_revision
                    )
                )
                conn.execute(
                    upsert(observations)
                    .values(
                        storm_id=batch.storm_id,
                        timestamp=fix.timestamp.isoformat(),
                        source=fix.source,
                        source_revision=source_revision,
                        lat=fix.lat,
                        lon=fix.lon,
                        payload=fix.model_dump_json(),
                    )
                    .on_conflict_do_nothing(
                        index_elements=[
                            "storm_id",
                            "timestamp",
                            "source",
                            "source_revision",
                        ]
                    )
                )
        return changed

    def track(self, storm_id):
        from typhoon_vn.api.schemas import Fix

        with self.engine.connect() as conn:
            rows = conn.execute(
                select(
                    observations.c.timestamp,
                    observations.c.payload,
                    observations.c.id,
                )
                .where(observations.c.storm_id == storm_id)
                .order_by(observations.c.timestamp, observations.c.id)
            ).all()
        latest_by_time = {row.timestamp: row.payload for row in rows}
        return [
            Fix.model_validate_json(latest_by_time[timestamp])
            for timestamp in sorted(latest_by_time)
        ]

    def active(self, hours=48):
        threshold = datetime.now(timezone.utc) - timedelta(hours=hours)
        with self.engine.connect() as conn:
            entries = conn.execute(select(storms)).mappings().all()
        results = []
        for entry in entries:
            track = self.track(entry["id"])
            if track and track[-1].timestamp >= threshold:
                results.append(
                    {
                        **dict(entry),
                        "latest": track[-1].model_dump(mode="json"),
                        "observation_count": len(track),
                    }
                )
        return results

    def cached(self, key):
        with self.engine.connect() as conn:
            payload = conn.execute(
                select(forecasts.c.payload).where(forecasts.c.id == key)
            ).scalar()
        return json.loads(payload) if payload else None

    def save_forecast(self, forecast):
        from sqlalchemy.dialects.postgresql import insert as pg_insert
        from sqlalchemy.dialects.sqlite import insert as sqlite_insert

        upsert = sqlite_insert if self.engine.dialect.name == "sqlite" else pg_insert
        input_revision = (
            getattr(forecast, "input_revision", None) or forecast.forecast_id
        )
        run_id = getattr(forecast, "run_id", None) or forecast.forecast_id
        with self.lock, self.engine.begin() as conn:
            conn.execute(
                upsert(storms)
                .values(
                    id=forecast.storm_id,
                    name=forecast.storm_id,
                    created_at=forecast.generated_at.isoformat(),
                )
                .on_conflict_do_nothing(index_elements=["id"])
            )
            conn.execute(
                upsert(model_versions)
                .values(
                    version=forecast.model_version,
                    dataset_version=forecast.dataset_version,
                    artifact_hash=None,
                    created_at=forecast.generated_at.isoformat(),
                )
                .on_conflict_do_nothing(index_elements=["version"])
            )
            statement = upsert(forecasts).values(
                id=forecast.forecast_id,
                run_id=run_id,
                storm_id=forecast.storm_id,
                issue_time=forecast.issue_time.isoformat(),
                generated_at=forecast.generated_at.isoformat(),
                model_version=forecast.model_version,
                dataset_version=forecast.dataset_version,
                input_revision=input_revision,
                payload=forecast.model_dump_json(),
            )
            conn.execute(statement.on_conflict_do_nothing(index_elements=["id"]))
            for point in forecast.points:
                conn.execute(
                    upsert(forecast_points)
                    .values(
                        forecast_id=forecast.forecast_id,
                        horizon_hours=point.horizon_hours,
                        valid_time=point.valid_time.isoformat(),
                        lat=point.lat,
                        lon=point.lon,
                        radius_km=point.radius_km,
                        cone_geojson=json.dumps(point.cone, sort_keys=True),
                    )
                    .on_conflict_do_nothing(
                        index_elements=["forecast_id", "horizon_hours"]
                    )
                )

    def latest_forecast(self, storm_id, issue_time=None):
        query = select(forecasts.c.payload).where(forecasts.c.storm_id == storm_id)
        if issue_time:
            query = query.where(forecasts.c.issue_time == issue_time.isoformat())
        with self.engine.connect() as conn:
            payload = conn.execute(
                query.order_by(
                    forecasts.c.issue_time.desc(), forecasts.c.generated_at.desc()
                )
            ).scalar()
        return json.loads(payload) if payload else None

    def subscribe(self, subscription):
        identifier = str(uuid4())
        with self.engine.begin() as conn:
            conn.execute(
                insert(subscriptions).values(
                    id=identifier,
                    owner_id=None,
                    payload=subscription.model_dump_json(),
                    created_at=datetime.now(timezone.utc).isoformat(),
                )
            )
        return identifier

    def list_subscriptions(self):
        with self.engine.connect() as conn:
            return [
                (r.id, json.loads(r.payload))
                for r in conn.execute(select(subscriptions))
            ]

    def alert_drafts(self):
        with self.engine.connect() as conn:
            return [
                json.loads(r)
                for r in conn.execute(
                    select(alerts.c.payload)
                    .order_by(alerts.c.created_at.desc())
                    .limit(100)
                ).scalars()
            ]

    def record_alert(self, subscription_id, forecast, subscription, closest):
        now = datetime.now(timezone.utc)
        key = hashlib.sha256(
            (subscription_id + forecast["forecast_id"]).encode()
        ).hexdigest()
        with self.lock, self.engine.begin() as conn:
            # Lock subscription row across PostgreSQL workers.
            conn.execute(
                select(subscriptions.c.id)
                .where(subscriptions.c.id == subscription_id)
                .with_for_update()
            ).first()
            previous = conn.execute(
                select(alerts.c.created_at)
                .where(
                    alerts.c.subscription_id == subscription_id,
                    alerts.c.storm_id == forecast["storm_id"],
                )
                .order_by(alerts.c.created_at.desc())
            ).scalar()
            if previous and now - datetime.fromisoformat(previous) < timedelta(
                hours=subscription["cooldown_hours"]
            ):
                return False
            draft = {
                "id": key,
                "label": subscription["label"],
                "storm_id": forecast["storm_id"],
                "forecast_id": forecast["forecast_id"],
                "created_at": now.isoformat(),
                "closest_km": closest,
                "status": "draft",
                "disclaimer": forecast["disclaimer"],
                "message": "Forecast enters your configured radius. Consult NCHMF.",
                "model_version": forecast["model_version"],
                "sources": forecast["sources"],
            }
            from sqlalchemy.dialects.postgresql import insert as pg_insert
            from sqlalchemy.dialects.sqlite import insert as sqlite_insert

            upsert = (
                sqlite_insert if self.engine.dialect.name == "sqlite" else pg_insert
            )
            result = conn.execute(
                upsert(alerts)
                .values(
                    id=key,
                    subscription_id=subscription_id,
                    forecast_id=forecast["forecast_id"],
                    storm_id=forecast["storm_id"],
                    created_at=now.isoformat(),
                    payload=json.dumps(draft),
                )
                .on_conflict_do_nothing(index_elements=["id"])
            )
        return result.rowcount > 0
