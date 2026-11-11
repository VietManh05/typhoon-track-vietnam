"""Verify the dashboard and its API over a running HTTP server."""

import json
import os
import re
import urllib.error
import urllib.request

BASE_URL = os.getenv("TYPHOON_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
EXPECTED_STORM_ID = os.getenv("TYPHOON_EXPECT_STORM_ID", "")
API_KEY = os.getenv("TYPHOON_API_KEY", "")


def request(path: str):
    headers = {"X-API-Key": API_KEY} if API_KEY else {}
    return urllib.request.urlopen(
        urllib.request.Request(f"{BASE_URL}{path}", headers=headers), timeout=10
    )


def check(path: str, expected_content_type: str):
    try:
        with request(path) as response:
            content_type = response.headers.get("content-type", "")
            payload = response.read()
            ok = response.status == 200 and expected_content_type in content_type
            print(
                f"ROUTE: {path:<42} STATUS: {response.status} "
                f"LEN: {len(payload):<8} CT: {content_type} "
                f"RESULT: {'PASS' if ok else 'FAIL'}"
            )
            return ok, payload
    except (OSError, urllib.error.HTTPError) as error:
        print(f"ROUTE: {path:<42} ERROR: {error} RESULT: FAIL")
        return False, b""


all_ok = True
home_ok, home = check("/", "text/html")
all_ok &= home_ok
for path, expected_content_type in [
    ("/favicon.svg", "image/svg+xml"),
    ("/data/vietnam_provinces.geojson", "application/geo+json"),
    ("/data/vietnam_islands.json", "application/json"),
    ("/health", "application/json"),
    ("/ready", "application/json"),
    ("/version", "application/json"),
]:
    ok, _ = check(path, expected_content_type)
    all_ok &= ok

for asset in re.findall(rb'(?:src|href)="(/assets/[^"]+)"', home):
    ok, _ = check(asset.decode("utf-8"), "")
    all_ok &= ok
for font in re.findall(rb'href="(/fonts/[^"]+)"', home):
    ok, _ = check(font.decode("utf-8"), "font/woff2")
    all_ok &= ok

active_ok, active_body = check("/typhoons/active", "application/json")
all_ok &= active_ok
if active_ok:
    active = json.loads(active_body)["typhoons"]
    print(f"ACTIVE STORMS: {len(active)}")
    if EXPECTED_STORM_ID:
        matching = [storm for storm in active if storm["id"] == EXPECTED_STORM_ID]
        expected_ok = len(matching) == 1
        print(
            f"EXPECTED STORM: {EXPECTED_STORM_ID} "
            f"RESULT: {'PASS' if expected_ok else 'FAIL'}"
        )
        all_ok &= expected_ok
        track_ok, track_body = check(
            f"/typhoons/{EXPECTED_STORM_ID}/track", "application/json"
        )
        all_ok &= track_ok
        if track_ok:
            track = json.loads(track_body)
            workflow_ok = (
                track.get("storm_id") == EXPECTED_STORM_ID
                and len(track.get("observations", [])) >= 2
                and bool((track.get("forecast") or {}).get("points"))
            )
            print(
                "ACTIVE -> TRACK -> FORECAST: " f"{'PASS' if workflow_ok else 'FAIL'}"
            )
            all_ok &= workflow_ok

print(f"\nALL VERIFICATION CHECKS PASSED: {all_ok}")
raise SystemExit(0 if all_ok else 1)
