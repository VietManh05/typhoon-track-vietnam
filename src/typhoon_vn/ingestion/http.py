"""Reliable HTTP downloads with bounded retries and isolated circuits."""

from __future__ import annotations

import hashlib
import logging
import os
import random
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from http.client import HTTPException
from pathlib import Path
from threading import RLock
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from typhoon_vn.ingestion.errors import DownloadError, DownloadTimeoutError
from typhoon_vn.ingestion.models import DownloadResult

LOGGER = logging.getLogger(__name__)
RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitOpenError(DownloadError):
    """A provider circuit is rejecting calls during its cooldown."""


@dataclass(frozen=True, slots=True)
class DownloadPolicy:
    attempts: int = 3
    timeout_seconds: float = 60
    backoff_seconds: float = 1.0
    jitter_seconds: float = 0.25
    chunk_size: int = 1024 * 1024
    circuit_failure_threshold: int = 3
    circuit_cooldown_seconds: float = 30.0

    def __post_init__(self) -> None:
        if self.attempts < 1 or self.timeout_seconds <= 0 or self.chunk_size < 1:
            raise ValueError("attempts, timeout and chunk size must be positive")
        if self.backoff_seconds < 0 or self.jitter_seconds < 0:
            raise ValueError("backoff and jitter must be non-negative")
        if self.circuit_failure_threshold < 1 or self.circuit_cooldown_seconds < 0:
            raise ValueError("invalid circuit breaker policy")


@dataclass(slots=True)
class _Circuit:
    state: CircuitState = CircuitState.CLOSED
    failures: int = 0
    opened_at: float = 0.0
    probing: bool = False


class HttpDownloader:
    """Stream a URL atomically with transient retries and failure isolation."""

    def __init__(self, policy: DownloadPolicy | None = None) -> None:
        self.policy = policy or DownloadPolicy()
        self._circuits: dict[str, _Circuit] = {}
        self._lock = RLock()

    @staticmethod
    def _key(source: str, url: str) -> str:
        return source.strip().casefold() + "@" + (urlsplit(url).hostname or "unknown")

    @staticmethod
    def _safe_url(url: str) -> str:
        parsed = urlsplit(url)
        return f"{parsed.scheme}://{parsed.hostname or 'unknown'}{parsed.path}"

    def circuit_state(self, source: str, url: str) -> CircuitState:
        key = self._key(source, url)
        with self._lock:
            circuit = self._circuits.get(key)
            if circuit is None:
                return CircuitState.CLOSED
            if (
                circuit.state is CircuitState.OPEN
                and time.monotonic() - circuit.opened_at
                >= self.policy.circuit_cooldown_seconds
            ):
                return CircuitState.HALF_OPEN
            return circuit.state

    def _admit(self, key: str) -> CircuitState:
        with self._lock:
            circuit = self._circuits.setdefault(key, _Circuit())
            if circuit.state is CircuitState.OPEN:
                if (
                    time.monotonic() - circuit.opened_at
                    < self.policy.circuit_cooldown_seconds
                ):
                    raise CircuitOpenError(f"circuit open for {key}")
                circuit.state = CircuitState.HALF_OPEN
            if circuit.state is CircuitState.HALF_OPEN:
                if circuit.probing:
                    raise CircuitOpenError(f"circuit probe in progress for {key}")
                circuit.probing = True
            return circuit.state

    def _success(self, key: str) -> None:
        with self._lock:
            self._circuits[key] = _Circuit()

    def _failure(self, key: str) -> CircuitState:
        with self._lock:
            circuit = self._circuits.setdefault(key, _Circuit())
            circuit.probing = False
            circuit.failures += 1
            if (
                circuit.state is CircuitState.HALF_OPEN
                or circuit.failures >= self.policy.circuit_failure_threshold
            ):
                circuit.state = CircuitState.OPEN
                circuit.opened_at = time.monotonic()
            return circuit.state

    @staticmethod
    def _retryable(error: Exception) -> bool:
        if isinstance(error, HTTPError):
            return error.code in RETRYABLE_STATUS
        return isinstance(
            error,
            (
                TimeoutError,
                URLError,
                ConnectionError,
                HTTPException,
                DownloadTimeoutError,
            ),
        )

    def fetch(
        self,
        *,
        source: str,
        url: str,
        destination: Path,
        expected_sha256: str | None = None,
    ) -> DownloadResult:
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_suffix(destination.suffix + ".part")
        key = self._key(source, url)
        host = urlsplit(url).hostname or "unknown"
        safe_url = self._safe_url(url)
        circuit_state = self._admit(key)
        last_error: Exception | None = None
        for attempt in range(1, self.policy.attempts + 1):
            started = time.perf_counter()
            status_code = None
            try:
                request = Request(
                    url, headers={"User-Agent": "typhoon-vn-forecast-system/0.1"}
                )
                with urlopen(request, timeout=self.policy.timeout_seconds) as response:
                    status_code = getattr(response, "status", 200)
                    digest, size = hashlib.sha256(), 0
                    with temporary.open("wb") as handle:
                        while chunk := response.read(self.policy.chunk_size):
                            handle.write(chunk)
                            digest.update(chunk)
                            size += len(chunk)
                    if size == 0:
                        raise DownloadError(f"empty response body for {safe_url}")
                    checksum = digest.hexdigest()
                    if expected_sha256 and checksum.lower() != expected_sha256.lower():
                        raise DownloadError(f"checksum mismatch for {safe_url}")
                    os.replace(temporary, destination)
                    self._success(key)
                    LOGGER.info(
                        "download succeeded",
                        extra={
                            "provider": source,
                            "host": host,
                            "url": safe_url,
                            "attempt": attempt,
                            "status_code": status_code,
                            "elapsed_ms": round(
                                (time.perf_counter() - started) * 1000, 2
                            ),
                            "exception_type": None,
                            "circuit_state": CircuitState.CLOSED.value,
                        },
                    )
                    return DownloadResult(
                        source=source,
                        url=url,
                        local_path=str(destination),
                        sha256=checksum,
                        downloaded_at=datetime.now(timezone.utc),
                        bytes_written=size,
                        etag=response.headers.get("ETag"),
                        last_modified=response.headers.get("Last-Modified"),
                    )
            # OSError/HTTPException cover mid-body resets and local write errors,
            # so a half-open probe always reports back to its circuit.
            except (OSError, HTTPException, DownloadError) as error:
                temporary.unlink(missing_ok=True)
                if isinstance(error, TimeoutError):
                    error = DownloadTimeoutError(
                        f"download timed out after {self.policy.timeout_seconds}s: {safe_url}: {error}"
                    )
                last_error = error
                status_code = (
                    error.code if isinstance(error, HTTPError) else status_code
                )
                retryable = self._retryable(error)
                LOGGER.warning(
                    "download attempt failed",
                    extra={
                        "provider": source,
                        "host": host,
                        "url": safe_url,
                        "attempt": attempt,
                        "status_code": status_code,
                        "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
                        "exception_type": type(error).__name__,
                        "circuit_state": circuit_state.value,
                        "retryable": retryable,
                    },
                )
                if attempt == self.policy.attempts or not retryable:
                    self._failure(key)
                    break
                delay = self.policy.backoff_seconds * 2 ** (
                    attempt - 1
                ) + random.uniform(0, self.policy.jitter_seconds)
                time.sleep(delay)
        raise DownloadError(
            f"could not download {safe_url}: {last_error}"
        ) from last_error


__all__ = ["CircuitOpenError", "CircuitState", "DownloadPolicy", "HttpDownloader"]
