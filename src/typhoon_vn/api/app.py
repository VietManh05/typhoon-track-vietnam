"""Forecast API and bilingual dashboard."""

import hmac
import ipaddress
import logging
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from pathlib import Path
from threading import RLock
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
from fastapi import Path as PathParam
from fastapi import Request
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
from typhoon_vn.operations.monitoring import verify_forecasts
from typhoon_vn.operations.store import Store
from typhoon_vn.operations.worker import evaluate_alerts, update
from typhoon_vn.settings import Settings, get_settings

logger = logging.getLogger(__name__)

# Same rule as ForecastRequest.storm_id, enforced on the URL so bad IDs are a
# 422 up front instead of a validation error deep inside the handler (500).
StormId = PathParam(min_length=1, max_length=80, pattern=r"^[\w.-]+$")

# Dashboard needs: own assets, Leaflet/Windy scripts, map tiles and APIs over https.
CONTENT_SECURITY_POLICY = (
    "default-src 'self'; "
    "script-src 'self' https://api.windy.com https://*.windy.com https://unpkg.com; "
    "style-src 'self' 'unsafe-inline' https://unpkg.com https://*.windy.com; "
    "img-src 'self' data: blob: https:; "
    "font-src 'self' data:; "
    "connect-src 'self' https:; "
    "worker-src 'self' blob:; "
    "frame-ancestors 'none'; base-uri 'self'; form-action 'self'; object-src 'none'"
)


