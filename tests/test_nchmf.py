"""NCHMF ingestion: source markup, provenance, failures and API integration."""

from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from typhoon_vn.api.app import create_app
from typhoon_vn.settings import Settings
from typhoon_vn.weather.errors import ProviderUnavailableError
from typhoon_vn.weather.nchmf import NchmfService, parse_home, source_url

HTML = """<h2>THỜI TIẾT CÁC TỈNH / THÀNH - CẬP NHẬT LÚC 13h - 21/09/2026</h2>
<ul><li><a class="name-wt-city" href="/kttvsite/vi-VN/1/ha-noi-w1.html">Hà Nội</a>
<div class="icon-wt-city"><img src="icon.png"></div><div class="temp-wt-city">30°C</div></li></ul>
<a href="/kttvsite/vi-VN/1/mua-post123.html">Tin mưa lớn<label>(21/09/2026 12:30:00)</label></a>
<a href="/kttvsite/vi-VN/1/lu-post124.html">Tin lũ<label>(21/09/2026 12:30:00)</label></a>
<script>alert("not content")</script>""".encode()
NOW = datetime(2026, 9, 21, 7, tzinfo=UTC)


def test_parse_temperature_timestamp_and_distinct_bulletins():
    value = parse_home(HTML, retrieved_at=NOW)
    assert value["observedAt"] == "2026-09-21T13:00:00+07:00"
    assert value["observations"][0]["temperatureC"] == 30
    assert value["observations"][0]["name"] == "Hà Nội"
    assert len({b["id"] for b in value["bulletins"]}) == 2
    assert value["bulletins"][0]["issuedAt"].endswith("+07:00")
    assert value["metadata"]["provider"] == "nchmf"
    assert len(value["metadata"]["sha256"]) == 64
    assert value["metadata"]["isStale"] is False
    assert "wind" not in value["observations"][0]


@pytest.mark.parametrize(
    "raw",
    [
        b"",
        b"<html>login</html>",
        HTML.replace("30°C".encode(), b"unknown"),
        HTML.replace(b"13h - 21/09/2026", b"99h - 21/09/2026"),
        HTML.replace(b"30", b"999"),
    ],
)
def test_schema_drift_fails_closed(raw):
    with pytest.raises(ValueError):
        parse_home(raw, retrieved_at=NOW)


@pytest.mark.parametrize(
    "url",
    [
        "http://nchmf.gov.vn/kttvsite/",
        "https://evil.example/kttvsite/",
        "https://nchmf.gov.vn.evil.example/kttvsite/",
        "https://nchmf.gov.vn/bin/",
    ],
)
def test_links_cannot_escape_official_public_source(url):
    with pytest.raises(ValueError):
        source_url(url)


def test_cache_single_fetch_and_stale_fallback():
    calls = []

    def fetch(timeout):
        calls.append(timeout)
        if len(calls) > 1:
            raise TimeoutError()
        return HTML

    service = NchmfService(transport=fetch)
    first = service.get()
    first["observations"].clear()
    assert service.get()["observations"]
    assert len(calls) == 1
    service.expires = 0
    stale = service.get()
    assert stale["metadata"]["isStale"] is True
    assert stale["observations"]
    assert service.get()["metadata"]["isStale"] is True
    assert len(calls) == 2


def test_no_cache_failure_and_backoff():
    calls = []

    def fail(timeout):
        calls.append(timeout)
        return b"<html>maintenance</html>"

    service = NchmfService(transport=fail)
    for _ in range(2):
        with pytest.raises(ProviderUnavailableError):
            service.get()
    assert len(calls) == 1


def test_api_and_cli_use_same_source_contract(monkeypatch, tmp_path):
    from typhoon_vn.cli import main
    from typhoon_vn.weather.nchmf import NchmfService

    expected = parse_home(HTML, retrieved_at=NOW)
    monkeypatch.setattr(NchmfService, "get", lambda self: expected)
    app = create_app(
        Settings(cache_enabled=False, operational_database_url="sqlite:///:memory:")
    )
    with TestClient(app) as client:
        response = client.get("/api/weather/nchmf")
        assert response.status_code == 200
        assert response.json() == expected
    target = tmp_path / "weather.json"
    assert main(["scrape-nchmf", "--output", str(target)]) == 0
    assert "nchmf" in Path(target).read_text(encoding="utf-8")


def test_api_source_failure_is_503(monkeypatch):
    def fail(self):
        raise ProviderUnavailableError("source down")

    monkeypatch.setattr(NchmfService, "get", fail)
    app = create_app(
        Settings(cache_enabled=False, operational_database_url="sqlite:///:memory:")
    )
    with TestClient(app) as client:
        assert client.get("/api/weather/nchmf").status_code == 503
