"""Regression tests for API thread-pool dispatch and resource lifecycle."""

import asyncio
import inspect
import threading
import time
from types import SimpleNamespace
from unittest.mock import Mock

import httpx
from fastapi.testclient import TestClient

from typhoon_vn.api.app import create_app
from typhoon_vn.settings import Settings


class StoreStub:
    def __init__(self, active=None):
        self.active = active or (lambda: [])
        self.engine = SimpleNamespace(dispose=Mock())


def settings():
    return Settings(
        _env_file=None,
        cache_enabled=False,
        operational_database_url="sqlite:///:memory:",
        requests_per_minute=1000,
    )


def forecaster():
    return SimpleNamespace(version="test", kind="mock", dataset="test")


def test_successful_database_request_runs_in_worker_thread():
    caller_thread = threading.get_ident()
    seen_threads = []
    store = StoreStub(
        lambda: seen_threads.append(threading.get_ident()) or [{"id": "S"}]
    )
    app = create_app(settings(), store=store, forecaster=forecaster())

    route = next(
        route
        for route in app.routes
        if getattr(route, "path", None) == "/typhoons/active"
    )
    assert not inspect.iscoroutinefunction(route.endpoint)
    with TestClient(app) as client:
        response = client.get("/typhoons/active")

    assert response.status_code == 200
    assert response.json()["typhoons"] == [{"id": "S"}]
    assert seen_threads and seen_threads[0] != caller_thread


def test_database_timeout_and_unexpected_exception_are_sanitized():
    for error, expected_status, expected_message in [
        (TimeoutError("database host and secret"), 503, "Services unavailable"),
        (RuntimeError("internal secret"), 500, "Internal server error"),
    ]:

        def fail(error=error):
            raise error

        app = create_app(settings(), store=StoreStub(fail), forecaster=forecaster())
        with TestClient(app, raise_server_exceptions=False) as client:
            response = client.get("/typhoons/active")

        assert response.status_code == expected_status
        assert response.json()["error"]["message"] == expected_message
        assert "secret" not in response.text
        assert response.headers["X-Request-ID"]


def test_lifespan_cleans_up_only_resources_owned_by_app(monkeypatch):
    import typhoon_vn.api.app as app_module

    owned_store = StoreStub()
    redis_client = Mock()
    monkeypatch.setattr(app_module, "Store", Mock(return_value=owned_store))
    monkeypatch.setattr("redis.Redis.from_url", Mock(return_value=redis_client))
    configured = settings().model_copy(update={"cache_enabled": True})
    app = create_app(configured, forecaster=forecaster())

    with TestClient(app):
        pass

    redis_client.close.assert_called_once_with()
    owned_store.engine.dispose.assert_called_once_with()

    injected_store = StoreStub()
    app = create_app(settings(), store=injected_store, forecaster=forecaster())
    with TestClient(app):
        pass
    injected_store.engine.dispose.assert_not_called()


def test_concurrent_blocking_requests_do_not_block_event_loop():
    seen_threads = set()
    lock = threading.Lock()

    def slow_active():
        with lock:
            seen_threads.add(threading.get_ident())
        time.sleep(0.1)
        return []

    app = create_app(settings(), store=StoreStub(slow_active), forecaster=forecaster())

    async def exercise():
        loop_thread = threading.get_ident()
        ticks = 0
        done = False

        async def heartbeat():
            nonlocal ticks
            while not done:
                ticks += 1
                await asyncio.sleep(0.005)

        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://test"
        ) as client:
            beat = asyncio.create_task(heartbeat())
            started = time.perf_counter()
            responses = await asyncio.gather(
                *(client.get("/typhoons/active") for _ in range(8))
            )
            elapsed = time.perf_counter() - started
            done = True
            await beat
        return loop_thread, ticks, elapsed, responses

    loop_thread, ticks, elapsed, responses = asyncio.run(exercise())
    assert all(response.status_code == 200 for response in responses)
    assert ticks >= 5
    assert seen_threads and loop_thread not in seen_threads
    assert elapsed < 0.5
