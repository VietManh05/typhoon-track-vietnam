"""Conventional Commit validation tests."""

import pytest
from scripts.validate_commit_msg import validate_message


@pytest.mark.parametrize(
    "message",
    [
        "feat(ingestion): parse timestamps as UTC",
        "fix: reject naive datetimes",
        "docs(bundle)!: revise artifact contract\n\nBREAKING CHANGE: manifest schema version is now 2",
    ],
)
def test_valid_messages(message: str) -> None:
    assert validate_message(message) == []


@pytest.mark.parametrize(
    "message",
    [
        "Update files",
        "feature(api): unsupported type",
        "fix(api) missing colon",
        "fix(api): ends in a period.",
        "fix(api)!: change response",
        "fix(api): short\nbody without blank line",
        "feat(api): " + "x" * 80,
    ],
)
def test_invalid_messages(message: str) -> None:
    assert validate_message(message)
