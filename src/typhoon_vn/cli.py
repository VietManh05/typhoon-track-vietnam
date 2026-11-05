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
    monitor = sub.add_parser(
        "monitor", help="Verify issued forecasts against later observations"
    )
    monitor.add_argument("--db", help="override OPERATIONAL_DATABASE_URL")
    monitor.add_argument("--min-n", type=int, default=20)
    monitor.add_argument("--min-coverage", type=float, default=0.6)
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
    if args.command == "monitor":
        return _monitor(args)
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


def _monitor(args: argparse.Namespace) -> int:
    """Print a skill report; exit 2 when the live cone coverage has degraded."""

    from typhoon_vn.operations.monitoring import assess, verify_forecasts
    from typhoon_vn.operations.store import Store
    from typhoon_vn.settings import Settings

    store = Store(args.db or Settings().operational_database_url)
    report = verify_forecasts(store)
    report["assessment"] = assess(
        report, min_n=args.min_n, min_coverage=args.min_coverage
    )
    print(json.dumps(report, indent=2))
    return 2 if report["assessment"]["status"] == "degraded" else 0


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
        settings.model_artifact,
        allow_baseline=settings.allow_baseline,
        analog_artifact=settings.analog_artifact,
    )
    if args.snapshot:
        source = snapshot_source(args.snapshot)
    else:
        from typhoon_vn.operations.live import fetch_ibtracs_active

        def source():
            return fetch_ibtracs_active(settings.data_dir)

    from typhoon_vn.operations.delivery import DeliveryConfig

    delivery = DeliveryConfig(
        enabled=settings.alert_delivery_enabled,
        url=settings.alert_webhook_url,
        secret=settings.alert_webhook_secret,
    )
    run_worker(
        store,
        forecaster,
        source=source,
        interval=args.interval,
        once=args.once,
        delivery=delivery,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
