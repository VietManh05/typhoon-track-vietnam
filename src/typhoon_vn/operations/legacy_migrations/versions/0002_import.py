"""Backfill the audited schema from retained legacy tables, in one transaction."""

import hashlib
import json
from datetime import datetime, timezone

import sqlalchemy as sa
from alembic import op

revision = "legacy_0002_import"
down_revision = "legacy_0001_archive"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    meta = sa.MetaData()
    names = (
        "typhoons",
        "observations",
        "forecasts",
        "forecast_points",
        "model_versions",
        "subscriptions",
        "alerts",
    )
    tables = {name: sa.Table(name, meta, autoload_with=conn) for name in names}
    now = datetime.now(timezone.utc).isoformat()

    def rows(name):
        table = sa.Table("legacy_v1_" + name, meta, autoload_with=conn)
        return conn.execute(sa.select(table)).mappings()

    storm_ids = set()

    def ensure_storm(identifier, name=None):
        if identifier not in storm_ids:
            conn.execute(
                tables["typhoons"]
                .insert()
                .values(id=identifier, name=name or identifier, created_at=now)
            )
            storm_ids.add(identifier)

    for row in rows("typhoons"):
        ensure_storm(row["id"], row["name"])
    for row in rows("observations"):
        payload = json.loads(row["payload"])
        ensure_storm(row["storm_id"])
        conn.execute(
            tables["observations"]
            .insert()
            .values(
                storm_id=row["storm_id"],
                timestamp=row["timestamp"],
                source=payload.get("source", "legacy-unknown"),
                source_revision=hashlib.sha256(row["payload"].encode()).hexdigest(),
                lat=payload["lat"],
                lon=payload["lon"],
                payload=row["payload"],
            )
        )
    models = set()
    forecast_ids = set()
    for row in rows("forecasts"):
        payload = json.loads(row["payload"])
        version = payload.get("model_version", "legacy-unknown")
        dataset = payload.get("dataset_version", "legacy-unknown")
        created = row["generated_at"] or now
        ensure_storm(row["storm_id"])
        if version not in models:
            conn.execute(
                tables["model_versions"]
                .insert()
                .values(
                    version=version,
                    dataset_version=dataset,
                    artifact_hash=None,
                    created_at=created,
                )
            )
            models.add(version)
        payload.setdefault("run_id", row["id"])
        payload.setdefault("input_revision", row["id"])
        conn.execute(
            tables["forecasts"]
            .insert()
            .values(
                id=row["id"],
                run_id=payload["run_id"],
                storm_id=row["storm_id"],
                issue_time=row["issue_time"],
                generated_at=created,
                model_version=version,
                dataset_version=dataset,
                input_revision=payload["input_revision"],
                payload=json.dumps(payload),
            )
        )
        forecast_ids.add(row["id"])
        for point in payload.get("points", []):
            conn.execute(
                tables["forecast_points"]
                .insert()
                .values(
                    forecast_id=row["id"],
                    horizon_hours=point["horizon_hours"],
                    valid_time=point["valid_time"],
                    lat=point["lat"],
                    lon=point["lon"],
                    radius_km=point["radius_km"],
                    cone_geojson=json.dumps(point["cone"]),
                )
            )
    subscription_ids = set()
    for row in rows("subscriptions"):
        conn.execute(
            tables["subscriptions"]
            .insert()
            .values(
                id=row["id"],
                owner_id=None,
                payload=row["payload"],
                created_at=now,
            )
        )
        subscription_ids.add(row["id"])
    for row in rows("alerts"):
        payload = json.loads(row["payload"])
        forecast_id = payload.get("forecast_id")
        if (
            forecast_id not in forecast_ids
            or row["subscription_id"] not in subscription_ids
        ):
            raise ValueError(
                "Legacy alert has missing forecast/subscription; repair references before adoption"
            )
        conn.execute(
            tables["alerts"]
            .insert()
            .values(
                id=row["id"],
                subscription_id=row["subscription_id"],
                forecast_id=forecast_id,
                storm_id=row["storm_id"],
                created_at=row["created_at"] or now,
                payload=row["payload"],
            )
        )


def downgrade():
    raise RuntimeError("Legacy adoption is forward-only; restore a verified backup")
