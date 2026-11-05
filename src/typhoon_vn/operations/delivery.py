"""Webhook delivery of alert drafts — disabled unless explicitly configured.

Each pending draft is POSTed once as JSON to ``ALERT_WEBHOOK_URL`` with an
``X-Typhoon-Signature: sha256=<HMAC(secret, body)>`` header and the alert id in
``X-Typhoon-Alert-Id`` so receivers can verify origin and de-duplicate. A 2xx
response marks the draft ``delivered``; failures are retried on later runs up
to ``max_attempts``, then the draft is marked ``failed``. Only HTTPS URLs (or
plain HTTP to localhost for testing) are accepted.

Delivery is outward-facing: turn it on only after business approval, and keep
the message text pointing to NCHMF as the official source.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlsplit

LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Refuse redirects: a receiver must not bounce signed alerts elsewhere
    (scheme downgrade or internal targets). A 3xx counts as a failed attempt."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


@dataclass(frozen=True)
class DeliveryConfig:
    enabled: bool = False
    url: str = ""
    secret: str = ""
    max_attempts: int = 5
    timeout_s: float = 10.0

    def __post_init__(self) -> None:
        if not self.enabled:
            return
        parts = urlsplit(self.url)
        local = parts.hostname in LOCAL_HOSTS
        if parts.scheme != "https" and not (parts.scheme == "http" and local):
            raise ValueError("alert webhook must use https (http only for localhost)")
        if parts.username or parts.password or not parts.hostname:
            raise ValueError("alert webhook URL must not embed credentials")
        if len(self.secret) < 6:
            raise ValueError("alert webhook secret is required")
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be positive")


def _post(config: DeliveryConfig, alert: dict) -> bool:
    body = json.dumps(alert, sort_keys=True).encode()
    signature = hmac.new(config.secret.encode(), body, hashlib.sha256).hexdigest()
    request = urllib.request.Request(
        config.url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Typhoon-Signature": f"sha256={signature}",
            "X-Typhoon-Alert-Id": alert["id"],
        },
    )
    try:
        with _OPENER.open(request, timeout=config.timeout_s) as response:
            return 200 <= response.status < 300
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def deliver_pending(store, config: DeliveryConfig) -> dict[str, int]:
    pending = store.pending_alerts()
    if not config.enabled:
        return {"delivered": 0, "failed": 0, "skipped": len(pending)}
    delivered = failed = 0
    for alert in pending:
        ok = _post(config, alert)
        attempts = int(alert.get("delivery_attempts", 0)) + 1
        update = {
            "delivery_attempts": attempts,
            "last_attempt_at": datetime.now(timezone.utc).isoformat(),
        }
        if ok:
            update["status"] = "delivered"
            delivered += 1
        elif attempts >= config.max_attempts:
            update["status"] = "failed"
            failed += 1
        store.update_alert(alert["id"], update)
    return {"delivered": delivered, "failed": failed, "skipped": 0}
