"""Canonical records exchanged by all Phase 1 source adapters."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

SUPPORTED_WIND_UNITS = frozenset({"kt", "knot", "knots", "m/s", "ms"})


def _utc_datetime(value: datetime, field_name: str) -> datetime:
    """Require an aware datetime and return its UTC representation."""

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return value.astimezone(timezone.utc)


@dataclass(frozen=True, slots=True)
class Observation:
    """One source observation with immutable source-level provenance.

    Wind values retain the source unit in ``wind_unit``. No conversion is done
    here, because later cleaning must make that decision visible and testable.
    """

    source: str
    source_storm_id: str
    storm_id: str
    timestamp: datetime
    latitude: float
    longitude: float
    source_url: str
    source_file_checksum: str
    wind: float | None = None
    wind_unit: str | None = None
    pressure_hpa: float | None = None
    storm_name: str | None = None
    intensity_code: str | None = None
    dataset_version: str | None = None
    contributing_sources: tuple[str, ...] = field(default_factory=tuple)
    downloaded_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not math.isfinite(self.latitude) or not -90 <= self.latitude <= 90:
            raise ValueError(f"latitude outside WGS84 bounds: {self.latitude}")
        if not math.isfinite(self.longitude) or not -180 <= self.longitude <= 360:
            raise ValueError(f"longitude outside supported bounds: {self.longitude}")
        object.__setattr__(
            self, "timestamp", _utc_datetime(self.timestamp, "timestamp")
        )
        if self.downloaded_at is not None:
            object.__setattr__(
                self,
                "downloaded_at",
                _utc_datetime(self.downloaded_at, "downloaded_at"),
            )
        source = self.source.strip().lower()
        if (
            not source
            or not self.source_url.strip()
            or not self.source_file_checksum.strip()
        ):
            raise ValueError("source, source_url and source_file_checksum are required")
        object.__setattr__(self, "source", source)
        if self.wind_unit is not None:
            unit = self.wind_unit.strip().lower()
            if unit not in SUPPORTED_WIND_UNITS:
                raise ValueError(f"unsupported wind unit: {self.wind_unit}")
            object.__setattr__(self, "wind_unit", unit)
        for field_name in ("wind", "pressure_hpa"):
            value = getattr(self, field_name)
            if value is not None and not math.isfinite(value):
                raise ValueError(f"{field_name} must be finite")
        if not self.contributing_sources:
            object.__setattr__(self, "contributing_sources", (self.source,))

    @property
    def year(self) -> int:
        """UTC year used for reproducible partition paths."""

        return self.timestamp.year

    def to_row(self) -> dict[str, Any]:
        """Return a dataframe-friendly, JSON-serialisable representation."""

        row = asdict(self)
        row["timestamp"] = self.timestamp.isoformat()
        row["contributing_sources"] = list(self.contributing_sources)
        return row


@dataclass(frozen=True, slots=True)
class DownloadResult:
    """A verified raw download and the metadata needed to reproduce it."""

    source: str
    url: str
    local_path: str
    sha256: str
    downloaded_at: datetime
    bytes_written: int
    etag: str | None = None
    last_modified: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "downloaded_at", _utc_datetime(self.downloaded_at, "downloaded_at")
        )

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["downloaded_at"] = self.downloaded_at.isoformat()
        return result


@dataclass(frozen=True, slots=True)
class SourceFile:
    """A local source file paired with its download lineage."""

    path: str
    source: str
    source_url: str
    checksum: str
    dataset_version: str | None = None


@dataclass(frozen=True, slots=True)
class ImpactLabel:
    """A raw impact record retained separately from track observations."""

    storm_id: str
    province: str
    impact_type: str
    source_url: str
    source_file_checksum: str
    event_time: datetime | None = None
    severity: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
