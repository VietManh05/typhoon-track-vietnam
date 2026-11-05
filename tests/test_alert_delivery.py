"""A29-020: signed, idempotent webhook delivery of alert drafts (off by default)."""

import hashlib
import hmac
import json
import threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from typhoon_vn.api.schemas import Fix, ObservationBatch, Subscription
from typhoon_vn.inference.service import TyphoonForecaster
from typhoon_vn.operations.delivery import DeliveryConfig, deliver_pending
from typhoon_vn.operations.store import Store
from typhoon_vn.operations.worker import update


class _Receiver(BaseHTTPRequestHandler):
    status = 200
    received: list = []

    def do_POST(self):  # noqa: N802 (http.server API)
        body = self.rfile.read(int(self.headers["Content-Length"]))
        type(self).received.append((dict(self.headers), body))
        self.send_response(type(self).status)
        self.end_headers()

    def log_message(self, *args):
        pass


@pytest.fixture()
def receiver():
    _Receiver.received = []
    _Receiver.status = 200
    server = HTTPServer(("127.0.0.1", 0), _Receiver)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}/hook"
    server.shutdown()


@pytest.fixture()
def store_with_alert(tmp_path):
    store = Store(f"sqlite:///{tmp_path / 'a.db'}")
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    fixes = [
        Fix(
            timestamp=now - timedelta(hours=6 * (5 - i)),
            lat=16.0,
            lon=110.0 - 0.4 * i,
            wind_ms=30,
            intensity="TY",
            source="test",
        )
        for i in range(6)
    ]
    store.subscribe(Subscription(label="Da Nang", lat=16.05, lon=108.2, radius_km=300))
    update(
        store,
        TyphoonForecaster(),
        [ObservationBatch(storm_id="S", name="S", observations=fixes)],
    )
    assert len(store.alert_drafts()) == 1
    return store


def _config(url, **overrides):
    values = {"enabled": True, "url": url, "secret": "s3cret", "max_attempts": 2}
    values.update(overrides)
    return DeliveryConfig(**values)


def test_delivery_is_signed_and_idempotent(store_with_alert, receiver) -> None:
    result = deliver_pending(store_with_alert, _config(receiver))
    assert result == {"delivered": 1, "failed": 0, "skipped": 0}
    headers, body = _Receiver.received[0]
    expected = hmac.new(b"s3cret", body, hashlib.sha256).hexdigest()
    assert headers["X-Typhoon-Signature"] == f"sha256={expected}"
    payload = json.loads(body)
    assert payload["status"] == "draft" and "NCHMF" in payload["disclaimer"]
    assert store_with_alert.alert_drafts()[0]["status"] == "delivered"
    # Second run sends nothing.
    assert deliver_pending(store_with_alert, _config(receiver))["delivered"] == 0
    assert len(_Receiver.received) == 1


def test_failures_retry_then_stop(store_with_alert, receiver) -> None:
    _Receiver.status = 500
    deliver_pending(store_with_alert, _config(receiver))
    alert = store_with_alert.alert_drafts()[0]
    assert alert["status"] == "draft" and alert["delivery_attempts"] == 1
    deliver_pending(store_with_alert, _config(receiver))
    assert store_with_alert.alert_drafts()[0]["status"] == "failed"
    deliver_pending(store_with_alert, _config(receiver))
    assert len(_Receiver.received) == 2  # no third attempt after max_attempts


def test_disabled_by_default_and_url_is_restricted(store_with_alert, receiver) -> None:
    assert deliver_pending(store_with_alert, DeliveryConfig())["skipped"] == 1
    assert _Receiver.received == []
    for bad in (
        "http://example.com/hook",
        "ftp://127.0.0.1/x",
        "https://user:pw@x.org/",
    ):
        with pytest.raises(ValueError):
            _config(bad)
