"""Pytest configuration: ensure the source tree is importable."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).parent / "src"
TEST_TEMP = (Path(__file__).parent / ".pytest-temp").resolve()
TEST_TEMP.mkdir(exist_ok=True)
for variable in ("TEMP", "TMP", "TMPDIR"):
    os.environ[variable] = str(TEST_TEMP)
tempfile.tempdir = str(TEST_TEMP)
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
