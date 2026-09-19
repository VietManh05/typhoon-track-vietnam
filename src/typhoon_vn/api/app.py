"""Forecast API and bilingual dashboard."""

import hmac
import logging
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from pathlib import Path
from threading import RLock

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from typhoon_vn import __version__
from typhoon_vn.api.schemas import (
    DISCLAIMER,
    ForecastRequest,
    ForecastResponse,
    ObservationBatch,
    Subscription,
)
from typhoon_vn.features.geo import haversine_km
from typhoon_vn.inference.service import TyphoonForecaster
from typhoon_vn.operations.store import Store
from typhoon_vn.operations.worker import evaluate_alerts, update
from typhoon_vn.settings import Settings, get_settings

logger = logging.getLogger(__name__)


def create_app(
    settings: Settings | None = None, store=None, forecaster=None
) -> FastAPI:
    settings = get_settings() if settings is None else settings
    services = {"store": store, "forecaster": forecaster, "redis": None}
    lock = RLock()
    requests = defaultdict(deque)
    counters = {"requests": 0, "errors": 0, "forecast_cache_hits": 0}

    def initialize():
        with lock:
            if services["store"] is None:
                services["store"] = Store(settings.operational_database_url)
            if services["forecaster"] is None:
                services["forecaster"] = TyphoonForecaster(
                    settings.model_artifact, settings.allow_baseline
                )
        return services

    @asynccontextmanager
    async def lifespan(app):
        initialize()
        if settings.cache_enabled:
            import redis

            services["redis"] = redis.Redis.from_url(
                settings.redis_url, socket_connect_timeout=1, socket_timeout=1
            )
        yield
        if services["redis"]:
            services["redis"].close()
        if store is None and services["store"]:
            services["store"].engine.dispose()

    app = FastAPI(
        title="Typhoon VN Forecast System",
        version=__version__,
        description=DISCLAIMER,
        lifespan=lifespan,
    )
    app.state.services = services

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def accounting(request, call_next):
        counters["requests"] += 1
        response = await call_next(request)
        if response.status_code >= 400:
            counters["errors"] += 1
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["X-Frame-Options"] = "DENY"
        return response

    def authorize(request: Request):
        if settings.api_key and not hmac.compare_digest(
            request.headers.get("X-API-Key", ""), settings.api_key
        ):
            raise HTTPException(401, "Valid X-API-Key required")
        now = time.monotonic()
        address = request.client.host if request.client else "local"
        with lock:
            # Bound cardinality and expire inactive clients.
            for key in list(requests):
                if not requests[key] or requests[key][-1] <= now - 60:
                    del requests[key]
            if address not in requests and len(requests) >= 10000:
                raise HTTPException(429, "Rate limiter at capacity")
            window = requests[address]
            while window and window[0] <= now - 60:
                window.popleft()
            if len(window) >= settings.requests_per_minute:
                raise HTTPException(
                    429, "Rate limit exceeded", headers={"Retry-After": "60"}
                )
            window.append(now)

    def db():
        return initialize()["store"]

    @app.get("/health", tags=["system"])
    def health():
        return {"status": "ok", "environment": settings.app_env}

    @app.get("/ready", tags=["system"])
    def ready():
        from sqlalchemy import text

        try:
            with db().engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return {
                "status": "ready",
                "model_version": initialize()["forecaster"].version,
            }
        except Exception:
            logger.exception("Readiness failed")
            raise HTTPException(503, "Services unavailable")

    @app.get("/version", tags=["system"])
    def version():
        service = initialize()["forecaster"]
        return {
            "version": __version__,
            "model_version": service.version,
            "model_kind": service.kind,
            "dataset_version": service.dataset,
        }

    @app.get(
        "/metrics", response_class=PlainTextResponse, dependencies=[Depends(authorize)]
    )
    def metrics():
        return (
            "\n".join(
                f"typhoon_{name}_total {value}" for name, value in counters.items()
            )
            + "\n"
        )

    def compute(body):
        service = initialize()["forecaster"]
        if body.observations is None:
            track = db().track(body.storm_id)
            if not track:
                raise HTTPException(404, "Storm not found")
            body = body.model_copy(update={"observations": track[-512:]})
        key = service.key(body)
        cached = db().cached(key)
        if cached:
            counters["forecast_cache_hits"] += 1
            # Refresh time-sensitive warning rather than serving an old freshness claim.
            from datetime import datetime, timedelta, timezone

            result = ForecastResponse.model_validate(cached)
            if result.issue_time < datetime.now(timezone.utc) - timedelta(hours=24):
                warning = "Observations are older than 24 hours"
                if warning not in result.warnings:
                    result.warnings.append(warning)
            return result
        try:
            result = service.forecast(body)
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        db().save_forecast(result)
        evaluate_alerts(db(), result.model_dump(mode="json"))
        if services["redis"]:
            try:
                services["redis"].setex(
                    "forecast:" + key, 1800, result.model_dump_json()
                )
            except Exception:
                logger.warning(
                    "Redis unavailable; durable database cache remains active"
                )
        return result

    @app.post(
        "/forecast", response_model=ForecastResponse, dependencies=[Depends(authorize)]
    )
    def forecast(body: ForecastRequest):
        return compute(body)

    @app.get("/typhoons/active", dependencies=[Depends(authorize)])
    def active():
        return {"typhoons": db().active(), "disclaimer": DISCLAIMER}

    @app.get("/typhoons/{storm_id}/track", dependencies=[Depends(authorize)])
    def track(storm_id: str):
        fixes = db().track(storm_id)
        if not fixes:
            raise HTTPException(404, "Storm not found")
        return {
            "storm_id": storm_id,
            "observations": fixes,
            "forecast": (
                compute(ForecastRequest(storm_id=storm_id)) if len(fixes) > 1 else None
            ),
        }

    @app.get("/typhoons/{storm_id}/impact", dependencies=[Depends(authorize)])
    def impact(storm_id: str, lat: float, lon: float):
        if not -90 <= lat <= 90 or not -180 <= lon <= 180:
            raise HTTPException(422, "Invalid location coordinates")
        result = compute(ForecastRequest(storm_id=storm_id))
        points = [
            {
                "horizon_hours": p.horizon_hours,
                "distance_km": haversine_km(lat, lon, p.lat, p.lon),
                "within_illustrative_radius": haversine_km(lat, lon, p.lat, p.lon)
                <= p.radius_km,
            }
            for p in result.points
        ]
        return {
            "storm_id": storm_id,
            "location": {"lat": lat, "lon": lon},
            "points": points,
            "disclaimer": DISCLAIMER,
            "limitation": "Point proximity only; not wind, flood, landfall or province impact.",
        }

    @app.post("/observations", dependencies=[Depends(authorize)])
    def observations(body: ObservationBatch):
        ids = update(db(), initialize()["forecaster"], [body])
        return {"status": "stored", "forecast_ids": ids}

    @app.post("/subscriptions", status_code=201, dependencies=[Depends(authorize)])
    def subscribe(body: Subscription):
        return {"id": db().subscribe(body), "delivery": "draft-only"}

    @app.get("/alerts", dependencies=[Depends(authorize)])
    def alert_drafts():
        return {"alerts": db().alert_drafts(), "delivery": "draft-only"}

    dashboard = Path(__file__).resolve().parents[1] / "dashboard"
    if dashboard.exists():
        assets_dir = dashboard / "assets"
        if assets_dir.exists():
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
        else:
            app.mount("/assets", StaticFiles(directory=dashboard), name="assets")

        data_dir = dashboard / "data"
        if data_dir.exists():
            app.mount("/data", StaticFiles(directory=data_dir), name="data")

        @app.get("/favicon.svg", include_in_schema=False)
        def favicon():
            fav = dashboard / "favicon.svg"
            if fav.exists():
                return FileResponse(fav)
            raise HTTPException(404)

        @app.get("/", include_in_schema=False)
        def home():
            return FileResponse(dashboard / "index.html")

    return app


app = create_app()
