"""Recent JMA tropical-cyclone guidance in the dashboard API contract."""

from __future__ import annotations

import json
import math
import re
import time
from datetime import datetime, timedelta, timezone
from threading import RLock
from urllib.request import Request, urlopen

from typhoon_vn.features.geo import destination_point

BASE = "https://www.jma.go.jp/bosai/typhoon/data/"
STORM_ID = re.compile(r"^TC\d{4}$")
ATTRIBUTION = (
    "JMA data processed by Typhoon VN; source: "
    "https://www.jma.go.jp/bosai/typhoon/. Follow NCHMF for official warnings "
    "in Vietnam."
)
_CACHE: dict[str, tuple[float, object]] = {}
_LOCK = RLock()


class JmaLiveError(RuntimeError):
    """A live JMA response is unavailable, stale, or malformed."""


def _read(path: str) -> object:
    now = time.monotonic()
    with _LOCK:
        cached = _CACHE.get(path)
        if cached and cached[0] > now:
            return cached[1]
    request = Request(
        BASE + path,
        headers={
            "Accept": "application/json",
            "User-Agent": "TyphoonVN/0.1 (public JMA bulletin reader)",
        },
    )
    try:
        with urlopen(request, timeout=8) as response:
            body = response.read(500_001)
        if len(body) > 500_000:
            raise JmaLiveError("JMA response exceeds size limit")
        value = json.loads(body)
    except (OSError, TimeoutError, ValueError) as error:
        raise JmaLiveError("JMA source unavailable or malformed") from error
    with _LOCK:
        _CACHE[path] = (now + 180, value)
    return value


