"""Offline tests for downloader retry and circuit isolation."""

from pathlib import Path
from urllib.error import HTTPError

import pytest

from typhoon_vn.ingestion import http
from typhoon_vn.ingestion.errors import DownloadError
from typhoon_vn.ingestion.http import (
    CircuitOpenError,
    CircuitState,
    DownloadPolicy,
    HttpDownloader,
)


class Response:
    status = 200
    headers = {}

    def __init__(self, body=b"ok"):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, _size):
        body, self.body = self.body, b""
        return body


def policy(**kw):
    values = {
        "attempts": 3,
        "backoff_seconds": 0,
        "jitter_seconds": 0,
        "circuit_failure_threshold": 3,
        "circuit_cooldown_seconds": 0,
    }
    values.update(kw)
    return DownloadPolicy(**values)


def test_success_and_transient_retries(tmp_path: Path, monkeypatch):
    calls = []

    def request(*_a, **_k):
        calls.append(1)
        if len(calls) == 1:
            raise TimeoutError("slow")
        return Response(b"payload")

    monkeypatch.setattr(http, "urlopen", request)
    result = HttpDownloader(policy()).fetch(
        source="jma", url="https://jma.test/file", destination=tmp_path / "x"
    )
    assert result.bytes_written == 7 and len(calls) == 2


def test_503_retries_404_does_not(tmp_path: Path, monkeypatch):
    codes = [503, 200]

    def request(*_a, **_k):
        code = codes.pop(0)
        if code != 200:
            raise HTTPError("https://x.test", code, "bad", {}, None)
        return Response()

    monkeypatch.setattr(http, "urlopen", request)
    HttpDownloader(policy()).fetch(
        source="noaa", url="https://x.test/a", destination=tmp_path / "a"
    )
    calls = []

    def missing(*_a, **_k):
        calls.append(1)
        raise HTTPError("https://x.test", 404, "missing", {}, None)

    monkeypatch.setattr(http, "urlopen", missing)
    with pytest.raises(DownloadError):
        HttpDownloader(policy()).fetch(
            source="noaa", url="https://x.test/b", destination=tmp_path / "b"
        )
    assert len(calls) == 1


def test_open_recovery_and_provider_isolation(tmp_path: Path, monkeypatch):
    def down(*_a, **_k):
        raise HTTPError("https://shared.test", 503, "down", {}, None)

    monkeypatch.setattr(http, "urlopen", down)
    downloader = HttpDownloader(policy(attempts=1, circuit_cooldown_seconds=3600))
    for i in range(3):
        with pytest.raises(DownloadError):
            downloader.fetch(
                source="jma", url="https://shared.test/a", destination=tmp_path / str(i)
            )
    assert downloader.circuit_state("jma", "https://shared.test/a") is CircuitState.OPEN
    with pytest.raises(CircuitOpenError):
        downloader.fetch(
            source="jma", url="https://shared.test/a", destination=tmp_path / "blocked"
        )
    monkeypatch.setattr(http, "urlopen", lambda *_a, **_k: Response())
    downloader.fetch(
        source="noaa", url="https://shared.test/a", destination=tmp_path / "isolated"
    )
    downloader.policy = policy(attempts=1, circuit_cooldown_seconds=0)
    downloader.fetch(
        source="jma", url="https://shared.test/a", destination=tmp_path / "probe"
    )
    assert (
        downloader.circuit_state("jma", "https://shared.test/a") is CircuitState.CLOSED
    )


def test_half_open_probe_releases_on_unexpected_network_error(
    tmp_path: Path, monkeypatch
):
    def reset(*_a, **_k):
        raise ConnectionResetError("peer reset")

    monkeypatch.setattr(http, "urlopen", reset)
    downloader = HttpDownloader(
        policy(attempts=1, circuit_failure_threshold=1, circuit_cooldown_seconds=0)
    )
    for name in ("first", "probe"):
        with pytest.raises(DownloadError):
            downloader.fetch(
                source="jma", url="https://x.test/a", destination=tmp_path / name
            )
    monkeypatch.setattr(http, "urlopen", lambda *_a, **_k: Response())
    downloader.fetch(source="jma", url="https://x.test/a", destination=tmp_path / "ok")
    assert downloader.circuit_state("jma", "https://x.test/a") is CircuitState.CLOSED
