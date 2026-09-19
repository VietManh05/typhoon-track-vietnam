"""Small, dependency-free geospatial contracts for Phase 2.

The production boundary archives remain versioned raw inputs.  These helpers
operate on WGS84 GeoJSON fixtures and keep the geometry assumptions explicit,
which makes CRS, point-in-polygon, nearest-province and coastline behaviour
testable without silently downloading or redistributing third-party data.
"""

from __future__ import annotations

import math
import re
import unicodedata
from dataclasses import dataclass
from typing import Iterable, Sequence

from typhoon_vn.features.geo import haversine_km

Point = tuple[float, float]  # longitude, latitude


def require_wgs84(crs: str | None) -> str:
    """Accept explicit EPSG:4326/CRS84 identifiers and reject ambiguity."""

    normalised = (crs or "").strip().upper().replace(" ", "")
    accepted = {"EPSG:4326", "URN:OGC:DEF:CRS:OGC:1.3:CRS84", "CRS84"}
    if normalised not in accepted:
        raise ValueError(f"expected WGS84/EPSG:4326, received {crs!r}")
    return "EPSG:4326"


def normalise_province_name(value: str) -> str:
    """Return a stable ASCII key while retaining display names separately."""

    translated = value.strip().lower().replace("đ", "d")
    decomposed = unicodedata.normalize("NFKD", translated)
    ascii_name = "".join(char for char in decomposed if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "-", ascii_name).strip("-")


def _point_segment_distance_km(point: Point, start: Point, end: Point) -> float:
    """Approximate local projection distance from a point to a line segment."""

    lon, lat = point
    lon0, lat0 = start
    lon1, lat1 = end
    scale = max(math.cos(math.radians(lat)), 1e-6)
    px, py = (lon - lon0) * scale, lat - lat0
    vx, vy = (lon1 - lon0) * scale, lat1 - lat0
    denominator = vx * vx + vy * vy
    factor = (
        0.0
        if denominator == 0
        else max(0.0, min(1.0, (px * vx + py * vy) / denominator))
    )
    nearest = (lon0 + factor * (lon1 - lon0), lat0 + factor * (lat1 - lat0))
    return haversine_km(lat, lon, nearest[1], nearest[0])


def distance_to_coast_km(point: Point, coastline: Sequence[Point]) -> float:
    """Return minimum geodesic distance to a coastline polyline."""

    if len(coastline) < 2:
        raise ValueError("coastline requires at least two points")
    return min(
        _point_segment_distance_km(point, left, right)
        for left, right in zip(coastline, coastline[1:])
    )


def point_in_polygon(point: Point, polygon: Sequence[Point]) -> bool:
    """Ray-casting containment; points on the boundary count as contained."""

    if len(polygon) < 3:
        raise ValueError("polygon requires at least three points")
    x, y = point
    inside = False
    ring = list(polygon)
    if ring[0] != ring[-1]:
        ring.append(ring[0])
    for left, right in zip(ring, ring[1:]):
        if _point_segment_distance_km(point, left, right) <= 1e-8:
            return True
        x0, y0 = left
        x1, y1 = right
        if (y0 > y) != (y1 > y):
            crossing = (x1 - x0) * (y - y0) / (y1 - y0) + x0
            if x <= crossing:
                inside = not inside
    return inside


def simplify_polyline(points: Sequence[Point], tolerance_degrees: float) -> list[Point]:
    """Simplify a line with Ramer-Douglas-Peucker while retaining endpoints."""

    if tolerance_degrees < 0:
        raise ValueError("tolerance_degrees must be non-negative")
    if len(points) <= 2:
        return list(points)
    start, end = points[0], points[-1]
    ex, ey = end[0] - start[0], end[1] - start[1]
    denominator = math.hypot(ex, ey)
    distances = []
    for point in points[1:-1]:
        if denominator == 0:
            distance = math.hypot(point[0] - start[0], point[1] - start[1])
        else:
            distance = (
                abs(ex * (start[1] - point[1]) - (start[0] - point[0]) * ey)
                / denominator
            )
        distances.append(distance)
    maximum = max(distances, default=0.0)
    if maximum <= tolerance_degrees:
        return [start, end]
    pivot = distances.index(maximum) + 1
    return simplify_polyline(points[: pivot + 1], tolerance_degrees)[
        :-1
    ] + simplify_polyline(points[pivot:], tolerance_degrees)


@dataclass(frozen=True, slots=True)
class ProvinceBoundary:
    province_id: str
    name: str
    polygon: tuple[Point, ...]

    @property
    def bbox(self) -> tuple[float, float, float, float]:
        xs, ys = zip(*self.polygon)
        return min(xs), min(ys), max(xs), max(ys)


class ProvinceIndex:
    """Bounding-box index with exact polygon filtering for small VN fixtures."""

    def __init__(self, boundaries: Iterable[ProvinceBoundary]) -> None:
        self.boundaries = tuple(boundaries)
        if len({item.province_id for item in self.boundaries}) != len(self.boundaries):
            raise ValueError("province IDs must be unique")

    def containing(self, point: Point) -> ProvinceBoundary | None:
        x, y = point
        for boundary in self.boundaries:
            xmin, ymin, xmax, ymax = boundary.bbox
            if (
                xmin <= x <= xmax
                and ymin <= y <= ymax
                and point_in_polygon(point, boundary.polygon)
            ):
                return boundary
        return None

    def nearest(self, point: Point) -> tuple[ProvinceBoundary, float]:
        if not self.boundaries:
            raise ValueError("province index is empty")
        containing = self.containing(point)
        if containing is not None:
            return containing, 0.0
        ranked = []
        for boundary in self.boundaries:
            ring = list(boundary.polygon)
            if ring[0] != ring[-1]:
                ring.append(ring[0])
            distance = min(
                _point_segment_distance_km(point, left, right)
                for left, right in zip(ring, ring[1:])
            )
            ranked.append((distance, boundary.province_id, boundary))
        distance, _, boundary = min(ranked)
        return boundary, distance


@dataclass(frozen=True, slots=True)
class SpecialLocation:
    location_id: str
    name: str
    latitude: float
    longitude: float

    def distance_km(self, latitude: float, longitude: float) -> float:
        return haversine_km(latitude, longitude, self.latitude, self.longitude)


SPECIAL_LOCATIONS: tuple[SpecialLocation, ...] = (
    SpecialLocation("island-hoang-sa", "Hoàng Sa", 16.55, 112.30),
    SpecialLocation("island-truong-sa", "Trường Sa", 8.64, 111.92),
    SpecialLocation("port-hai-phong", "Cảng Hải Phòng", 20.86, 106.68),
    SpecialLocation("port-da-nang", "Cảng Đà Nẵng", 16.07, 108.22),
    SpecialLocation("port-vung-tau", "Cảng Vũng Tàu", 10.35, 107.07),
)


__all__ = [
    "Point",
    "ProvinceBoundary",
    "ProvinceIndex",
    "SPECIAL_LOCATIONS",
    "SpecialLocation",
    "distance_to_coast_km",
    "normalise_province_name",
    "point_in_polygon",
    "require_wgs84",
    "simplify_polyline",
]
