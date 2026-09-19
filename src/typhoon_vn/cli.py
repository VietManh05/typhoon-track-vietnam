"""Command-line entry points for local data and training workflows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="typhoon-vn")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("clean-data", help="Reserved cleaning command")
    train = sub.add_parser("train", help="Train and export a validated model bundle")
    train.add_argument("--config", type=Path, required=True)
    train.add_argument("--output-dir", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "clean-data":
        print("No raw data modified; use the ingestion cleaning pipeline explicitly.")
        return 0
    from typhoon_vn.training.run import run_training_file

    result = run_training_file(args.config, args.output_dir)
    print(
        json.dumps(
            {
                "status": "ok",
                "manifest": str(result["manifest"]),
                "epochs": len(result["history"]),
                "data_kind": "synthetic-demo",
                "warning": "Smoke training only; not a real-storm skill metric.",
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
