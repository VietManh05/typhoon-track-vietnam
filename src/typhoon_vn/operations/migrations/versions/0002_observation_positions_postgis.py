"""Observation positions; PostGIS geography + GIST index when available.

Adds portable ``lat``/``lon`` columns to ``observations`` (backfilled from the
JSON payload). On PostgreSQL with the PostGIS extension available, also adds a
generated ``geog geography(Point, 4326)`` column and a GIST index so radius
queries use ``ST_DWithin``. Other databases keep the portable columns only.

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-05
"""

import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def _postgis_available(bind) -> bool:
    if bind.dialect.name != "postgresql":
        return False
    return bool(
        bind.execute(
            sa.text("SELECT 1 FROM pg_available_extensions WHERE name = 'postgis'")
        ).scalar()
    )


def upgrade() -> None:
    bind = op.get_bind()
    with op.batch_alter_table("observations") as batch:
        batch.add_column(sa.Column("lat", sa.Float(), nullable=True))
        batch.add_column(sa.Column("lon", sa.Float(), nullable=True))
    if bind.dialect.name == "postgresql":
        op.execute(
            "UPDATE observations SET lat = (payload::json->>'lat')::double precision, "
            "lon = (payload::json->>'lon')::double precision"
        )
    else:
        op.execute(
            "UPDATE observations SET lat = json_extract(payload, '$.lat'), "
            "lon = json_extract(payload, '$.lon')"
        )
    op.create_index(
        "ix_observations_storm_time", "observations", ["storm_id", "timestamp"]
    )
    if _postgis_available(bind):
        op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
        op.execute(
            "ALTER TABLE observations ADD COLUMN geog geography(Point, 4326) "
            "GENERATED ALWAYS AS "
            "(ST_SetSRID(ST_MakePoint(lon, lat), 4326)::geography) STORED"
        )
        op.execute(
            "CREATE INDEX ix_observations_geog ON observations USING GIST (geog)"
        )


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("DROP INDEX IF EXISTS ix_observations_geog")
        op.execute("ALTER TABLE observations DROP COLUMN IF EXISTS geog")
    op.drop_index("ix_observations_storm_time", table_name="observations")
    with op.batch_alter_table("observations") as batch:
        batch.drop_column("lon")
        batch.drop_column("lat")
