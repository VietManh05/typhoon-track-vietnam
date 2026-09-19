"""Portable transactional storage; SQLite locally, PostgreSQL in deployment."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import RLock
from uuid import uuid4

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    insert,
    select,
)
from sqlalchemy.pool import StaticPool

metadata = MetaData()
storms = Table(
    "typhoons",
    metadata,
    Column("id", String(80), primary_key=True),
    Column("name", String(120), nullable=False),
)
observations = Table(
    "observations",
    metadata,
    Column("storm_id", String(80), primary_key=True),
    Column("timestamp", String(40), primary_key=True),
    Column("payload", Text, nullable=False),
)
forecasts = Table(
    "forecasts",
    metadata,
    Column("id", String(64), primary_key=True),
    Column("storm_id", String(80), index=True),
    Column("issue_time", String(40), index=True),
    Column("generated_at", String(40)),
    Column("payload", Text, nullable=False),
)
subscriptions = Table(
    "subscriptions",
    metadata,
    Column("id", String(40), primary_key=True),
    Column("payload", Text, nullable=False),
)
alerts = Table(
    "alerts",
    metadata,
    Column("id", String(64), primary_key=True),
    Column("subscription_id", String(40)),
    Column("storm_id", String(80)),
    Column("created_at", String(40)),
    Column("payload", Text),
)
schema_versions = Table(
    "schema_versions", metadata, Column("version", Integer, primary_key=True)
)


class Store:
    def __init__(self, url):
        options = {}
        if url.startswith("sqlite"):
            options["connect_args"] = {"check_same_thread": False}
            if url.endswith(":memory:"):
                options["poolclass"] = StaticPool
            else:
                Path(url.split("///", 1)[1]).parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(url, **options)
        self.lock = RLock()
        metadata.create_all(self.engine)
        with self.engine.begin() as conn:
            if conn.execute(select(schema_versions)).first() is None:
                conn.execute(insert(schema_versions).values(version=1))

    def upsert_observations(self, batch):
        # SQL upserts are atomic across API/worker processes.
        from sqlalchemy.dialects.postgresql import insert as pg_insert
        from sqlalchemy.dialects.sqlite import insert as sqlite_insert

        upsert = sqlite_insert if self.engine.dialect.name == "sqlite" else pg_insert
        with self.lock, self.engine.begin() as conn:
            statement = upsert(storms).values(id=batch.storm_id, name=batch.name)
            conn.execute(
                statement.on_conflict_do_update(
                    index_elements=["id"], set_={"name": batch.name}
                )
            )
            for fix in batch.observations:
                statement = upsert(observations).values(
                    storm_id=batch.storm_id,
                    timestamp=fix.timestamp.isoformat(),
                    payload=fix.model_dump_json(),
                )
                conn.execute(
                    statement.on_conflict_do_update(
                        index_elements=["storm_id", "timestamp"],
                        set_={"payload": fix.model_dump_json()},
                    )
                )

    def track(self, storm_id):
        from typhoon_vn.api.schemas import Fix

        with self.engine.connect() as conn:
            rows = (
                conn.execute(
                    select(observations.c.payload)
                    .where(observations.c.storm_id == storm_id)
                    .order_by(observations.c.timestamp)
                )
                .scalars()
                .all()
            )
        return [Fix.model_validate_json(row) for row in rows]

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
        with self.engine.begin() as conn:
            statement = upsert(forecasts).values(
                id=forecast.forecast_id,
                storm_id=forecast.storm_id,
                issue_time=forecast.issue_time.isoformat(),
                generated_at=forecast.generated_at.isoformat(),
                payload=forecast.model_dump_json(),
            )
            conn.execute(statement.on_conflict_do_nothing(index_elements=["id"]))

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
                    id=identifier, payload=subscription.model_dump_json()
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
        import hashlib

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
                    storm_id=forecast["storm_id"],
                    created_at=now.isoformat(),
                    payload=json.dumps(draft),
                )
                .on_conflict_do_nothing(index_elements=["id"])
            )
        return result.rowcount > 0
