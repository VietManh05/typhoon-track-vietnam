"""Verify the public Pages demo against the current local frontend build."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "https://baoviet2026.pages.dev"
ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "src" / "typhoon_vn" / "dashboard" / "index.html"
RESULTS = []


def fetch(path: str, method: str = "GET") -> tuple[int, str, bytes]:
    request = Request(
        BASE + path, method=method, headers={"User-Agent": "TyphoonVN-Demo-Smoke/1"}
    )
    try:
        response = urlopen(request, timeout=20)
    except HTTPError as error:
        response = error
    with response:
        return (
            response.status,
            response.headers.get("Content-Type", ""),
            response.read(),
        )


def check(name: str, passed: bool, detail: str) -> None:
    RESULTS.append({"check": name, "pass": passed, "detail": detail})


def json_route(name: str, path: str, expected_status: int):
    status, content_type, body = fetch(path)
    try:
        payload = json.loads(body)
    except (ValueError, UnicodeDecodeError):
        payload = None
    passed = (
        status == expected_status
        and "application/json" in content_type
        and isinstance(payload, dict)
    )
    check(name, passed, f"HTTP {status}, {content_type}")
    return payload if passed else {}


def main() -> None:
    local_html = INDEX.read_text(encoding="utf-8")
    assets = re.findall(r'(?:src|href)="(/assets/[^"?]+)', local_html)
    status, content_type, remote_html = fetch("/")
    check("homepage", status == 200 and "text/html" in content_type, f"HTTP {status}")
    html = remote_html.decode("utf-8", errors="replace")
    check(
        "release-assets-match",
        bool(assets) and all(asset in html for asset in assets),
        str(assets),
    )
    for asset in assets:
        asset_status, _, _ = fetch(asset)
        check("asset:" + asset, asset_status == 200, f"HTTP {asset_status}")

    health = json_route("health", "/health", 200)
    capabilities = health.get("capabilities", {})
    check("no-storm-feed", capabilities.get("stormFeed") is False, str(capabilities))
    check(
        "no-alert-delivery",
        capabilities.get("alertDelivery") is False,
        str(capabilities),
    )
    ready = json_route("ready", "/ready", 503)
    check(
        "not-operational", ready.get("status") == "not_ready", str(ready.get("status"))
    )
    auth = json_route("auth-capabilities", "/auth/capabilities", 200)
    check("no-demo-login", auth.get("available") is False, str(auth.get("available")))
    session = json_route("auth-session", "/auth/session", 503)
    check(
        "no-false-session",
        session.get("authenticated") is False,
        str(session.get("authenticated")),
    )
    storms = json_route("active-storms", "/typhoons/active", 200)
    check(
        "storm-state-honest",
        storms.get("feedAvailable") is False,
        str(storms.get("feedAvailable")),
    )
    json_route("alerts-unavailable", "/alerts", 503)
    json_route("nchmf-unavailable-on-pages", "/api/weather/nchmf", 503)
    status, content_type, _ = fetch("/token", "POST")
    check(
        "token-unavailable",
        status == 503 and "application/json" in content_type,
        f"HTTP {status}",
    )
    weather = json_route(
        "weather-bundle", "/api/weather/bundle?location_id=da-nang", 200
    )
    check("weather-has-data", bool(weather), f"fields={len(weather)}")
    current = weather.get("current", {})
    metadata = current.get("metadata", {}) if isinstance(current, dict) else {}
    check(
        "weather-source-labelled",
        metadata.get("provider") == "open-meteo" and bool(metadata.get("retrievedAt")),
        str(metadata.get("provider")),
    )

    report = {
        "url": BASE,
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "localIndexSha256": hashlib.sha256(INDEX.read_bytes()).hexdigest(),
        "passed": all(row["pass"] for row in RESULTS),
        "results": RESULTS,
    }
    evidence = ROOT / "reports" / "demo-release-smoke-2026-09-23.json"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"{sum(row['pass'] for row in RESULTS)}/{len(RESULTS)} checks passed; {evidence}"
    )
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
