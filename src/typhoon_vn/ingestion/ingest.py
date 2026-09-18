"""Convert a verified raw object into partitioned canonical raw observations."""

from __future__ import annotations

import hashlib
from pathlib import Path

from typhoon_vn.ingestion.errors import IngestionError
from typhoon_vn.ingestion.providers.cma import parse_cma_text
from typhoon_vn.ingestion.providers.ibtracs import parse_ibtracs_csv
from typhoon_vn.ingestion.providers.jma import parse_jma_archive
from typhoon_vn.ingestion.providers.jtwc import parse_jtwc_atcf
from typhoon_vn.ingestion.providers.vietnam import parse_impact_csv, parse_nchmf_csv
from typhoon_vn.ingestion.storage import write_impact_labels, write_observations


def sha256_file(path: Path) -> str:
    """Calculate the digest of the exact object given to a parser."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def parse_and_store(
    source: str,
    *,
    input_path: Path,
    source_url: str,
    data_root: Path,
) -> list[Path]:
    """Parse one raw object and append it to source/year raw Parquet parts."""

    checksum = sha256_file(input_path)
    source = source.lower()
    if source == "cma":
        observations = parse_cma_text(
            input_path.read_text(encoding="utf-8", errors="replace"),
            source_url=source_url,
            checksum=checksum,
        )
    elif source == "ibtracs":
        observations = parse_ibtracs_csv(
            input_path.read_text(encoding="utf-8-sig", errors="replace"),
            source_url=source_url,
            checksum=checksum,
        )
    elif source == "jma":
        observations = parse_jma_archive(
            input_path,
            source_url=source_url,
            checksum=checksum,
        )
    elif source == "jtwc":
        observations = parse_jtwc_atcf(
            input_path.read_text(encoding="utf-8", errors="replace"),
            source_url=source_url,
            checksum=checksum,
        )
    elif source == "nchmf":
        observations = parse_nchmf_csv(
            input_path,
            source_url=source_url,
            checksum=checksum,
        )
    elif source == "pctt":
        labels = parse_impact_csv(input_path, source_url=source_url, checksum=checksum)
        label_path = write_impact_labels(labels, data_root=data_root)
        return [label_path] if label_path else []
    else:
        raise IngestionError(f"unsupported parser source: {source}")
    return write_observations(observations, data_root=data_root)
