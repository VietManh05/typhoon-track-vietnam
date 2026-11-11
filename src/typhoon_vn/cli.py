"""Command-line entry points for local data and training workflows."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="typhoon-vn")
    sub = parser.add_subparsers(dest="command", required=True)
    clean = sub.add_parser(
        "clean-data", help="Clean raw observations and export auditable features"
    )
    clean.add_argument("--input", type=Path, required=True)
    clean.add_argument("--output-dir", type=Path, required=True)
    clean.add_argument("--config", type=Path)
    train = sub.add_parser("train", help="Train and export a validated model bundle")
    train.add_argument("--config", type=Path, required=True)
    train.add_argument("--output-dir", type=Path, required=True)
    nchmf = sub.add_parser(
        "scrape-nchmf", help="Fetch public NCHMF weather with provenance"
    )
    nchmf.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "scrape-nchmf":
        from typhoon_vn.weather.nchmf import NchmfService

        value = NchmfService().get()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(
            json.dumps(
                {
                    "status": "ok",
                    "observations": len(value["observations"]),
                    "bulletins": len(value["bulletins"]),
                    "output": str(args.output),
                }
            )
        )
        return 0
    if args.command == "clean-data":
        if not args.input.is_file():
            raise SystemExit(f"input file does not exist: {args.input}")
        if args.config is not None and not args.config.is_file():
            raise SystemExit(f"config file does not exist: {args.config}")
        config = (
            json.loads(args.config.read_text(encoding="utf-8")) if args.config else {}
        )
        unknown = set(config) - {"n_lags"}
        if unknown:
            raise SystemExit(f"unsupported clean-data config keys: {sorted(unknown)}")
        from pandas import read_csv, read_parquet

        from typhoon_vn.features.build import FeatureBuilder
        from typhoon_vn.features.pipeline import Phase2Pipeline

        raw_hash = hashlib.sha256(args.input.read_bytes()).hexdigest()
        loader = read_parquet if args.input.suffix.lower() == ".parquet" else read_csv
        frame = loader(args.input)
        pipeline = Phase2Pipeline(
            builder=FeatureBuilder(n_lags=int(config.get("n_lags", 3)))
        )
        featured, report = pipeline.run([frame])
        args.output_dir.mkdir(parents=True, exist_ok=True)
        output = pipeline.export(featured, report, args.output_dir / "features.parquet")
        after_hash = hashlib.sha256(args.input.read_bytes()).hexdigest()
        if raw_hash != after_hash:
            raise RuntimeError("raw input changed during clean-data execution")
        provenance = {
            "input": str(args.input.resolve()),
            "input_sha256": raw_hash,
            "output": str(output.resolve()),
            "rows": len(featured),
            "config": config,
        }
        provenance_path = args.output_dir / "provenance.json"
        provenance_path.write_text(
            json.dumps(provenance, indent=2, sort_keys=True), encoding="utf-8"
        )
        print(json.dumps({"status": "ok", **provenance}, sort_keys=True))
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