def _fresh(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        issued = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if issued.tzinfo is None:
            return False
        age = datetime.now(timezone.utc) - issued.astimezone(timezone.utc)
        return -timedelta(minutes=30) <= age <= timedelta(hours=24)
    except ValueError:
        return False


def _number(value: object) -> float | None:
    if value in (None, ""):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _value(item: object, *keys: str) -> object:
    for key in keys:
        if not isinstance(item, dict):
            return None
        item = item.get(key)
    return item


def _position(value: object) -> tuple[float, float]:
    if not isinstance(value, list) or len(value) < 2:
        raise JmaLiveError("JMA position is invalid")
    lat, lon = _number(value[0]), _number(value[1])
    if lat is None or lon is None or not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise JmaLiveError("JMA position is invalid")
    return lat, lon


def _category(value: object) -> str:
    return (
        value
        if isinstance(value, str)
        and value in {"TD", "TS", "STS", "TY", "STY", "SUPERTY"}
        else "UNK"
    )


def _source_url(storm_id: str) -> str:
    return (
        "https://www.jma.go.jp/bosai/map.html#contents=typhoon"
        f"&elem=root&typhoon={storm_id}"
    )


def _targets() -> list[dict]:
    value = _read("targetTc.json")
    if not isinstance(value, list) or len(value) > 20:
        raise JmaLiveError("JMA active list is invalid")
    for item in value:
        if (
            not isinstance(item, dict)
            or not STORM_ID.fullmatch(str(item.get("tropicalCyclone", "")))
            or not _fresh(item.get("issue"))
        ):
            raise JmaLiveError("JMA active list is invalid or stale")
    return value


def _storm(storm_id: str) -> tuple[dict, list[dict], dict]:
    if not STORM_ID.fullmatch(storm_id):
        raise JmaLiveError("Invalid JMA storm ID")
    value = _read(f"{storm_id}/specifications.json")
    if (
        not isinstance(value, list)
        or not value
        or not all(isinstance(item, dict) for item in value)
    ):
        raise JmaLiveError("JMA storm bulletin is invalid")
    title = value[0]
    analysis = next((item for item in value if item.get("advancedHours") == 0), None)
    issue = _value(title, "issue", "UTC")
    valid = _value(analysis, "validtime", "UTC")
    if not _fresh(issue) or not _fresh(valid):
        raise JmaLiveError("JMA storm bulletin is invalid or stale")
    lat, lon = _position(_value(analysis, "position", "deg"))
    wind = _number(_value(analysis, "maximumWind", "sustained", "m/s"))
    pressure = _number(_value(analysis, "pressure"))
    if wind is not None and not 0 <= wind <= 150:
        raise JmaLiveError("JMA wind value is invalid")
    if pressure is not None and not 850 <= pressure <= 1050:
        raise JmaLiveError("JMA pressure is invalid")
    latest = {
        "timestamp": valid,
        "lat": lat,
        "lon": lon,
        "wind_ms": wind,
        "pressure_hpa": pressure,
        "intensity": _category(_value(analysis, "category", "en")),
        "source": "JMA RSMC Tokyo (processed by Typhoon VN)",
        "source_url": _source_url(storm_id),
    }
    return title, value, latest


def active_typhoons() -> dict:
    items = []
    for target in _targets():
        storm_id = target["tropicalCyclone"]
        title, _, latest = _storm(storm_id)
        items.append(
            {
                "id": storm_id,
                "name": _value(title, "name", "en")
                or title.get("typhoonNumber")
                or storm_id,
                "year": int(title["issue"]["UTC"][:4]),
                "latest": latest,
                "observation_count": 1,
                "status": "active",
            }
        )
    return {
        "typhoons": items,
        "feedAvailable": True,
        "source": "JMA RSMC Tokyo",
        "disclaimer": ATTRIBUTION,
    }


def _circle(lat: float, lon: float, radius_km: float) -> dict:
    ring = []
    for angle in range(0, 361, 10):
        y, x = destination_point(lat, lon, angle, radius_km)
        ring.append([x, y])
    return {"type": "Polygon", "coordinates": [ring]}


def storm_track(storm_id: str) -> dict:
    if storm_id not in {item["tropicalCyclone"] for item in _targets()}:
        raise KeyError(storm_id)
    title, items, latest = _storm(storm_id)
    points = []
    for item in items:
        hours = item.get("advancedHours")
        if isinstance(hours, bool) or not isinstance(hours, int) or not 0 < hours <= 72:
            continue
        lat, lon = _position(_value(item, "position", "deg"))
        radius = _number(_value(item, "probabilityCircleRadius", "km"))
        valid = _value(item, "validtime", "UTC")
        if radius is None or not 0 <= radius <= 1000 or not isinstance(valid, str):
            raise JmaLiveError("JMA forecast point is invalid")
        points.append(
            {
                "horizon_hours": hours,
                "valid_time": valid,
                "lat": lat,
                "lon": lon,
                "intensity": _category(_value(item, "category", "en")),
                "radius_km": radius,
                "cone": _circle(lat, lon, radius),
                "wind_ms": _number(_value(item, "maximumWind", "sustained", "m/s")),
                "pressure_hpa": _number(item.get("pressure")),
            }
        )
    issue = title["issue"]["UTC"]
    issue_ms = int(
        datetime.fromisoformat(issue.replace("Z", "+00:00")).timestamp() * 1000
    )
    return {
        "storm_id": storm_id,
        "observations": [latest],
        "forecast": (
            {
                "forecast_id": f"JMA-{storm_id}-{issue_ms}",
                "storm_id": storm_id,
                "issue_time": issue,
                "generated_at": issue,
                "model_version": "JMA RSMC Tokyo",
                "model_kind": "external guidance",
                "dataset_version": "JMA live bulletin",
                "sources": ["JMA RSMC Tokyo"],
                "uncertainty_method": (
                    "JMA probability circle radius; Typhoon VN approximates circles "
                    "for map display."
                ),
                "warnings": [
                    "Regional JMA guidance. Follow NCHMF for official warnings in Vietnam."
                ],
                "disclaimer": (
                    f"JMA data processed by Typhoon VN. Source: {_source_url(storm_id)}. "
                    "Not an official Vietnam warning."
                ),
                "points": points,
            }
            if points
            else None
        ),
    }
