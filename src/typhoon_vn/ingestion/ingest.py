"""Convert verified raw objects into partitioned canonical records."""

from __future__ import annotations

import hashlib
from pathlib import Path

from typhoon_vn.ingestion.errors import IngestionError, ProviderSchemaError
from typhoon_vn.ingestion.providers.strategies import (
    DEFAULT_PROVIDER_FACTORY,
    ProviderFactory,
)
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
    factory: ProviderFactory = DEFAULT_PROVIDER_FACTORY,
) -> list[Path]:
    """Parse one raw object through an isolated strategy and persist it."""
    checksum = sha256_file(input_path)
    strategy = factory.create(source)
    try:
        payload = strategy.parse(input_path, source_url=source_url, checksum=checksum)
    except IngestionError:
        raise
    except (KeyError, TypeError, ValueError, UnicodeError) as exc:
        raise ProviderSchemaError(
            f"{strategy.source} payload does not match its parser contract: {exc}"
        ) from exc
    if payload.kind == "impact_labels":
        label_path = write_impact_labels(payload.records, data_root=data_root)
        return [label_path] if label_path else []
    if payload.kind != "observations":
        raise ProviderSchemaError(
            f"{strategy.source} returned unsupported payload kind {payload.kind!r}"
        )
    return write_observations(payload.records, data_root=data_root)
