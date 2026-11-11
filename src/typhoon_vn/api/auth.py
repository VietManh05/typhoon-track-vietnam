"""Minimal OAuth2 password flow and strictly validated HMAC JWT tokens."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Credentials accepted by the token endpoint."""

    username: str = Field(min_length=1, max_length=128)
    password: str = Field(min_length=1, max_length=1024)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


@dataclass(frozen=True)
class TokenClaims:
    subject: str
    expires_at: int


def _b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _b64decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def issue_token(
    subject: str,
    secret: str,
    issuer: str,
    audience: str,
    expires_seconds: int,
    *,
    now: int | None = None,
) -> TokenResponse:
    """Issue an HS256 token without leaking credentials into claims."""
    issued_at = int(time.time()) if now is None else now
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": subject,
        "iss": issuer,
        "aud": audience,
        "iat": issued_at,
        "nbf": issued_at,
        "exp": issued_at + expires_seconds,
    }
    signing_input = ".".join(
        _b64encode(json.dumps(part, separators=(",", ":")).encode("utf-8"))
        for part in (header, payload)
    )
    signature = hmac.new(
        secret.encode("utf-8"), signing_input.encode("ascii"), hashlib.sha256
    ).digest()
    return TokenResponse(
        access_token=f"{signing_input}.{_b64encode(signature)}",
        expires_in=expires_seconds,
    )


def validate_token(
    token: str,
    secret: str,
    issuer: str,
    audience: str,
    *,
    now: int | None = None,
) -> TokenClaims:
    """Validate structure, algorithm, signature and registered JWT claims."""
    if not secret:
        raise ValueError("JWT authentication is not configured")
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
        header: dict[str, Any] = json.loads(_b64decode(encoded_header))
        payload: dict[str, Any] = json.loads(_b64decode(encoded_payload))
        supplied_signature = _b64decode(encoded_signature)
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("Malformed bearer token") from exc
    if header != {"alg": "HS256", "typ": "JWT"}:
        raise ValueError("Unsupported bearer token header")
    signing_input = f"{encoded_header}.{encoded_payload}"
    expected = hmac.new(
        secret.encode("utf-8"), signing_input.encode("ascii"), hashlib.sha256
    ).digest()
    if not hmac.compare_digest(supplied_signature, expected):
        raise ValueError("Invalid bearer token signature")
    current = int(time.time()) if now is None else now
    try:
        subject = payload["sub"]
        issued_at = int(payload["iat"])
        not_before = int(payload["nbf"])
        expires_at = int(payload["exp"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Bearer token is missing required claims") from exc
    if not isinstance(subject, str) or not subject or payload.get("iss") != issuer:
        raise ValueError("Invalid bearer token claims")
    token_audience = payload.get("aud")
    audiences = token_audience if isinstance(token_audience, list) else [token_audience]
    if audience not in audiences:
        raise ValueError("Invalid bearer token audience")
    if issued_at > current + 30 or not_before > current + 30 or expires_at <= current:
        raise ValueError("Bearer token is not currently valid")
    return TokenClaims(subject=subject, expires_at=expires_at)
