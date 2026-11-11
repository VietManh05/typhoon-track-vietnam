"""TTL weather cache with stale fallback; Redis-compatible and bounded in memory."""

from __future__ import annotations

import json
import time
from collections import OrderedDict
from typing import Any

from redis.exceptions import RedisError


class WeatherCache:
    def __init__(self, client=None, *, max_entries: int = 256):
        self.client = client
        self.max_entries = max_entries
        self.memory: OrderedDict[str, tuple[float, Any]] = OrderedDict()

    def get(self, key: str, *, allow_stale: bool = False) -> tuple[Any, bool] | None:
        now = time.time()
        if self.client:
            try:
                raw = self.client.get(key)
                if raw:
                    data = json.loads(raw)
                    expired = data["expires_at"] < now
                    if not expired or allow_stale:
                        return data["value"], expired
            except (OSError, RuntimeError, ValueError, TypeError, RedisError):
                pass
        item = self.memory.get(key)
        if not item:
            return None
        expires, value = item
        expired = expires < now
        if expired and not allow_stale:
            return None
        self.memory.move_to_end(key)
        return value, expired

    def put(self, key: str, value: Any, ttl: int) -> None:
        payload = {"expires_at": time.time() + ttl, "value": value}
        self.memory[key] = (payload["expires_at"], value)
        self.memory.move_to_end(key)
        while len(self.memory) > self.max_entries:
            self.memory.popitem(last=False)
        if self.client:
            try:
                self.client.setex(
                    key, ttl * 3, json.dumps(payload, separators=(",", ":"))
                )
            except (OSError, RuntimeError, TypeError, ValueError, RedisError):
                pass
