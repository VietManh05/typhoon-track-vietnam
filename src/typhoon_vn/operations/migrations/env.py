"""Alembic environment: reuse a passed connection or build one from the URL."""

from alembic import context
from sqlalchemy import create_engine

from typhoon_vn.operations.store import metadata

config = context.config


def _run(connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=metadata,
        render_as_batch=connection.dialect.name == "sqlite",
    )
    with context.begin_transaction():
        context.run_migrations()


connection = config.attributes.get("connection")
if connection is not None:
    _run(connection)
else:
    from typhoon_vn.settings import Settings

    url = config.get_main_option("sqlalchemy.url") or (
        Settings().operational_database_url
    )
    with create_engine(url).begin() as conn:
        _run(conn)
