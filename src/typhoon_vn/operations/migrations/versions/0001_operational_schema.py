"""Create the audited operational forecast schema.

Revision ID: 0001_operational_schema
Revises: None
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0001_operational_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "typhoons",
        sa.Column("id", sa.String(80), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("created_at", sa.String(40), nullable=False),
    )
    op.create_table(
        "model_versions",
        sa.Column("version", sa.String(120), primary_key=True),
        sa.Column("dataset_version", sa.String(120), nullable=False),
        sa.Column("artifact_hash", sa.String(64), nullable=True),
        sa.Column("created_at", sa.String(40), nullable=False),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.String(40), primary_key=True),
        sa.Column("subject", sa.String(200), nullable=False, unique=True),
        sa.Column("created_at", sa.String(40), nullable=False),
    )
    op.create_table(
        "observations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "storm_id",
            sa.String(80),
            sa.ForeignKey("typhoons.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("timestamp", sa.String(40), nullable=False),
        sa.Column("source", sa.String(200), nullable=False),
        sa.Column("source_revision", sa.String(64), nullable=False),
        sa.Column("lat", sa.Float(), nullable=False),
        sa.Column("lon", sa.Float(), nullable=False),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.CheckConstraint("lat >= -90 AND lat <= 90", name="ck_observation_lat"),
        sa.CheckConstraint("lon >= -180 AND lon <= 180", name="ck_observation_lon"),
        sa.UniqueConstraint(
            "storm_id",
            "timestamp",
            "source",
            "source_revision",
            name="uq_observation_revision",
        ),
    )
    op.create_index(
        "ix_observations_storm_time", "observations", ["storm_id", "timestamp"]
    )
    op.create_table(
        "forecasts",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("run_id", sa.String(64), nullable=False, unique=True),
        sa.Column(
            "storm_id",
            sa.String(80),
            sa.ForeignKey("typhoons.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("issue_time", sa.String(40), nullable=False),
        sa.Column("generated_at", sa.String(40), nullable=False),
        sa.Column("model_version", sa.String(120), nullable=False),
        sa.Column("dataset_version", sa.String(120), nullable=False),
        sa.Column("input_revision", sa.String(64), nullable=False),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["model_version"], ["model_versions.version"]),
    )
    op.create_index("ix_forecasts_storm_issue", "forecasts", ["storm_id", "issue_time"])
    op.create_table(
        "forecast_points",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "forecast_id",
            sa.String(64),
            sa.ForeignKey("forecasts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("horizon_hours", sa.Integer(), nullable=False),
        sa.Column("valid_time", sa.String(40), nullable=False),
        sa.Column("lat", sa.Float(), nullable=False),
        sa.Column("lon", sa.Float(), nullable=False),
        sa.Column("radius_km", sa.Float(), nullable=False),
        sa.Column("cone_geojson", sa.Text(), nullable=False),
        sa.CheckConstraint("horizon_hours > 0", name="ck_forecast_horizon"),
        sa.CheckConstraint("radius_km >= 0", name="ck_forecast_radius"),
        sa.UniqueConstraint(
            "forecast_id", "horizon_hours", name="uq_forecast_point_horizon"
        ),
    )
    op.create_index("ix_forecast_points_valid_time", "forecast_points", ["valid_time"])
    op.create_table(
        "subscriptions",
        sa.Column("id", sa.String(40), primary_key=True),
        sa.Column(
            "owner_id",
            sa.String(40),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.Column("created_at", sa.String(40), nullable=False),
    )
    op.create_table(
        "alerts",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column(
            "subscription_id",
            sa.String(40),
            sa.ForeignKey("subscriptions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "forecast_id",
            sa.String(64),
            sa.ForeignKey("forecasts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("storm_id", sa.String(80), nullable=False),
        sa.Column("created_at", sa.String(40), nullable=False),
        sa.Column("payload", sa.Text(), nullable=False),
    )
    op.create_index(
        "ix_alerts_subscription_storm",
        "alerts",
        ["subscription_id", "storm_id", "created_at"],
    )

    if op.get_bind().dialect.name == "postgresql":
        op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
        op.execute(
            "ALTER TABLE observations ADD COLUMN location geometry(Point, 4326) "
            "GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(lon, lat), 4326)) STORED"
        )
        op.execute(
            "CREATE INDEX ix_observations_location_gist "
            "ON observations USING GIST (location)"
        )
        op.execute(
            "ALTER TABLE forecast_points ADD COLUMN cone geometry(Polygon, 4326) "
            "GENERATED ALWAYS AS "
            "(ST_SetSRID(ST_GeomFromGeoJSON(cone_geojson), 4326)) STORED"
        )
        op.execute(
            "CREATE INDEX ix_forecast_points_cone_gist "
            "ON forecast_points USING GIST (cone)"
        )


def downgrade() -> None:
    op.drop_table("alerts")
    op.drop_table("subscriptions")
    op.drop_table("forecast_points")
    op.drop_table("forecasts")
    op.drop_table("observations")
    op.drop_table("users")
    op.drop_table("model_versions")
    op.drop_table("typhoons")
