"""Raw Parquet storage with source/year partitioning and no implicit cleanup."""

from __future__ import annotations

import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from typhoon_vn.ingestion.errors import OptionalDependencyError
from typhoon_vn.ingestion.models import ImpactLabel, Observation

OBSERVATION_SCHEMA_VERSION = "1.0.0"


def _pandas():
    try:
        import pandas as pd
    except ImportError as error:
        raise OptionalDependencyError(
            'Parquet storage requires: python -m pip install -e ".[ingestion]"'
        ) from error
    return pd


def _write_parquet_atomic(frame, path: Path) -> None:
    """Write ``frame`` to ``path`` atomically (stage to ``.tmp``, then rename).

    Parquet is first written to a sibling ``.<name>.tmp`` file and moved into
    place with :func:`os.replace`, which is atomic within one filesystem. A
    crash or kill mid-write therefore leaves only the temporary file, never a
    truncated ``part-*.parquet`` that downstream readers would accept as valid.
    """

    tmp_path = path.with_name(f".{path.name}.tmp")
    try:
        frame.to_parquet(tmp_path, index=False, engine="pyarrow")
        os.replace(tmp_path, path)
    finally:
        tmp_path.unlink(missing_ok=True)


def write_observations(
    observations: Iterable[Observation], *, data_root: Path
) -> list[Path]:
    """Append a unique Parquet part for each source/year partition.

    Existing parts are never overwritten. This lets DVC version completed raw
    snapshots and preserves source changes for investigation.
    """

    partitions: dict[tuple[str, int], list[dict[str, object]]] = defaultdict(list)
    for observation in observations:
        row = observation.to_row()
        row["metadata"] = json.dumps(
            row["metadata"], ensure_ascii=False, sort_keys=True
        )
        row["schema_version"] = OBSERVATION_SCHEMA_VERSION
        partitions[(observation.source, observation.year)].append(row)
    pd = _pandas()
    paths: list[Path] = []
    for (source, year), rows in partitions.items():
        partition = data_root / "raw" / "observations" / f"source={source}"
        partition = partition / f"year={year}"
        partition.mkdir(parents=True, exist_ok=True)
        index = len(list(partition.glob("part-*.parquet")))
        path = partition / f"part-{index:05d}.parquet"
        _write_parquet_atomic(pd.DataFrame(rows), path)
        paths.append(path)
    return paths


def write_impact_labels(
    labels: Iterable[ImpactLabel], *, data_root: Path
) -> Path | None:
    """Store raw impact labels separately from track observations."""

    rows = []
    for label in labels:
        rows.append(
            {
                "storm_id": label.storm_id,
                "province": label.province,
                "impact_type": label.impact_type,
                "source_url": label.source_url,
                "source_file_checksum": label.source_file_checksum,
                "event_time": (
                    label.event_time.isoformat() if label.event_time else None
                ),
                "severity": label.severity,
                "metadata": json.dumps(
                    label.metadata, ensure_ascii=False, sort_keys=True
                ),
            }
        )
    if not rows:
        return None
    pd = _pandas()
    directory = data_root / "raw" / "impact_labels"
    directory.mkdir(parents=True, exist_ok=True)
    index = len(list(directory.glob("part-*.parquet")))
    path = directory / f"part-{index:05d}.parquet"
    _write_parquet_atomic(pd.DataFrame(rows), path)
    return path
