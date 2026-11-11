"""Alembic runtime configuration for Typhoon VN operational storage."""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from typhoon_vn.operations.store import metadata

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = metadata


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        version_table=config.attributes.get("version_table", "alembic_version"),
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    supplied_connection = config.attributes.get("connection")
    connectable = supplied_connection or engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    def migrate(connection) -> None:
        if connection.dialect.name == "sqlite":
            connection.exec_driver_sql("PRAGMA foreign_keys=ON")
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            version_table=config.attributes.get("version_table", "alembic_version"),
            render_as_batch=connection.dialect.name == "sqlite",
        )
        with context.begin_transaction():
            context.run_migrations()
        if supplied_connection is None and connection.in_transaction():
            connection.commit()

    if supplied_connection is not None:
        migrate(supplied_connection)
    else:
        with connectable.connect() as connection:
            migrate(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
