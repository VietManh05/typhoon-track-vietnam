"""Retrying HTTPS downloads with content-addressable provenance."""

from __future__ import annotations

import hashlib
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from typhoon_vn.ingestion.errors import DownloadError
from typhoon_vn.ingestion.models import DownloadResult


@dataclass(frozen=True, slots=True)
class DownloadPolicy:
    """Network behaviour that is explicit, bounded, and testable."""

    attempts: int = 4
    timeout_seconds: int = 60
    backoff_seconds: float = 1.0
    chunk_size: int = 1024 * 1024


class HttpDownloader:
    """Fetch a URL atomically and calculate SHA-256 while streaming it."""

    def __init__(self, policy: DownloadPolicy | None = None) -> None:
        self.policy = policy or DownloadPolicy()

    def fetch(
        self,
        *,
        source: str,
        url: str,
        destination: Path,
        expected_sha256: str | None = None,
    ) -> DownloadResult:
        """Download to ``destination`` or raise without leaving a partial file."""

        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_suffix(f"{destination.suffix}.part")
        last_error: Exception | None = None
        for attempt in range(1, self.policy.attempts + 1):
            try:
                request = Request(
                    url,
                    headers={"User-Agent": "typhoon-vn-forecast-system/0.1"},
                )
                with urlopen(request, timeout=self.policy.timeout_seconds) as response:
                    digest = hashlib.sha256()
                    bytes_written = 0
                    with temporary.open("wb") as handle:
                        while chunk := response.read(self.policy.chunk_size):
                            handle.write(chunk)
                            digest.update(chunk)
                            bytes_written += len(chunk)
                    checksum = digest.hexdigest()
                    if expected_sha256 and checksum.lower() != expected_sha256.lower():
                        temporary.unlink(missing_ok=True)
                        raise DownloadError(
                            f"checksum mismatch for {url}: expected {expected_sha256}, "
                            f"received {checksum}"
                        )
                    os.replace(temporary, destination)
                    return DownloadResult(
                        source=source,
                        url=url,
                        local_path=str(destination),
                        sha256=checksum,
                        downloaded_at=datetime.now(timezone.utc),
                        bytes_written=bytes_written,
                        etag=response.headers.get("ETag"),
                        last_modified=response.headers.get("Last-Modified"),
                    )
            except (HTTPError, URLError, TimeoutError, DownloadError) as error:
                last_error = error
                temporary.unlink(missing_ok=True)
                retryable = not isinstance(error, HTTPError) or error.code >= 500
                if attempt == self.policy.attempts or not retryable:
                    break
                time.sleep(self.policy.backoff_seconds * (2 ** (attempt - 1)))
        raise DownloadError(f"could not download {url}: {last_error}")
