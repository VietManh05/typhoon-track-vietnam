"""Use the same runtime with a separate legacy adoption revision table."""

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).parents[1] / "migrations" / "env.py"))
