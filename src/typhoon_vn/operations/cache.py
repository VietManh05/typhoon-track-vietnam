"""Resilient Redis-compatible cache primitives for operational forecasts.

The module depends only on the small Redis command surface it uses, which keeps
contract tests independent from a running Redis service and a trained model.
"""

from __future__ import annotations

import hashlib
import json
import logging
from collections.abc import Iterator, Mapping
from typing import Any, Protocol
from urllib.parse import quote

logger = logging.getLogger(__name__)


class RedisLike(Protocol):
    """Redis command subset required by :class:`ForecastCache`."""

    def get(self, key: str) -> bytes | str | None: ...

    def setex(self, key: str, ttl_seconds: int, value: str) -> Any: ...

    def scan_iter(self, match: str) -> Iterator[bytes | str]: ...

    def delete(self, *keys: bytes | str) -> int: ...


def _canonical_json(value: Any) -> str:
    try:
        return json.dumps(
            value,
            ensure_ascii=True,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("cache values must be finite JSON-serializable data") from exc


class ForecastCache:
    """Fail-open forecast cache with versioned, deterministic keys.

    Cache failures are treated as misses so the caller can continue through its
    durable store or compute path. Keys include storm, input revision and model
    revision to prevent stale forecasts from crossing those boundaries.
    """

    def __init__(
        self,
        client: RedisLike | None,
        *,
        ttl_seconds: int = 1800,
        namespace: str = "typhoon-vn:v1",
    ) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        if not namespace or any(character.isspace() for character in namespace):
            raise ValueError("namespace must be non-empty and contain no whitespace")
        self.client = client
        self.ttl_seconds = ttl_seconds
        self.namespace = namespace.rstrip(":")

    def key(
        self,
        *,
        storm_id: str,
        input_revision: Any,
        model_revision: str,
    ) -> str:
        """Build a stable key whose digest covers the complete input revision."""
        if not storm_id.strip():
            raise ValueError("storm_id must be non-empty")
        if not model_revision.strip():
            raise ValueError("model_revision must be non-empty")
        digest = hashlib.sha256(
            _canonical_json(input_revision).encode("ascii")
        ).hexdigest()
        storm = quote(storm_id.strip(), safe="")
        model = quote(model_revision.strip(), safe="")
        return f"{self.namespace}:forecast:{storm}:{model}:{digest}"

    def get(self, key: str) -> Any | None:
        """Return decoded JSON or a miss when Redis/payload is unavailable."""
        if self.client is None:
            return None
        try:
            raw = self.client.get(key)
            if raw is None:
                return None
            if isinstance(raw, bytes):
                raw = raw.decode("utf-8")
            return json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError, OSError, RuntimeError):
            logger.warning("Cache read failed; continuing as a miss", exc_info=True)
            return None

    def put(self, key: str, payload: Mapping[str, Any]) -> bool:
        """Write JSON with TTL; return false instead of breaking the primary path."""
        encoded = _canonical_json(payload)
        if self.client is None:
            return False
        try:
            self.client.setex(key, self.ttl_seconds, encoded)
            return True
        except (OSError, RuntimeError):
            logger.warning(
                "Cache write failed; primary result remains valid", exc_info=True
            )
            return False

    def invalidate_storm(self, storm_id: str) -> int:
        """Delete every cached model/input revision for one storm."""
        if not storm_id.strip():
            raise ValueError("storm_id must be non-empty")
        if self.client is None:
            return 0
        storm = quote(storm_id.strip(), safe="")
        pattern = f"{self.namespace}:forecast:{storm}:*"
        try:
            keys = list(self.client.scan_iter(match=pattern))
            return self.client.delete(*keys) if keys else 0
        except (OSError, RuntimeError):
            logger.warning(
                "Cache invalidation failed; continuing safely", exc_info=True
            )
            return 0
