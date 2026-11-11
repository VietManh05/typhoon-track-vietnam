"""Authentication and public endpoint rate-limit integration tests."""

from fastapi.testclient import TestClient

from typhoon_vn.api.app import create_app
from typhoon_vn.inference.service import TyphoonForecaster
from typhoon_vn.operations.store import Store
from typhoon_vn.settings import Settings


def secured_app(**overrides):
    values = {
        "_env_file": None,
        "cache_enabled": False,
        "operational_database_url": "sqlite:///:memory:",
        "jwt_secret": "a-secure-test-secret-that-is-long-enough",
        "oauth_username": "operator",
        "oauth_password": "correct-horse-battery-staple",
    }
    values.update(overrides)
    return create_app(
        settings=Settings(**values),
        store=Store("sqlite:///:memory:"),
        forecaster=TyphoonForecaster(),
    )


def test_oauth_token_grants_access_to_protected_endpoint() -> None:
    with TestClient(secured_app()) as client:
        denied = client.get("/typhoons/active")
        token = client.post(
            "/token",
            json={
                "username": "operator",
                "password": "correct-horse-battery-staple",
            },
        )
        allowed = client.get(
            "/typhoons/active",
            headers={"Authorization": f"Bearer {token.json()['access_token']}"},
        )
    assert denied.status_code == 401
    assert token.status_code == 200
    assert token.json()["token_type"] == "bearer"
    assert allowed.status_code == 200


def test_invalid_credentials_and_tampered_token_are_rejected() -> None:
    with TestClient(secured_app()) as client:
        invalid = client.post(
            "/token", json={"username": "operator", "password": "wrong"}
        )
        token = client.post(
            "/token",
            json={
                "username": "operator",
                "password": "correct-horse-battery-staple",
            },
        ).json()["access_token"]
        tampered = client.get(
            "/typhoons/active",
            headers={"Authorization": f"Bearer {token[:-1]}x"},
        )
    assert invalid.status_code == 401
    assert tampered.status_code == 401
    assert tampered.json()["error"]["code"] == "unauthorized"


def test_public_weather_endpoint_is_rate_limited() -> None:
    with TestClient(
        secured_app(
            requests_per_minute=1,
            jwt_secret="",
            oauth_username="",
            oauth_password="",
            weather_provider="accuweather",
        )
    ) as client:
        first = client.get("/api/weather/current")
        second = client.get("/api/weather/current")
    assert first.status_code == 503
    assert second.status_code == 429


def test_cors_allows_only_configured_origin() -> None:
    with TestClient(
        secured_app(cors_origins=["https://baoviet2026.pages.dev"])
    ) as client:
        allowed = client.get(
            "/health", headers={"Origin": "https://baoviet2026.pages.dev"}
        )
        denied = client.get("/health", headers={"Origin": "https://untrusted.example"})
    assert allowed.headers.get("access-control-allow-origin") == (
        "https://baoviet2026.pages.dev"
    )
    assert denied.headers.get("access-control-allow-origin") is None


def test_auth_session_requires_verified_credentials() -> None:
    with TestClient(secured_app(api_key="accepted-key")) as client:
        assert client.get("/auth/capabilities").json() == {"available": True}
        assert (
            client.get("/auth/session", headers={"X-API-Key": "wrong"}).status_code
            == 401
        )
        assert client.get(
            "/auth/session", headers={"X-API-Key": "accepted-key"}
        ).json() == {"authenticated": True}


def test_authentication_is_not_advertised_without_credentials() -> None:
    with TestClient(
        secured_app(api_key="", jwt_secret="", oauth_username="", oauth_password="")
    ) as client:
        assert client.get("/auth/capabilities").json() == {"available": False}
        assert client.get("/auth/session").status_code == 503


def test_non_ascii_credentials_are_rejected_not_crashed() -> None:
    with TestClient(secured_app(), raise_server_exceptions=False) as client:
        login = client.post("/token", json={"username": "quản-trị", "password": "sai"})
        assert login.status_code == 401
        keyed = client.get("/typhoons/active", headers={"X-API-Key": "clé".encode()})
        assert keyed.status_code == 401
    with TestClient(secured_app(oauth_password="mật-khẩu")) as client:
        login = client.post(
            "/token", json={"username": "operator", "password": "mật-khẩu"}
        )
        assert login.status_code == 200


def test_unknown_route_uses_error_envelope() -> None:
    with TestClient(secured_app()) as client:
        body = client.get("/no-such-route").json()
    assert body["error"]["code"] == "not_found" and body["request_id"]
