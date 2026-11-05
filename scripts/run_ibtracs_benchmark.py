"""Train the LSTM on real IBTrACS WP tracks and compare it with baselines.

Reads ingested raw partitions under ``<data-root>/raw/observations`` (see
``python -m typhoon_vn.ingestion.cli fetch ibtracs`` + ``parse``), keeps
synoptic 6-hourly IBTrACS fixes, cleans them, trains with a whole-storm year
split and writes ``benchmark.json`` + ``benchmark.md`` to the output dir.

Usage::

    python scripts/run_ibtracs_benchmark.py --data-root data \
        --output-dir runs/ibtracs-benchmark --years 1980-2024
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from typhoon_vn.datasets.ibtracs import load_ibtracs_tracks
from typhoon_vn.training.config_loader import load_config
from typhoon_vn.training.registry import PromotionPolicy, promotion_metrics
from typhoon_vn.training.run import run_training


def _years(value: str) -> tuple[int, int]:
    start, _, end = value.partition("-")
    first, last = int(start), int(end or start)
    if first > last:
        raise argparse.ArgumentTypeError("years must be START-END with START<=END")
    return first, last


def _markdown(summary: dict) -> str:
    models = summary["evaluation"]["models"]
    horizons = [row["horizon_h"] for row in next(iter(models.values()))]
    lines = [
        f"# IBTrACS WP benchmark — {summary['dataset_version']}",
        "",
        f"- Years: {summary['years']}; clean rows: {summary['clean_rows']}; "
        f"storms: {summary['storms']}",
        f"- Split (whole storms by final year): {summary['split_storms']}",
        f"- Test years: {summary['test_years']}; "
        f"test storms: {summary['evaluation']['n_storms']}",
        f"- Epochs run: {len(summary['history'])}; "
        f"train seconds: {summary['elapsed_seconds']:.0f}",
        "",
        "Mean great-circle track error (km) on the test split:",
        "",
        "| model | " + " | ".join(f"{h}h" for h in horizons) + " |",
        "|---|" + "---:|" * len(horizons),
    ]
    for name, rows in models.items():
        cells = " | ".join(f"{row['mean_error_km']:.0f}" for row in rows)
        lines.append(f"| {name} | {cells} |")
    counts = " | ".join(str(row["n_forecasts"]) for row in models["lstm"])
    lines += [f"| n forecasts | {counts} |", ""]
    cone = summary["evaluation"].get("cone")
    if cone:
        radius = " | ".join(f"{cone['radius_km'][str(h)]:.0f}" for h in horizons)
        hit = " | ".join(f"{cone['test_coverage'][str(h)]:.0%}" for h in horizons)
        lines += [
            f"Cone calibrated on the {cone['calibration_split']} split for "
            f"{cone['coverage_target']:.0%} coverage:",
            "",
            "| | " + " | ".join(f"{h}h" for h in horizons) + " |",
            "|---|" + "---:|" * len(horizons),
            f"| radius km | {radius} |",
            f"| test coverage | {hit} |",
            "",
        ]
    gate = summary.get("promotion_gate")
    if gate:
        verdict = "PASS" if not gate["failures"] else "FAIL"
        lines += [
            f"Promotion gate at {gate['horizon_h']}h (proposed thresholds): "
            f"**{verdict}**",
            "",
            f"- policy: {gate['policy']}",
            f"- metrics: {gate['metrics']}",
        ]
        lines += [f"- failed: {failure}" for failure in gate["failures"]]
        lines.append("")
    lines.append(
        "Research benchmark only; not an operational warning. CLIPER is a "
        "damped-persistence proxy, not operational CLIPER5."
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--config", type=Path, default=Path("configs/ibtracs_benchmark.yaml")
    )
    parser.add_argument("--years", type=_years, default=(1980, 2024))
    parser.add_argument("--epochs", type=int, help="override training.epochs")
    gate = parser.add_argument_group("promotion gate (proposed defaults)")
    gate.add_argument("--gate-horizon", type=int, default=72)
    gate.add_argument("--max-error-km", type=float, default=550.0)
    gate.add_argument("--min-coverage", type=float, default=0.75)
    gate.add_argument("--max-persistence-ratio", type=float, default=0.9)
    args = parser.parse_args(argv)

    raw_csv = args.data_root / "raw/downloads/ibtracs/ibtracs-wp.csv"
    raw_sha = (
        hashlib.sha256(raw_csv.read_bytes()).hexdigest()
        if raw_csv.exists()
        else "unknown"
    )
    raw, cleaned, quality = load_ibtracs_tracks(args.data_root, args.years)
    if cleaned.empty:
        raise SystemExit("no IBTrACS fixes left after cleaning")

    config = load_config(args.config)
    if args.epochs is not None:
        config.training.epochs = args.epochs
    dataset_version = (
        f"IBTrACS-WP-{args.years[0]}-{args.years[1]}-sha256:{raw_sha[:12]}"
    )
    started = time.perf_counter()
    result = run_training(
        config,
        output_dir=args.output_dir,
        frame=cleaned,
        dataset_version=dataset_version,
    )
    if result["evaluation"] is None:
        raise SystemExit("test split produced no evaluable windows")

    final_year = cleaned.groupby("storm_id")["timestamp"].max().dt.year
    test_years = sorted(set(final_year[result["split"]["test"]].tolist()))
    summary = {
        "dataset_version": dataset_version,
        "source_csv_sha256": raw_sha,
        "years": list(args.years),
        "selected_raw_rows": len(raw),
        "clean_rows": len(cleaned),
        "storms": int(cleaned["storm_id"].nunique()),
        "cleaning": quality.as_dict(),
        "split_storms": {k: len(result["split"][k]) for k in ("train", "val", "test")},
        "test_years": test_years,
        "elapsed_seconds": time.perf_counter() - started,
        "history": result["history"],
        "evaluation": result["evaluation"],
        "manifest": str(result["manifest"]),
    }
    policy = PromotionPolicy(
        max_mean_error_km=args.max_error_km,
        min_calibration_coverage=args.min_coverage,
        max_persistence_error_ratio=args.max_persistence_ratio,
    )
    metrics = promotion_metrics(result["evaluation"], horizon_h=args.gate_horizon)
    summary["promotion_gate"] = {
        "horizon_h": args.gate_horizon,
        "policy": vars(policy),
        "metrics": {k: round(v, 3) for k, v in metrics.items()},
        "failures": policy.failures(metrics),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "benchmark.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    report = _markdown(summary)
    (args.output_dir / "benchmark.md").write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
