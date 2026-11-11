"""Canonical storm-track contract shared across architectural layers."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field


@dataclass(frozen=True)
class TrackSchema:
    """Column names and required fields for canonical cleaned track frames."""

    storm_id: str = "storm_id"
    timestamp: str = "timestamp"
    lat: str = "lat"
    lon: str = "lon"
    wind_ms: str = "wind_ms"
    pressure_hpa: str = "pressure_hpa"
    intensity: str = "intensity"
    end_flag: str = "end_flag"
    source: str = "source"
    source_url: str = "source_url"
    source_file_checksum: str = "source_file_checksum"
    dataset_version: str = "dataset_version"
    downloaded_at: str = "downloaded_at"
    interpolated: str = "interpolated"
    suspicious: str = "suspicious"

    @property
    def required(self) -> tuple[str, ...]:
        return (self.storm_id, self.timestamp, self.lat, self.lon)

    @property
    def numeric(self) -> tuple[str, ...]:
        return (self.lat, self.lon, self.wind_ms, self.pressure_hpa)

    def validate_columns(self, columns: Iterable[str]) -> None:
        names = list(columns)
        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            raise ValueError(
                f"canonical track schema contains duplicate columns: {duplicates}"
            )
        available = set(names)
        missing = [name for name in self.required if name not in available]
        if missing:
            raise ValueError(
                f"canonical track schema missing required columns: {missing}"
            )

    def columns(self) -> list[str]:
        return [
            self.storm_id,
            self.timestamp,
            self.lat,
            self.lon,
            self.wind_ms,
            self.pressure_hpa,
            self.intensity,
            self.end_flag,
            self.source,
            self.source_url,
            self.source_file_checksum,
            self.dataset_version,
            self.downloaded_at,
            self.interpolated,
            self.suspicious,
        ]


DEFAULT_SCHEMA = TrackSchema()


@dataclass
class CleaningReport:
    """Per-run quality summary emitted by the cleaning pipeline."""

    n_input: int = 0
    n_output: int = 0
    n_dropped_invalid_coords: int = 0
    n_dropped_outside_domain: int = 0
    n_dropped_invalid_physics: int = 0
    n_duplicates_removed: int = 0
    n_interpolated: int = 0
    n_suspicious_flagged: int = 0
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, object]:
        return {
            "n_input": self.n_input,
            "n_output": self.n_output,
            "n_dropped_invalid_coords": self.n_dropped_invalid_coords,
            "n_dropped_outside_domain": self.n_dropped_outside_domain,
            "n_dropped_invalid_physics": self.n_dropped_invalid_physics,
            "n_duplicates_removed": self.n_duplicates_removed,
            "n_interpolated": self.n_interpolated,
            "n_suspicious_flagged": self.n_suspicious_flagged,
            "notes": list(self.notes),
        }
