"""Fetch free IBTrACS tracks and train an isolated, unpromoted candidate.

Run from the repository root with Python 3.11 and the train/ingestion extras.
The same source/config/year selection is trained only once. No bundle is
published or promoted by this script.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from evaluate_ibtracs_candidate import evaluate_candidate
from run_ibtracs_training import train_from_ibtracs

from typhoon_vn.ingestion.ingest import parse_and_store
from typhoon_vn.ingestion.providers.ibtracs import IBTrACSProvider


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _training_code_sha256() -> str:
    digest = hashlib.sha256()
    paths = sorted(Path("src/typhoon_vn").rglob("*.py")) + [
        Path("scripts/run_ibtracs_training.py"),
        Path("scripts/evaluate_ibtracs_candidate.py"),
    ]
    for path in paths:
        digest.update(path.as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", type=Path, default=Path("configs/ibtracs_candidate.yaml")
    )
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument(
        "--output-root", type=Path, default=Path("data/processed/retraining")
    )
    parser.add_argument("--start-year", type=int, default=2015)
    parser.add_argument("--end-year", type=int)
    parser.add_argument("--use-local-source", action="store_true")
    args = parser.parse_args()
    end_year = args.end_year or datetime.now(timezone.utc).year - 1
    if args.start_year > end_year:
        parser.error("--start-year must not exceed --end-year")
    if not args.config.is_file():
        parser.error(f"training config is missing: {args.config}")

    args.output_root.mkdir(parents=True, exist_ok=True)
    lock_path = args.output_root / ".retrain.lock"
    try:
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as error:
        raise SystemExit(
            f"another retraining run may be active: {lock_path}"
        ) from error
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as lock:
            lock.write(
                f"pid={os.getpid()} utc={datetime.now(timezone.utc).isoformat()}\n"
            )
        provider = IBTrACSProvider()
        source = args.data_root / "raw/downloads/ibtracs/ibtracs-wp.csv"
        if not args.use_local_source:
            source = Path(provider.download(data_root=args.data_root).local_path)
        if not source.is_file():
            raise SystemExit(f"IBTrACS source is missing: {source}")
        source_sha = _sha256(source)
        identity_data = {
            "source_sha256": source_sha,
            "config_sha256": _sha256(args.config),
            "code_sha256": _training_code_sha256(),
            "start_year": args.start_year,
            "end_year": end_year,
        }
        identity = hashlib.sha256(
            json.dumps(identity_data, sort_keys=True).encode("utf-8")
        ).hexdigest()[:20]
        output_dir = args.output_root / identity
        summary_path = output_dir / "training-summary.json"
        if summary_path.is_file():
            evaluation_path = output_dir / "heldout-evaluation.json"
            if not evaluation_path.is_file():
                evaluation = evaluate_candidate(
                    candidate=output_dir,
                    data_root=args.data_root,
                    start_year=args.start_year,
                    end_year=end_year,
                )
            else:
                evaluation = json.loads(evaluation_path.read_text(encoding="utf-8"))
            print(
                json.dumps(
                    {
                        "status": "unchanged",
                        "candidate": str(output_dir),
                        "evaluation_status": evaluation["status"],
                    }
                )
            )
            return 0 if evaluation["beats_persistence_all_horizons"] else 2
        if output_dir.exists():
            raise SystemExit(
                f"incomplete candidate needs operator review: {output_dir}"
            )

        parsed_marker = source.parent / f"parsed-{source_sha}.json"
        if not parsed_marker.is_file():
            parts = parse_and_store(
                "ibtracs",
                input_path=source,
                source_url=provider.url,
                data_root=args.data_root,
            )
            parsed_marker.write_text(
                json.dumps(
                    {
                        "source_sha256": source_sha,
                        "source_url": provider.url,
                        "partition_count": len(parts),
                        "parsed_at": datetime.now(timezone.utc).isoformat(),
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
        summary = train_from_ibtracs(
            config=args.config,
            data_root=args.data_root,
            output_dir=output_dir,
            start_year=args.start_year,
            end_year=end_year,
        )
        (output_dir / "run-identity.json").write_text(
            json.dumps(identity_data, indent=2, sort_keys=True), encoding="utf-8"
        )
        evaluation = evaluate_candidate(
            candidate=output_dir,
            data_root=args.data_root,
            start_year=args.start_year,
            end_year=end_year,
        )
        print(
            json.dumps(
                {
                    "status": evaluation["status"],
                    "candidate": str(output_dir),
                    "source_sha256": source_sha,
                    "storms": summary["storms"],
                    "beats_persistence_all_horizons": evaluation[
                        "beats_persistence_all_horizons"
                    ],
                    "promoted": False,
                }
            )
        )
        return 0 if evaluation["beats_persistence_all_horizons"] else 2
    finally:
        lock_path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
