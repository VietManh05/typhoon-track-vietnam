"""Fail if the served dashboard differs from a fresh ``viz/frontend`` build.

FastAPI serves ``src/typhoon_vn/dashboard``, a committed copy of
``viz/frontend/dist``. Run after ``npm run build``::

    python scripts/check_dashboard_sync.py

Trailing whitespace and final newlines are normalised because pre-commit
fixers rewrite them in the committed copy.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "viz/frontend/dist"
SERVED = ROOT / "src/typhoon_vn/dashboard"


def _files(root: Path) -> dict[str, Path]:
    return {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file()
    }


def _normalised(path: Path) -> bytes:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    return "\n".join(lines).rstrip("\n").encode("utf-8")


def main() -> int:
    if not BUILD.is_dir():
        print(f"missing build output: {BUILD} (run npm run build)", file=sys.stderr)
        return 2
    built, served = _files(BUILD), _files(SERVED)
    problems = [f"only in build: {name}" for name in sorted(built.keys() - served)]
    problems += [f"only in served: {name}" for name in sorted(served.keys() - built)]
    problems += [
        f"content differs: {name}"
        for name in sorted(built.keys() & served.keys())
        if _normalised(built[name]) != _normalised(served[name])
    ]
    if problems:
        print("served dashboard is stale; rebuild and copy dist:", file=sys.stderr)
        print("\n".join(f"  {problem}" for problem in problems), file=sys.stderr)
        return 1
    print(f"dashboard in sync ({len(built)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
