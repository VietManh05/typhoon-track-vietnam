"""Archive the exact pre-Alembic schema without removing any rows.

Stop old writers before adoption. Irreversible automatically: restore a backup
to roll back the application; archives remain available for manual recovery.
"""

import sqlalchemy as sa
from alembic import op

revision = "legacy_0001_archive"
down_revision = None
branch_labels = None
depends_on = None

LEGACY = {
    "typhoons": {"id", "name"},
    "observations": {"storm_id", "timestamp", "payload"},
    "forecasts": {"id", "storm_id", "issue_time", "generated_at", "payload"},
    "subscriptions": {"id", "payload"},
    "alerts": {"id", "subscription_id", "storm_id", "created_at", "payload"},
    "schema_versions": {"version"},
}


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = set(inspector.get_table_names())
    for name, columns in LEGACY.items():
        if (
            name not in tables
            or {c["name"] for c in inspector.get_columns(name)} != columns
        ):
            raise ValueError(
                f"Unrecognized legacy schema: {name}; restore/inspect before migration"
            )
        if "legacy_v1_" + name in tables:
            raise ValueError("Legacy archive already exists without its revision")
    versions = (
        conn.exec_driver_sql("SELECT version FROM schema_versions").scalars().all()
    )
    if versions not in ([], [1]):
        raise ValueError("Unsupported legacy schema version")
    quote = conn.dialect.identifier_preparer.quote
    for name in LEGACY:
        # PostgreSQL index names survive a table rename and would clash with 0001.
        if conn.dialect.name == "postgresql":
            indexes = (
                conn.execute(
                    sa.text(
                        "SELECT indexname FROM pg_indexes WHERE schemaname = current_schema() AND tablename = :name"
                    ),
                    {"name": name},
                )
                .scalars()
                .all()
            )
            for index in indexes:
                conn.exec_driver_sql(
                    f"ALTER INDEX {quote(index)} RENAME TO {quote('legacy_v1_' + index)}"
                )
        op.rename_table(name, "legacy_v1_" + name)


def downgrade():
    raise RuntimeError("Legacy adoption is forward-only; restore a verified backup")
