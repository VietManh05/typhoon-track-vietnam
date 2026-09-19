"""Contribution documentation must match the repository workflow."""

from pathlib import Path


def test_contributing_matches_verified_workflow() -> None:
    text = Path("CONTRIBUTING.md").read_text(encoding="utf-8")
    required = [
        "Python 3.11",
        ".[api,train,ingestion,dev]",
        "develop",
        "feature/<task-id>-<short-slug>",
        "python -m pytest -q --basetemp=.pytest-local",
        "Conventional Commits",
        "synthetic",
        "official-warning disclaimer",
        "https://github.com/VietManh05/typhoon-track-vietnam.git",
    ]
    assert all(item in text for item in required)
    assert "no upstream remote" not in text
    assert "from `main`" not in text
    assert Path("docs/branching.md").is_file()