def create_app(
    settings: Settings | None = None, store=None, forecaster=None
) -> FastAPI:
    settings = get_settings() if settings is None else settings
    services = {"store": store, "forecaster": forecaster}
    lock = RLock()
    # Separate limiter state so unauthenticated public reads can never exhaust
    # the capacity used by key-holding operators and writers.
    # Edge-forwarded viewers get their own state so a viewer surge can never fill
    # the operator/writer limiter.
    limiters = {
        "auth": defaultdict(deque),
        "public": defaultdict(deque),
        "edge": defaultdict(deque),
    }
    counters = {
        "requests": 0,
        "errors": 0,
        "forecast_cache_hits": 0,
        "forecasts_issued": 0,
    }
    # Prometheus-style request latency histogram (seconds).
    buckets = (0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
    latency = {"counts": [0] * (len(buckets) + 1), "sum": 0.0}

    def initialize():
        with lock:
            if services["store"] is None:
                services["store"] = Store(settings.operational_database_url)
            if services["forecaster"] is None:
                services["forecaster"] = TyphoonForecaster(
                    settings.model_artifact,
                    settings.allow_baseline,
                    analog_artifact=settings.analog_artifact,
                )
        return services

    @asynccontextmanager
    async def lifespan(app):
        initialize()
        yield
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
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def accounting(request, call_next):
        counters["requests"] += 1
        request_id = uuid4().hex
        started = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - started
        with lock:
            latency["sum"] += elapsed
            index = next(
                (i for i, edge in enumerate(buckets) if elapsed <= edge), len(buckets)
            )
            latency["counts"][index] += 1
        if response.status_code >= 400:
            counters["errors"] += 1
        # One structured line per request; no query strings or headers (no secrets).
        logger.info(
            "request id=%s method=%s path=%s status=%s ms=%.1f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            elapsed * 1000,
        )
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = CONTENT_SECURITY_POLICY
        return response

    def authorize(request: Request):
        if settings.api_key and not hmac.compare_digest(
            request.headers.get("X-API-Key", ""), settings.api_key
        ):
            raise HTTPException(401, "Valid X-API-Key required")
        # The edge proxies every viewer from a few Cloudflare IPs; trust its
        # forwarded viewer address only once the key has been verified.
        viewer = viewer_address(request) if settings.api_key else None
        if viewer:
            rate_limit(request, limiters["edge"], viewer)
        else:
            rate_limit(request, limiters["auth"])

    def viewer_address(request: Request) -> str | None:
        """Valid X-Client-IP; IPv6 grouped by /64 so one host cannot fan out."""
        try:
            ip = ipaddress.ip_address(request.headers.get("X-Client-IP", "").strip())
        except ValueError:
            return None
        if ip.version == 6:
            return str(ipaddress.ip_network(f"{ip}/64", strict=False))
        return str(ip)

    def authorize_read(request: Request):
        """Dashboard read routes: public when ``public_read``, always rate limited."""
        if settings.public_read and "X-API-Key" not in request.headers:
            rate_limit(request, limiters["public"])
        else:
            authorize(request)

    def rate_limit(
        request: Request, requests: defaultdict, address: str | None = None
    ) -> None:
        now = time.monotonic()
        address = address or (request.client.host if request.client else "local")
        with lock:
            # Bound cardinality and expire inactive clients (only when large,
            # so a normal request does not scan every client).
            if len(requests) > 1000:
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
            "model_revision": service.revision,
            "model_kind": service.kind,
            "dataset_version": service.dataset,
        }

    @app.get(
        "/metrics", response_class=PlainTextResponse, dependencies=[Depends(authorize)]
    )
    def metrics():
        lines = []
        for name, value in counters.items():
            lines.append(f"# TYPE typhoon_{name}_total counter")
            lines.append(f"typhoon_{name}_total {value}")
        lines.append("# TYPE typhoon_http_request_duration_seconds histogram")
        with lock:
            cumulative = 0
            for edge, count in zip((*buckets, "+Inf"), latency["counts"]):
                cumulative += count
                lines.append(
                    f'typhoon_http_request_duration_seconds_bucket{{le="{edge}"}} '
                    f"{cumulative}"
                )
            lines.append(
                f"typhoon_http_request_duration_seconds_sum {latency['sum']:.6f}"
            )
            lines.append(f"typhoon_http_request_duration_seconds_count {cumulative}")
        # Live skill: issued forecasts verified against later observations.
        report = verify_forecasts(db())
        for gauge, key in (
            ("forecast_verified", "n"),
            ("forecast_error_km_mean", "mean_error_km"),
            ("forecast_cone_coverage", "cone_coverage"),
        ):
            lines.append(f"# TYPE typhoon_{gauge} gauge")
            for row in report["horizons"]:
                if row[key] is not None:
                    lines.append(
                        f'typhoon_{gauge}{{horizon_h="{row["horizon_h"]}"}} {row[key]}'
                    )
        return "\n".join(lines) + "\n"

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
        counters["forecasts_issued"] += 1
        db().save_forecast(result)
        evaluate_alerts(db(), result.model_dump(mode="json"))
        return result

    @app.post(
        "/forecast", response_model=ForecastResponse, dependencies=[Depends(authorize)]
    )
    def forecast(body: ForecastRequest):
        return compute(body)

    @app.get("/typhoons/active", dependencies=[Depends(authorize_read)])
    def active():
        return {"typhoons": db().active(), "disclaimer": DISCLAIMER}

    @app.get("/typhoons/near", dependencies=[Depends(authorize_read)])
    def near(lat: float, lon: float, radius_km: float = 500.0):
        """Active storms whose latest fix is within ``radius_km`` of a point."""

        if not -90 <= lat <= 90 or not -180 <= lon <= 180:
            raise HTTPException(422, "Invalid location coordinates")
        if not 0 < radius_km <= 2000:
            raise HTTPException(422, "radius_km must be in (0, 2000]")
        store = db()
        return {
            "location": {"lat": lat, "lon": lon},
            "radius_km": radius_km,
            "spatial_backend": store.spatial_backend,
            "typhoons": store.storms_near(lat, lon, radius_km),
            "disclaimer": DISCLAIMER,
        }

    @app.get("/typhoons/{storm_id}/track", dependencies=[Depends(authorize_read)])
    def track(storm_id: str = StormId):
        fixes = db().track(storm_id)
        if not fixes:
            raise HTTPException(404, "Storm not found")
        forecast, reason = None, None
        if len(fixes) > 1:
            try:
                forecast = compute(ForecastRequest(storm_id=storm_id))
            except HTTPException as exc:
                # Observations are still worth showing when no forecast is possible.
                reason = exc.detail
        return {
            "storm_id": storm_id,
            "observations": fixes,
            "forecast": forecast,
            "forecast_unavailable": reason,
        }

    @app.get("/typhoons/{storm_id}/impact", dependencies=[Depends(authorize)])
    def impact(lat: float, lon: float, storm_id: str = StormId):
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
