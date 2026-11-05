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
    worker = sub.add_parser(
        "worker", help="Ingest observations and refresh forecasts (no messages sent)"
    )
    source = worker.add_mutually_exclusive_group(required=True)
    source.add_argument("--snapshot", type=Path, help="JSON list of batches")
    source.add_argument(
        "--ibtracs-active",
        action="store_true",
        help="NOAA IBTrACS ACTIVE feed (keyless; lags by up to days)",
    )
    worker.add_argument("--db", help="override OPERATIONAL_DATABASE_URL")
    worker.add_argument("--interval", type=int, default=3600, help="seconds")
    worker.add_argument("--once", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "clean-data":
        print("No raw data modified; use the ingestion cleaning pipeline explicitly.")
        return 0
    if args.command == "worker":
        return _worker(args)
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


def _worker(args: argparse.Namespace) -> int:
    import logging

    from typhoon_vn.inference.service import TyphoonForecaster
    from typhoon_vn.operations.store import Store
    from typhoon_vn.operations.worker import run_worker, snapshot_source
    from typhoon_vn.settings import Settings

    logging.basicConfig(level=logging.INFO)
    settings = Settings()
    store = Store(args.db or settings.operational_database_url)
    forecaster = TyphoonForecaster(
        settings.model_artifact, allow_baseline=settings.allow_baseline
    )
    if args.snapshot:
        source = snapshot_source(args.snapshot)
    else:
        from typhoon_vn.operations.live import fetch_ibtracs_active

        def source():
            return fetch_ibtracs_active(settings.data_dir)

    run_worker(store, forecaster, source=source, interval=args.interval, once=args.once)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
