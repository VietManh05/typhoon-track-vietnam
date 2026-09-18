"""Explicit, conservative reconciliation of observations from multiple sources."""

from __future__ import annotations

import math
from dataclasses import replace
from datetime import timedelta
from typing import Iterable

from typhoon_vn.ingestion.identifiers import is_resolved_storm_id
from typhoon_vn.ingestion.models import Observation

SOURCE_PRIORITY = ("ibtracs", "jtwc", "jma", "cma", "nchmf")


def haversine_km(
    latitude_a: float,
    longitude_a: float,
    latitude_b: float,
    longitude_b: float,
) -> float:
    """Return the great-circle distance in kilometres between WGS84 points."""

    radius_km = 6371.0088
    latitude_delta = math.radians(latitude_b - latitude_a)
    longitude_delta = math.radians(longitude_b - longitude_a)
    a = (
        math.sin(latitude_delta / 2) ** 2
        + math.cos(math.radians(latitude_a))
        * math.cos(math.radians(latitude_b))
        * math.sin(longitude_delta / 2) ** 2
    )
    return 2 * radius_km * math.asin(math.sqrt(a))


def observations_match(
    left: Observation,
    right: Observation,
    *,
    time_tolerance: timedelta = timedelta(hours=3),
    distance_tolerance_km: float = 75.0,
) -> bool:
    """Match only evidence-backed identities that are close in time and space."""

    same_identity = (
        is_resolved_storm_id(left.storm_id) and left.storm_id == right.storm_id
    )
    if not same_identity or abs(left.timestamp - right.timestamp) > time_tolerance:
        return False
    distance = haversine_km(
        left.latitude,
        left.longitude,
        right.latitude,
        right.longitude,
    )
    return distance <= distance_tolerance_km


def merge_observations(observations: Iterable[Observation]) -> list[Observation]:
    """Merge duplicates while retaining every contributing source in metadata.

    Conflicting values are not averaged. The priority source is selected for the
    row and every alternative remains in ``metadata['source_conflicts']`` for
    later quality review.
    """

    ordered = sorted(
        observations,
        key=lambda item: (item.storm_id, item.timestamp, _priority(item.source)),
    )
    groups: list[list[Observation]] = []
    for observation in ordered:
        for group in groups:
            if observations_match(group[0], observation):
                group.append(observation)
                break
        else:
            groups.append([observation])

    merged: list[Observation] = []
    for group in groups:
        selected = min(group, key=lambda item: _priority(item.source))
        conflicts = [
            {
                "source": item.source,
                "latitude": item.latitude,
                "longitude": item.longitude,
                "wind": item.wind,
                "pressure_hpa": item.pressure_hpa,
            }
            for item in group
            if item != selected
        ]
        metadata = {**selected.metadata, "source_conflicts": conflicts}
        merged.append(
            replace(
                selected,
                contributing_sources=tuple(sorted({item.source for item in group})),
                metadata=metadata,
            )
        )
    return merged


def _priority(source: str) -> int:
    try:
        return SOURCE_PRIORITY.index(source.lower())
    except ValueError:
        return len(SOURCE_PRIORITY)
