"""Fixture-only cache contracts for Phase 4 prework."""

from __future__ import annotations

import fnmatch
import time

import pytest

from typhoon_vn.operations.cache import ForecastCache


class FakeRedis:
    def __init__(self) -> None:
        self.now = time.monotonic()
        self.values: dict[str, tuple[float, str]] = {}

    def get(self, key: str):
        item = self.values.get(key)
        if item is None:
            return None
        expires_at, value = item
        if expires_at <= self.now:
            del self.values[key]
            return None
        return value.encode("utf-8")

    def setex(self, key: str, ttl_seconds: int, value: str) -> bool:
        self.values[key] = (self.now + ttl_seconds, value)
        return True

    def scan_iter(self, match: str):
        for key in list(self.values):
            if fnmatch.fnmatchcase(key, match):
                yield key.encode("utf-8")

    def delete(self, *keys) -> int:
        deleted = 0
        for key in keys:
            decoded = key.decode("utf-8") if isinstance(key, bytes) else key
            deleted += self.values.pop(decoded, None) is not None
        return deleted


class FailingRedis:
    def get(self, key: str):
        raise OSError("redis unavailable")

    def setex(self, key: str, ttl_seconds: int, value: str):
        raise OSError("redis unavailable")

    def scan_iter(self, match: str):
        raise OSError("redis unavailable")
        yield

    def delete(self, *keys):
        raise OSError("redis unavailable")


def test_cache_key_is_canonical_and_revision_aware() -> None:
    cache = ForecastCache(None)
    first = cache.key(
        storm_id="VN 01",
        input_revision={"last_fix": "2026-09-19T00:00:00Z", "count": 4},
        model_revision="lstm/v2",
    )
    reordered = cache.key(
        storm_id="VN 01",
        input_revision={"count": 4, "last_fix": "2026-09-19T00:00:00Z"},
        model_revision="lstm/v2",
    )
    changed_input = cache.key(
        storm_id="VN 01",
        input_revision={"count": 5, "last_fix": "2026-09-19T00:00:00Z"},
        model_revision="lstm/v2",
    )
    changed_model = cache.key(
        storm_id="VN 01",
        input_revision={"count": 4, "last_fix": "2026-09-19T00:00:00Z"},
        model_revision="lstm/v3",
    )
    assert first == reordered
    assert len({first, changed_input, changed_model}) == 3
    assert ":forecast:VN%2001:lstm%2Fv2:" in first


def test_cache_hit_miss_and_ttl_expiry() -> None:
    redis = FakeRedis()
    cache = ForecastCache(redis, ttl_seconds=30)
    key = cache.key(storm_id="S1", input_revision="obs-1", model_revision="m1")
    assert cache.get(key) is None
    assert cache.put(key, {"forecast_id": "f1", "points": []}) is True
    assert cache.get(key) == {"forecast_id": "f1", "points": []}
    redis.now += 30
    assert cache.get(key) is None


def test_invalidation_is_scoped_to_one_storm_across_revisions() -> None:
    redis = FakeRedis()
    cache = ForecastCache(redis)
    s1_keys = [
        cache.key(storm_id="S1", input_revision="obs-1", model_revision="m1"),
        cache.key(storm_id="S1", input_revision="obs-2", model_revision="m2"),
    ]
    s2_key = cache.key(storm_id="S2", input_revision="obs-1", model_revision="m1")
    for key in [*s1_keys, s2_key]:
        cache.put(key, {"key": key})
    assert cache.invalidate_storm("S1") == 2
    assert all(cache.get(key) is None for key in s1_keys)
    assert cache.get(s2_key) == {"key": s2_key}


def test_redis_outage_fails_open_without_masking_primary_result() -> None:
    cache = ForecastCache(FailingRedis())
    key = cache.key(storm_id="S1", input_revision="obs", model_revision="m1")
    assert cache.get(key) is None
    assert cache.put(key, {"forecast_id": "still-valid"}) is False
    assert cache.invalidate_storm("S1") == 0


def test_cache_rejects_unsafe_configuration_and_payloads() -> None:
    with pytest.raises(ValueError, match="ttl_seconds"):
        ForecastCache(None, ttl_seconds=0)
    cache = ForecastCache(FakeRedis())
    with pytest.raises(ValueError, match="model_revision"):
        cache.key(storm_id="S1", input_revision="obs", model_revision=" ")
    with pytest.raises(ValueError, match="finite JSON"):
        cache.put("key", {"value": float("nan")})
