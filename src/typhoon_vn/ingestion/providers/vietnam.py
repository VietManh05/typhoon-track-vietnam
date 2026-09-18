"""Manifest-driven ingestion for NCHMF bulletins and PCTT impact labels."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

from typhoon_vn.ingestion.identifiers import canonical_storm_id
from typhoon_vn.ingestion.models import ImpactLabel, Observation


def parse_nchmf_csv(
    path: Path,
    *,
    source_url: str,
    checksum: str,
) -> list[Observation]:
    """Parse an approved NCHMF export in the documented interchange layout.

    Historical NCHMF bulletins are not treated as a scrape target. An authorised
    export is mapped to timestamp, storm_id, latitude, longitude, wind_kt,
    pressure_hpa, and name. The source URL remains required provenance.
    """

    observations: list[Observation] = []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            timestamp = _parse_utc(row.get("timestamp", ""))
            latitude = _as_float(row.get("latitude"))
            longitude = _as_float(row.get("longitude"))
            if timestamp is None or latitude is None or longitude is None:
                continue
            source_id = (row.get("storm_id") or "UNKNOWN").strip()
            observations.append(
                Observation(
                    source="nchmf",
                    source_storm_id=source_id,
                    storm_id=canonical_storm_id(source_id, season=timestamp.year),
                    timestamp=timestamp,
                    latitude=latitude,
                    longitude=longitude,
                    wind=_as_float(row.get("wind_kt")),
                    wind_unit="kt",
                    pressure_hpa=_as_float(row.get("pressure_hpa")),
                    storm_name=(row.get("name") or "").strip() or None,
                    source_url=source_url,
                    source_file_checksum=checksum,
                    dataset_version="NCHMF authorised bulletin export",
                    metadata={"original_time_zone": "Asia/Ho_Chi_Minh"},
                )
            )
    return observations


def parse_impact_csv(
    path: Path,
    *,
    source_url: str,
    checksum: str,
) -> list[ImpactLabel]:
    """Parse approved provincial impact labels without mixing them into tracks."""

    labels: list[ImpactLabel] = []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            source_id = (row.get("storm_id") or "UNKNOWN").strip()
            event_time = _parse_utc(row.get("event_time", ""))
            labels.append(
                ImpactLabel(
                    storm_id=canonical_storm_id(
                        source_id,
                        season=event_time.year if event_time else None,
                    ),
                    province=(row.get("province") or "").strip(),
                    impact_type=(row.get("impact_type") or "unspecified").strip(),
                    severity=(row.get("severity") or "").strip() or None,
                    event_time=event_time,
                    source_url=source_url,
                    source_file_checksum=checksum,
                    metadata={
                        "reference": (row.get("reference") or "").strip() or None
                    },
                )
            )
    return labels


def _parse_utc(value: str) -> datetime | None:
    cleaned = value.strip()
    for format_string in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S"):
        try:
            parsed = datetime.strptime(cleaned, format_string)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc)
        except ValueError:
            continue
    return None


def _as_float(value: str | None) -> float | None:
    try:
        return float(value) if value not in (None, "") else None
    except ValueError:
        return None
