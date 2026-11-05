"""Alembic migrations for the operational store (SQLite and PostgreSQL).

``upgrade(engine)`` is what ``Store`` runs on start-up. Databases created by
the pre-Alembic ``metadata.create_all`` path are stamped at the initial
revision first, so existing rows are kept.

CLI equivalent::

    alembic -c src/typhoon_vn/operations/migrations/alembic.ini upgrade head
"""

from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import inspect
from sqlalchemy.engine import Engine

HERE = Path(__file__).resolve().parent
INITIAL = "0001"


def _config() -> Config:
    config = Config()
    config.set_main_option("script_location", str(HERE))
    return config


HEAD = ScriptDirectory.from_config(_config()).get_current_head()


def upgrade(engine: Engine, revision: str = "head") -> None:
    config = _config()
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        current = MigrationContext.configure(connection).get_current_revision()
        if current is None and inspect(connection).has_table("typhoons"):
            # Legacy schema built by metadata.create_all == revision 0001.
            command.stamp(config, INITIAL)
        command.upgrade(config, revision)
