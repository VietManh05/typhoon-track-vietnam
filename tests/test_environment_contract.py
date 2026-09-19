"""Repository environment and configuration contracts."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from typhoon_vn.settings import Settings

ROOT = Path(__file__).resolve().parents[1]


def _dependency_names(specs: list[str]) -> set[str]:
    return {
        re.split(r"(?=[<>=!~\[])", specification, maxsplit=1)[0].lower()
        for specification in specs
    }


def test_python_and_dependency_groups_are_reproducible():
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = metadata["project"]
    extras = project["optional-dependencies"]

    assert (ROOT / ".python-version").read_text(encoding="utf-8").strip() == "3.11.9"
    assert project["requires-python"] == ">=3.11,<3.12"
    assert {"torch", "pandas", "numpy", "scikit-learn"} <= _dependency_names(
        extras["train"]
    )
    assert {"fastapi", "uvicorn", "sqlalchemy", "alembic"} <= _dependency_names(
        extras["api"]
    )
    assert {"mlflow", "optuna", "dvc"} <= _dependency_names(extras["experiment"])
    assert {"pytest", "black", "isort", "flake8"} <= _dependency_names(extras["dev"])


def test_setup_target_installs_all_supported_extras():
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    assert ".[api,train,ingestion,dev,experiment]" in makefile


def test_env_template_and_settings_loader(monkeypatch):
    template = (ROOT / ".env.example").read_text(encoding="utf-8")
    for key in (
        "APP_ENV",
        "DATA_DIR",
        "DATABASE_URL",
        "REDIS_URL",
        "MODEL_REGISTRY_URI",
    ):
        assert re.search(rf"(?m)^{key}=", template)

    monkeypatch.setenv("APP_ENV", "contract-test")
    monkeypatch.setenv("DEBUG", "false")
    settings = Settings(_env_file=None)
    assert settings.app_env == "contract-test"
    assert settings.debug is False
