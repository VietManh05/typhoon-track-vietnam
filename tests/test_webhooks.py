from datetime import datetime, timedelta, timezone

import pytest

from typhoon_vn.api.webhooks import sign, validate_destination, verify


def test_signature_and_replay_window():
    now = datetime(2026, 9, 20, tzinfo=timezone.utc)
    payload = {
        "version": "1",
        "delivery_id": "d1",
        "timestamp": now.isoformat(),
        "event": "alert.draft",
    }
    signature = sign(payload, "secret")
    verify(payload, "secret", signature, now=now)
    with pytest.raises(ValueError, match="signature"):
        verify(payload, "wrong", signature, now=now)
    with pytest.raises(ValueError, match="replay"):
        verify(payload, "secret", signature, now=now + timedelta(minutes=6))


def test_destination_blocks_ssrf_and_accepts_public_resolution():
    def private(*args):
        return [(None, None, None, None, ("127.0.0.1", 80))]

    def public(*args):
        return [(None, None, None, None, ("93.184.216.34", 443))]

    for url in ("file:///tmp/x", "http://localhost/hook", "http://127.0.0.1/hook"):
        with pytest.raises(ValueError):
            validate_destination(url, resolver=private)
    assert validate_destination("https://example.com/hook", resolver=public).startswith(
        "https://"
    )
