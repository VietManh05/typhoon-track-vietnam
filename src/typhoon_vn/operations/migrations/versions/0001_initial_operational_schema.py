"""Initial operational schema (matches the pre-Alembic create_all layout).

Revision ID: 0001
Revises:
Create Date: 2026-11-05
"""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "typhoons",
        sa.Column("id", sa.String(80), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
    )
    op.create_table(
        "observations",
        sa.Column("storm_id", sa.String(80), primary_key=True),
        sa.Column("timestamp", sa.String(40), primary_key=True),
        sa.Column("payload", sa.Text, nullable=False),
    )
    op.create_table(
        "forecasts",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("storm_id", sa.String(80)),
        sa.Column("issue_time", sa.String(40)),
        sa.Column("generated_at", sa.String(40)),
        sa.Column("payload", sa.Text, nullable=False),
    )
    op.create_index("ix_forecasts_storm_id", "forecasts", ["storm_id"])
    op.create_index("ix_forecasts_issue_time", "forecasts", ["issue_time"])
    op.create_table(
        "subscriptions",
        sa.Column("id", sa.String(40), primary_key=True),
        sa.Column("payload", sa.Text, nullable=False),
    )
    op.create_table(
        "alerts",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("subscription_id", sa.String(40)),
        sa.Column("storm_id", sa.String(80)),
        sa.Column("created_at", sa.String(40)),
        sa.Column("payload", sa.Text),
    )
    op.create_table(
        "schema_versions",
        sa.Column("version", sa.Integer, primary_key=True),
    )


def downgrade() -> None:
    for table in (
        "schema_versions",
        "alerts",
        "subscriptions",
        "forecasts",
        "observations",
        "typhoons",
    ):
        op.drop_table(table)
