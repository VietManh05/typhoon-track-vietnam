"""Build the small, licence-safe Phase-2 DVC fixture deterministically."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from typhoon_vn.features.pipeline import Phase2Pipeline


def build(source: Path, destination: Path) -> dict[str, object]:
    raw = pd.read_csv(source)
    featured, report = Phase2Pipeline().run([raw])
    Phase2Pipeline().export(featured, report, destination)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    manifest = {
        "source": source.as_posix(),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "output": destination.as_posix(),
        "output_sha256": digest,
        "rows": len(featured),
        "synthetic_fixture": True,
    }
    manifest_path = destination.with_suffix(".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    build(args.source, args.destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
