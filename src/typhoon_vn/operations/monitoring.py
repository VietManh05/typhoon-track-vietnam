"""Phase 6 operational monitoring, drift and health primitives."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping, Sequence


@dataclass(frozen=True, slots=True)
class OperationalCheck:
    """Structured dependency health result safe to expose in runbooks."""

    name: str
    ok: bool
    message: str
    checked_at: datetime
    latency_ms: float | None = None

    def model_dump(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": self.name,
            "ok": self.ok,
            "message": self.message,
            "checked_at": self.checked_at.isoformat(),
        }
        if self.latency_ms is not None:
            payload["latency_ms"] = round(self.latency_ms, 3)
        return payload


class MetricsRegistry:
    """Small in-process Prometheus text registry for API runtime metrics."""

    def __init__(self, *, buckets_ms: Sequence[float] | None = None) -> None:
        self.started_at = time.monotonic()
        self.buckets_ms = tuple(buckets_ms or (50, 100, 250, 500, 1000, 2500, 5000))
        self.request_count = 0
        self.error_count = 0
        self.latency_sum_ms = 0.0
        self.latency_buckets = {bucket: 0 for bucket in self.buckets_ms}
        self.status_counts: dict[int, int] = {}
        self.last_request_at: datetime | None = None

    def record_request(
        self, method: str, path: str, status_code: int, duration_ms: float
    ) -> None:
        """Record one request using low-cardinality aggregate metrics only."""
        if not math.isfinite(duration_ms) or duration_ms < 0:
            raise ValueError("duration_ms must be a non-negative finite number")
        self.request_count += 1
        self.status_counts[status_code] = self.status_counts.get(status_code, 0) + 1
        self.latency_sum_ms += duration_ms
        for bucket in self.buckets_ms:
            if duration_ms <= bucket:
                self.latency_buckets[bucket] += 1
        if status_code >= 400:
            self.error_count += 1
        self.last_request_at = datetime.now(timezone.utc)

    def render(self, *, extra_lines: Iterable[str] = ()) -> str:
        """Render Prometheus exposition text without leaking labels or secrets."""
        uptime = max(0.0, time.monotonic() - self.started_at)
        lines = [
            "# HELP typhoon_api_uptime_seconds Process uptime in seconds.",
            "# TYPE typhoon_api_uptime_seconds gauge",
            f"typhoon_api_uptime_seconds {uptime:.3f}",
            "# HELP typhoon_api_requests_total Total HTTP requests.",
            "# TYPE typhoon_api_requests_total counter",
            f"typhoon_api_requests_total {self.request_count}",
            "# HELP typhoon_api_errors_total Total HTTP responses >=400.",
            "# TYPE typhoon_api_errors_total counter",
            f"typhoon_api_errors_total {self.error_count}",
            "# HELP typhoon_api_request_latency_ms HTTP request latency.",
            "# TYPE typhoon_api_request_latency_ms histogram",
        ]
        for bucket in self.buckets_ms:
            lines.append(
                'typhoon_api_request_latency_ms_bucket{le="%s"} %d'
                % (int(bucket), self.latency_buckets[bucket])
            )
        lines.extend(
            [
                'typhoon_api_request_latency_ms_bucket{le="+Inf"} '
                f"{self.request_count}",
                f"typhoon_api_request_latency_ms_sum {self.latency_sum_ms:.3f}",
                f"typhoon_api_request_latency_ms_count {self.request_count}",
            ]
        )
        lines.extend(extra_lines)
        return "\n".join(lines).rstrip() + "\n"


def check_database_status(engine: Any) -> OperationalCheck:
    """Run a small SELECT 1 readiness probe against a SQLAlchemy engine."""
    from sqlalchemy import text

    started = time.perf_counter()
    now = datetime.now(timezone.utc)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return OperationalCheck(
            "database", True, "ok", now, (time.perf_counter() - started) * 1000
        )
    except Exception as exc:
        return OperationalCheck("database", False, type(exc).__name__, now)


def check_redis_status(client: Any | None) -> OperationalCheck:
    """Check Redis with PING when configured; None is reported explicitly."""
    now = datetime.now(timezone.utc)
    if client is None:
        return OperationalCheck("redis", False, "not_configured", now)
    started = time.perf_counter()
    try:
        response = client.ping()
        ok = bool(response)
        return OperationalCheck(
            "redis",
            ok,
            "ok" if ok else "ping_failed",
            now,
            (time.perf_counter() - started) * 1000,
        )
    except Exception as exc:
        return OperationalCheck("redis", False, type(exc).__name__, now)


@dataclass(frozen=True, slots=True)
class FreshnessReport:
    source: str
    last_update: datetime | None
    max_delay_seconds: int
    now: datetime

    @property
    def delay_seconds(self) -> float | None:
        if self.last_update is None:
            return None
        return (self.now - self.last_update).total_seconds()

    @property
    def ok(self) -> bool:
        delay = self.delay_seconds
        return delay is not None and 0 <= delay <= self.max_delay_seconds

    def model_dump(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "ok": self.ok,
            "last_update": self.last_update.isoformat() if self.last_update else None,
            "delay_seconds": self.delay_seconds,
            "max_delay_seconds": self.max_delay_seconds,
        }


def assess_freshness(
    source: str,
    last_update: datetime | None,
    *,
    now: datetime | None = None,
    max_delay_seconds: int = 6 * 3600,
) -> FreshnessReport:
    if max_delay_seconds <= 0:
        raise ValueError("max_delay_seconds must be positive")
    return FreshnessReport(
        source=source,
        last_update=last_update,
        max_delay_seconds=max_delay_seconds,
        now=now or datetime.now(timezone.utc),
    )


@dataclass(frozen=True, slots=True)
class SchemaDriftReport:
    expected: tuple[str, ...]
    actual: tuple[str, ...]

    @property
    def missing(self) -> tuple[str, ...]:
        return tuple(column for column in self.expected if column not in self.actual)

    @property
    def extra(self) -> tuple[str, ...]:
        return tuple(column for column in self.actual if column not in self.expected)

    @property
    def reordered(self) -> bool:
        common_actual = tuple(
            column for column in self.actual if column in self.expected
        )
        common_expected = tuple(
            column for column in self.expected if column in self.actual
        )
        return common_actual != common_expected

    @property
    def ok(self) -> bool:
        return not self.missing and not self.extra and not self.reordered

    def model_dump(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "missing": list(self.missing),
            "extra": list(self.extra),
            "reordered": self.reordered,
        }


def compare_schema(expected: Sequence[str], actual: Sequence[str]) -> SchemaDriftReport:
    if len(set(expected)) != len(expected) or len(set(actual)) != len(actual):
        raise ValueError("schemas must not contain duplicate columns")
    return SchemaDriftReport(tuple(expected), tuple(actual))


def population_stability_index(
    reference: Sequence[float], current: Sequence[float], *, bins: int = 10
) -> float:
    """Return PSI for drift monitoring; higher values mean stronger drift."""
    ref = [float(value) for value in reference if math.isfinite(float(value))]
    cur = [float(value) for value in current if math.isfinite(float(value))]
    if not ref or not cur:
        raise ValueError("reference and current must contain finite values")
    if bins < 2:
        raise ValueError("bins must be >= 2")
    lo = min(ref)
    hi = max(ref)
    if lo == hi:
        hi = lo + 1.0
    width = (hi - lo) / bins
    epsilon = 1e-6
    psi = 0.0
    for index in range(bins):
        left = lo + index * width
        right = hi if index == bins - 1 else left + width
        ref_count = sum(left <= value <= right for value in ref)
        cur_count = sum(left <= value <= right for value in cur)
        ref_share = max(ref_count / len(ref), epsilon)
        cur_share = max(cur_count / len(cur), epsilon)
        psi += (cur_share - ref_share) * math.log(cur_share / ref_share)
    return float(psi)


def summarize_numeric_distribution(values: Sequence[float]) -> Mapping[str, float]:
    finite = sorted(float(value) for value in values if math.isfinite(float(value)))
    if not finite:
        raise ValueError("values must contain at least one finite number")
    mid = len(finite) // 2
    median = finite[mid] if len(finite) % 2 else (finite[mid - 1] + finite[mid]) / 2
    return {
        "count": float(len(finite)),
        "min": finite[0],
        "median": median,
        "max": finite[-1],
        "mean": sum(finite) / len(finite),
    }
