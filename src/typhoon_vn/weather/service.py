"""Provider orchestration, normalized caching and stale fallback."""

from __future__ import annotations

from typing import Literal

from .cache import WeatherCache
from .errors import WeatherProviderError
from .locations import BY_ID, search_locations
from .models import WeatherLocation


class WeatherService:
    TTLS = {"current": 600, "hourly": 1200, "daily": 7200, "alerts": 300}

    def __init__(self, provider, *, cache: WeatherCache | None = None):
        self.provider = provider
        self.cache = cache or WeatherCache()

    def location(self, location_id: str) -> WeatherLocation:
        try:
            return BY_ID[location_id]
        except KeyError as exc:
            raise KeyError("weather location not found") from exc

    def search(self, query: str):
        return search_locations(query)

    def get(
        self, kind: Literal["current", "hourly", "daily", "alerts"], location_id: str
    ):
        location = self.location(location_id)
        key = f"weather:{kind}:{self.provider.__class__.__name__.lower()}:{location.id}"
        hit = self.cache.get(key)
        if hit:
            return hit[0]
        try:
            value = getattr(self.provider, kind)(location)
            dumped = (
                [x.model_dump(mode="json", by_alias=True) for x in value]
                if isinstance(value, list)
                else value.model_dump(mode="json", by_alias=True)
            )
            self.cache.put(key, dumped, self.TTLS[kind])
            return dumped
        except WeatherProviderError:
            stale = self.cache.get(key, allow_stale=True)
            if stale:
                return stale[0]
            raise
