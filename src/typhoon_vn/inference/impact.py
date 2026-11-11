"""Geometry-only cone impact assessment with explicit semantic limits."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from typhoon_vn.features.geo import haversine_km
from typhoon_vn.features.geospatial import Point, point_in_polygon


@dataclass(frozen=True, slots=True)
class ImpactAssessment:
    intersects_province: bool
    intersects_coastline: bool
    first_intersection_hours: int | None
    minimum_center_distance_km: float
    hazard_probability: float | None = None
    limitation: str = (
        "Cone intersection describes possible track-center geometry only; "
        "it is not wind, flood, damage, or landfall probability."
    )


def _orientation(a: Point, b: Point, c: Point) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _on_segment(a: Point, b: Point, p: Point, *, epsilon: float = 1e-10) -> bool:
    return (
        min(a[1], b[1]) - epsilon <= p[1] <= max(a[1], b[1]) + epsilon
        and min(a[0], b[0]) - epsilon <= p[0] <= max(a[0], b[0]) + epsilon
        and abs(_orientation(a, b, p)) <= epsilon
    )


def _segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    o1, o2 = _orientation(a, b, c), _orientation(a, b, d)
    o3, o4 = _orientation(c, d, a), _orientation(c, d, b)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    return any(
        (abs(value) <= 1e-10 and _on_segment(start, end, candidate))
        for value, start, end, candidate in (
            (o1, a, b, c),
            (o2, a, b, d),
            (o3, c, d, a),
            (o4, c, d, b),
        )
    )


def _edges(points: Sequence[Point], *, close: bool) -> Iterable[tuple[Point, Point]]:
    for index in range(len(points) - 1):
        yield points[index], points[index + 1]
    if close and len(points) > 2 and points[0] != points[-1]:
        yield points[-1], points[0]


def polygons_intersect(left: Sequence[Point], right: Sequence[Point]) -> bool:
    """Return true for overlap, containment, or a boundary touch."""
    if len(left) < 3 or len(right) < 3:
        raise ValueError("polygons require at least three points")
    if point_in_polygon(left[0], right) or point_in_polygon(right[0], left):
        return True
    return any(
        _segments_intersect(a, b, c, d)
        for a, b in _edges(left, close=True)
        for c, d in _edges(right, close=True)
    )


def polygon_intersects_line(polygon: Sequence[Point], line: Sequence[Point]) -> bool:
    if len(polygon) < 3 or len(line) < 2:
        raise ValueError("polygon/line geometry is incomplete")
    if any(point_in_polygon(point, polygon) for point in line):
        return True
    return any(
        _segments_intersect(a, b, c, d)
        for a, b in _edges(polygon, close=True)
        for c, d in _edges(line, close=False)
    )


def assess_cone_impact(
    forecast_points: Sequence[object],
    *,
    province: Sequence[Point],
    coastline: Sequence[Point],
) -> ImpactAssessment:
    """Assess forecast cone geometry against versioned province/coast shapes."""
    if not forecast_points:
        raise ValueError("at least one forecast point is required")
    province_hits: list[int] = []
    coast_hit = False
    distances: list[float] = []
    for point in forecast_points:
        coordinates = point.cone["coordinates"][0]
        cone = [(float(lon), float(lat)) for lon, lat in coordinates]
        if polygons_intersect(cone, province):
            province_hits.append(int(point.horizon_hours))
        coast_hit = coast_hit or polygon_intersects_line(cone, coastline)
        distances.extend(
            haversine_km(point.lat, point.lon, vertex[1], vertex[0])
            for vertex in province
        )
    return ImpactAssessment(
        intersects_province=bool(province_hits),
        intersects_coastline=coast_hit,
        first_intersection_hours=min(province_hits) if province_hits else None,
        minimum_center_distance_km=min(distances),
    )


__all__ = [
    "ImpactAssessment",
    "assess_cone_impact",
    "polygon_intersects_line",
    "polygons_intersect",
]
