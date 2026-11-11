"""Versioned signed webhook helpers with replay and SSRF protection."""

import hashlib
import hmac
import ipaddress
import json
import socket
from datetime import datetime, timezone
from urllib.parse import urlparse


def canonical_payload(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def sign(payload: dict, secret: str) -> str:
    return hmac.new(
        secret.encode(), canonical_payload(payload), hashlib.sha256
    ).hexdigest()


def verify(
    payload: dict,
    secret: str,
    signature: str,
    *,
    now: datetime | None = None,
    window_seconds: int = 300,
) -> None:
    if payload.get("version") != "1" or not payload.get("delivery_id"):
        raise ValueError("unsupported payload or missing delivery_id")
    if not hmac.compare_digest(sign(payload, secret), signature):
        raise ValueError("invalid signature")
    timestamp = datetime.fromisoformat(str(payload["timestamp"]).replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    now = now or datetime.now(timezone.utc)
    if abs((now - timestamp.astimezone(timezone.utc)).total_seconds()) > window_seconds:
        raise ValueError("webhook timestamp outside replay window")


def validate_destination(url: str, *, resolver=socket.getaddrinfo) -> str:
    parsed = urlparse(url)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username
        or parsed.password
    ):
        raise ValueError("webhook URL must be public http(s) without user info")
    if parsed.hostname.lower() == "localhost":
        raise ValueError("local webhook destinations are forbidden")
    try:
        addresses = {
            item[4][0]
            for item in resolver(
                parsed.hostname,
                parsed.port or (443 if parsed.scheme == "https" else 80),
            )
        }
    except OSError as exc:
        raise ValueError("webhook host cannot be resolved") from exc
    if not addresses or any(
        not ipaddress.ip_address(value).is_global for value in addresses
    ):
        raise ValueError("webhook destination must resolve only to public addresses")
    return url
