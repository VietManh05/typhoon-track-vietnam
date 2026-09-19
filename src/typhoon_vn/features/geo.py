"""Great-circle geodesy helpers used across the feature pipeline.

These functions keep the core ideas of the original ``share_func.py``
(Haversine distance, initial bearing, destination point) but are written as
pure, individually testable units with explicit units (kilometres / degrees).
"""

from __future__ import annotations

import math

EARTH_RADIUS_KM = 6371.0088


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two points in kilometres."""

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2.0) ** 2
    )
    return 2.0 * EARTH_RADIUS_KM * math.asin(min(1.0, math.sqrt(a)))


def bearing_deg(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Initial bearing from point 1 to point 2, in degrees clockwise from north."""

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dlam = math.radians(lon2 - lon1)
    x = math.sin(dlam) * math.cos(phi2)
    y = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(
        dlam
    )
    return (math.degrees(math.atan2(x, y)) + 360.0) % 360.0


def destination_point(
    lat: float, lon: float, bearing: float, distance_km: float
) -> tuple[float, float]:
    """Point reached when travelling ``distance_km`` along ``bearing`` from (lat, lon)."""

    delta = distance_km / EARTH_RADIUS_KM
    theta = math.radians(bearing)
    phi1 = math.radians(lat)
    lam1 = math.radians(lon)

    phi2 = math.asin(
        math.sin(phi1) * math.cos(delta)
        + math.cos(phi1) * math.sin(delta) * math.cos(theta)
    )
    lam2 = lam1 + math.atan2(
        math.sin(theta) * math.sin(delta) * math.cos(phi1),
        math.cos(delta) - math.sin(phi1) * math.sin(phi2),
    )
    lon2 = (math.degrees(lam2) + 540.0) % 360.0 - 180.0
    return math.degrees(phi2), lon2


def bearing_change_deg(bearing_from: float, bearing_to: float) -> float:
    """Signed smallest turn from one bearing to another, in degrees (-180, 180]."""

    return ((bearing_to - bearing_from + 180.0) % 360.0) - 180.0
