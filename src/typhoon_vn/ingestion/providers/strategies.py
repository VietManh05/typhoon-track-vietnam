"""Provider parsing strategies and their explicit registry.

External formats are isolated behind ProviderStrategy. Adding or replacing a
source does not require editing the ingestion orchestration flow.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, TypeVar

from typhoon_vn.ingestion.errors import ProviderSchemaError, UnsupportedProviderError
from typhoon_vn.ingestion.models import ImpactLabel, Observation
from typhoon_vn.ingestion.providers.cma import parse_cma_text
from typhoon_vn.ingestion.providers.ibtracs import parse_ibtracs_csv
from typhoon_vn.ingestion.providers.jma import parse_jma_archive
from typhoon_vn.ingestion.providers.jtwc import parse_jtwc_atcf
from typhoon_vn.ingestion.providers.vietnam import parse_impact_csv, parse_nchmf_csv

Record = TypeVar("Record", Observation, ImpactLabel)


@dataclass(frozen=True, slots=True)
class ParsedPayload(Generic[Record]):
    kind: str
    records: list[Record]


class ProviderStrategy(ABC):
    """Parse one verified source object into domain records."""

    source: str
    kind = "observations"

    @abstractmethod
    def parse(
        self, input_path: Path, *, source_url: str, checksum: str
    ) -> ParsedPayload:
        """Parse one source object or raise a typed provider failure."""

    def _checked(
        self, records: list[Record], input_path: Path
    ) -> ParsedPayload[Record]:
        if not records:
            raise ProviderSchemaError(
                f"{self.source} produced no valid {self.kind} from {input_path}; "
                "the upstream schema may have changed"
            )
        return ParsedPayload(self.kind, records)


class CMAParser(ProviderStrategy):
    source = "cma"

    def parse(
        self, input_path: Path, *, source_url: str, checksum: str
    ) -> ParsedPayload:
        records = parse_cma_text(
            input_path.read_text(encoding="utf-8", errors="replace"),
            source_url=source_url,
            checksum=checksum,
        )
        return self._checked(records, input_path)


class IBTrACSParser(ProviderStrategy):
    source = "ibtracs"

    def parse(
        self, input_path: Path, *, source_url: str, checksum: str
    ) -> ParsedPayload:
        records = parse_ibtracs_csv(
            input_path.read_text(encoding="utf-8-sig", errors="replace"),
            source_url=source_url,
            checksum=checksum,
        )
        return self._checked(records, input_path)


class JMAParser(ProviderStrategy):
    source = "jma"

    def parse(
        self, input_path: Path, *, source_url: str, checksum: str
    ) -> ParsedPayload:
        records = parse_jma_archive(
            input_path, source_url=source_url, checksum=checksum
        )
        return self._checked(records, input_path)


class JTWCParser(ProviderStrategy):
    source = "jtwc"

    def parse(
        self, input_path: Path, *, source_url: str, checksum: str
    ) -> ParsedPayload:
        records = parse_jtwc_atcf(
            input_path.read_text(encoding="utf-8", errors="replace"),
            source_url=source_url,
            checksum=checksum,
        )
        return self._checked(records, input_path)


class NCHMFParser(ProviderStrategy):
    source = "nchmf"

    def parse(
        self, input_path: Path, *, source_url: str, checksum: str
    ) -> ParsedPayload:
        records = parse_nchmf_csv(input_path, source_url=source_url, checksum=checksum)
        return self._checked(records, input_path)


class PCTTParser(ProviderStrategy):
    source = "pctt"
    kind = "impact_labels"

    def parse(
        self, input_path: Path, *, source_url: str, checksum: str
    ) -> ParsedPayload:
        records = parse_impact_csv(input_path, source_url=source_url, checksum=checksum)
        return self._checked(records, input_path)


class ProviderFactory:
    """Resolve immutable parser strategies by normalized source name."""

    def __init__(self, strategies: tuple[ProviderStrategy, ...] | None = None) -> None:
        configured = strategies or (
            CMAParser(),
            IBTrACSParser(),
            JMAParser(),
            JTWCParser(),
            NCHMFParser(),
            PCTTParser(),
        )
        self._strategies = {item.source: item for item in configured}
        if len(self._strategies) != len(configured):
            raise ValueError("provider strategy names must be unique")

    @property
    def sources(self) -> tuple[str, ...]:
        return tuple(sorted(self._strategies))

    def create(self, source: str) -> ProviderStrategy:
        normalized = source.strip().lower()
        try:
            return self._strategies[normalized]
        except KeyError as exc:
            raise UnsupportedProviderError(
                f"unsupported parser source: {source}; supported: {', '.join(self.sources)}"
            ) from exc


DEFAULT_PROVIDER_FACTORY = ProviderFactory()

__all__ = [
    "DEFAULT_PROVIDER_FACTORY",
    "ParsedPayload",
    "ProviderFactory",
    "ProviderStrategy",
]
