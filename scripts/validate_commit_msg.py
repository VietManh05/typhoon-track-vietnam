"""Validate Conventional Commit message files without dependencies."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TYPES = ("feat", "fix", "docs", "test", "refactor", "build", "ci", "chore", "perf")
HEADER = re.compile(
    r"^(?:" + "|".join(TYPES) + r")(?:\([a-z0-9][a-z0-9._/-]*\))?!?: [^\s].{0,70}$"
)


def validate_message(message: str) -> list[str]:
    lines = message.replace("\r\n", "\n").split("\n")
    header = lines[0] if lines else ""
    errors: list[str] = []
    if not HEADER.fullmatch(header):
        errors.append(
            "header must use an allowed type, optional scope, colon, and <=72 characters"
        )
    if header.endswith("."):
        errors.append("header summary must not end with a period")
    if len(lines) > 1 and lines[1].strip():
        errors.append("body must be separated from header by a blank line")
    breaking_header = bool(re.match(r"^[a-z]+(?:\([^)]+\))?!:", header))
    breaking_footer = any(line.startswith("BREAKING CHANGE: ") for line in lines[2:])
    malformed = any(
        line.startswith("BREAKING CHANGE") and not line.startswith("BREAKING CHANGE: ")
        for line in lines[2:]
    )
    if malformed:
        errors.append("breaking footer must use BREAKING CHANGE: description")
    if breaking_header and not breaking_footer:
        errors.append("a ! header requires a BREAKING CHANGE footer")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("message_file", type=Path)
    args = parser.parse_args(argv)
    errors = validate_message(args.message_file.read_text(encoding="utf-8"))
    if errors:
        print("Invalid Conventional Commit message:")
        for error in errors:
            print("- " + error)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
