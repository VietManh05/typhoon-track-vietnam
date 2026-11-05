"""Alembic environment: reuse a passed connection or build one from the URL."""

from alembic import context
from sqlalchemy import create_engine

from typhoon_vn.operations.store import metadata

config = context.config


def include_name(name, type_, parent_names) -> bool:
    # Only manage our own tables (PostGIS images ship TIGER/topology tables).
    return type_ != "table" or name in metadata.tables


def _run(connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=metadata,
        include_name=include_name,
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
