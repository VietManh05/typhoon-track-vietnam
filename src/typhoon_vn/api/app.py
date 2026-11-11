"""Forecast API and bilingual dashboard."""

import hmac
import logging
import mimetypes
import time
import uuid
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from pathlib import Path
from threading import RLock

from fastapi import Depends, FastAPI, HTTPException, Request, Security
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from typhoon_vn import __version__
from typhoon_vn.api.auth import LoginRequest, TokenResponse, issue_token, validate_token
from typhoon_vn.api.schemas import (
    DISCLAIMER,
    ErrorResponse,
    ForecastRequest,
    ForecastResponse,
    ObservationBatch,
    Subscription,
)
from typhoon_vn.features.geo import haversine_km
from typhoon_vn.inference.service import TyphoonForecaster
from typhoon_vn.logging_config import configure_logging
from typhoon_vn.operations.cache import ForecastCache
from typhoon_vn.operations.monitoring import MetricsRegistry
from typhoon_vn.operations.store import Store
from typhoon_vn.operations.worker import evaluate_alerts, update
from typhoon_vn.settings import Settings, get_settings
from typhoon_vn.weather.cache import WeatherCache
from typhoon_vn.weather.errors import (
    LocationNotFoundError,
    ProviderQuotaError,
    ProviderUnavailableError,
)
from typhoon_vn.weather.jma_live import JmaLiveError, active_typhoons, storm_track
from typhoon_vn.weather.nchmf import NchmfService
from typhoon_vn.weather.providers import AccuWeatherProvider, OpenMeteoProvider
from typhoon_vn.weather.service import WeatherService

logger = logging.getLogger(__name__)
mimetypes.add_type("application/geo+json", ".geojson")
mimetypes.add_type("font/woff2", ".woff2")


def _same_secret(supplied: str, expected: str) -> bool:
    # compare_digest raises TypeError on non-ASCII str; compare bytes instead.
    return hmac.compare_digest(supplied.encode("utf-8"), expected.encode("utf-8"))


def create_app(
    settings: Settings | None = None, store=None, forecaster=None, cache=None
) -> FastAPI:
    settings = get_settings() if settings is None else settings
    configure_logging(settings.log_level, json_logs=settings.log_json)
    services = {
        "store": store,
        "forecaster": forecaster,
        "redis": None,
        "cache": cache,
        "weather": None,
    }
    nchmf = NchmfService(timeout=settings.weather_request_timeout_seconds)
    lock = RLock()
    requests = defaultdict(deque)
    counters = {"requests": 0, "errors": 0, "forecast_cache_hits": 0}
    metrics_registry = MetricsRegistry()
    api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
    oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)

    def initialize():
        with lock:
            if services["store"] is None:
                services["store"] = Store(settings.operational_database_url)
            if services["forecaster"] is None:
                services["forecaster"] = TyphoonForecaster(
                    settings.model_artifact,
                    settings.allow_baseline,
                    cache_ttl_seconds=settings.forecast_cache_ttl_seconds,
                    cache_max_entries=settings.forecast_cache_max_entries,
                    # ALLOW_BASELINE=false must also forbid the silent fallback.
                    allow_environment_fallback=settings.allow_baseline,
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
            if services["cache"] is None:
                services["cache"] = ForecastCache(
                    services["redis"],
                    ttl_seconds=settings.forecast_cache_ttl_seconds,
                )
        provider = None
        if settings.weather_provider == "open-meteo":
            provider = OpenMeteoProvider(
                base_url=settings.open_meteo_base_url,
                timeout=settings.weather_request_timeout_seconds,
            )
        elif settings.accuweather_api_key:
            provider = AccuWeatherProvider(
                settings.accuweather_api_key,
                base_url=settings.accuweather_base_url,
                timeout=settings.weather_request_timeout_seconds,
            )
        if provider is not None:
            weather = WeatherService(
                provider,
                cache=WeatherCache(services["redis"]),
            )
            weather.TTLS = {
                "current": settings.weather_current_ttl_seconds,
                "hourly": settings.weather_hourly_ttl_seconds,
                "daily": settings.weather_daily_ttl_seconds,
                "alerts": settings.weather_alerts_ttl_seconds,
            }
            services["weather"] = weather
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
    app.state.metrics = metrics_registry

    protected_responses = {
        401: {"model": ErrorResponse, "description": "API key missing or invalid"},
        404: {"model": ErrorResponse, "description": "Storm not found"},
        422: {
            "model": ErrorResponse,
            "description": "Invalid request or forecast input",
        },
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        503: {"model": ErrorResponse, "description": "Dependency unavailable"},
    }

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-API-Key", "X-Request-ID"],
    )

    @app.middleware("http")
    async def accounting(request: Request, call_next):
        started = time.perf_counter()
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id
        counters["requests"] += 1
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception:
            counters["errors"] += 1
            elapsed_ms = (time.perf_counter() - started) * 1000
            metrics_registry.record_request(
                request.method, request.url.path, status_code, elapsed_ms
            )
            logger.exception(
                "request failed",
                extra={"request_id": request_id, "path": request.url.path},
            )
            raise
        elapsed_ms = (time.perf_counter() - started) * 1000
        if status_code >= 400:
            counters["errors"] += 1
        metrics_registry.record_request(
            request.method, request.url.path, status_code, elapsed_ms
        )
        log = logger.warning if elapsed_ms >= settings.slow_request_ms else logger.info
        log(
            "request completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "duration_ms": round(elapsed_ms, 2),
            },
        )
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["X-Frame-Options"] = "DENY"
        return response

    @app.exception_handler(Exception)
    async def unexpected_error(request: Request, exc: Exception):
        logger.exception(
            "unhandled request error",
            extra={"request_id": getattr(request.state, "request_id", "unknown")},
        )
        return JSONResponse(
            status_code=500,
            headers={"X-Request-ID": getattr(request.state, "request_id", "unknown")},
            content={
                "error": {
                    "status": 500,
                    "code": "internal_error",
                    "message": "Internal server error",
                },
                "request_id": getattr(request.state, "request_id", "unknown"),
            },
        )

    @app.exception_handler(TimeoutError)
    async def dependency_timeout(request: Request, exc: TimeoutError):
        logger.warning(
            "dependency timeout",
            extra={"request_id": getattr(request.state, "request_id", "unknown")},
        )
        return JSONResponse(
            status_code=503,
            content={
                "error": {
                    "status": 503,
                    "code": "unavailable",
                    "message": "Services unavailable",
                },
                "request_id": getattr(request.state, "request_id", "unknown"),
            },
        )

    # Starlette's base class also covers routing 404/405 and static files.
    @app.exception_handler(StarletteHTTPException)
    async def http_error(request: Request, exc: StarletteHTTPException):
        code = {
            401: "unauthorized",
            404: "not_found",
            405: "method_not_allowed",
            422: "invalid_request",
            429: "rate_limited",
            503: "unavailable",
        }.get(exc.status_code, "http_error")
        return JSONResponse(
            status_code=exc.status_code,
            headers=getattr(exc, "headers", None),
            content=jsonable_encoder(
                {
                    "error": {
                        "status": exc.status_code,
                        "code": code,
                        "message": str(exc.detail),
                    },
                    "request_id": getattr(request.state, "request_id", "unknown"),
                }
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(
                {
                    "error": {
                        "status": 422,
                        "code": "validation_error",
                        "message": "Request validation failed",
                    },
                    "request_id": getattr(request.state, "request_id", "unknown"),
                    "issues": exc.errors(),
                }
            ),
        )

    def rate_limit(request: Request) -> None:
        now = time.monotonic()
        address = request.client.host if request.client else "local"
        with lock:
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

    def authorize(
        request: Request,
        supplied_key: str | None = Security(api_key_header),
        bearer_token: str | None = Security(oauth2_bearer),
    ) -> None:
        configured = bool(
            settings.require_api_key
            or settings.api_key
            or settings.jwt_secret
            or settings.oauth_username
            or settings.oauth_password
        )
        if not configured:
            rate_limit(request)
            return
        api_key_valid = bool(
            settings.api_key
            and supplied_key
            and _same_secret(supplied_key, settings.api_key)
        )
        jwt_valid = False
        if bearer_token and settings.jwt_secret:
            try:
                validate_token(
                    bearer_token,
                    settings.jwt_secret,
                    settings.jwt_issuer,
                    settings.jwt_audience,
                )
                jwt_valid = True
            except ValueError:
                pass
        if not api_key_valid and not jwt_valid:
            raise HTTPException(
                401,
                "Valid bearer token or X-API-Key required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        rate_limit(request)

    def authorize_storm_read(
        request: Request,
        source: str | None = None,
        supplied_key: str | None = Security(api_key_header),
        bearer_token: str | None = Security(oauth2_bearer),
    ) -> None:
        if source == "jma":
            rate_limit(request)
            return
        authorize(request, supplied_key, bearer_token)

    @app.post(
        "/token",
        response_model=TokenResponse,
        tags=["authentication"],
        responses={401: protected_responses[401], 429: protected_responses[429]},
    )
    def token(body: LoginRequest, request: Request) -> TokenResponse:
        rate_limit(request)
        valid = bool(
            settings.jwt_secret
            and settings.oauth_username
            and settings.oauth_password
            and _same_secret(body.username, settings.oauth_username)
            and _same_secret(body.password, settings.oauth_password)
        )
        if not valid:
            raise HTTPException(
                401,
                "Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return issue_token(
            body.username,
            settings.jwt_secret,
            settings.jwt_issuer,
            settings.jwt_audience,
            settings.jwt_expiry_seconds,
        )

    @app.get("/auth/capabilities", tags=["authentication"])
    def auth_capabilities():
        return {
            "available": bool(
                settings.api_key
                or (
                    settings.jwt_secret
                    and settings.oauth_username
                    and settings.oauth_password
                )
            )
        }

    @app.get("/auth/session", tags=["authentication"])
    def auth_session(request: Request, _: None = Depends(authorize)):
        if not (settings.api_key or settings.jwt_secret):
            raise HTTPException(503, "Authentication is not configured")
        return {"authenticated": True}

    def db():
        return initialize()["store"]

    @app.get("/health", tags=["system"])
    def health():
        return {"status": "ok", "environment": settings.app_env}

    @app.get(
        "/ready",
        tags=["system"],
        responses={503: protected_responses[503]},
    )
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
            "model_revision": service.cache_revision,
            "model_kind": service.kind,
            "dataset_version": service.dataset,
        }

    metrics_token = (
        settings.metrics_token_file.read_text(encoding="utf-8").strip()
        if settings.metrics_token_file
        else None
    )
    if metrics_token == "":
        raise ValueError("Monitoring token file must not be empty")

    def authorize_metrics(
        request: Request,
        supplied_key: str | None = Security(api_key_header),
        bearer_token: str | None = Security(oauth2_bearer),
    ) -> None:
        if metrics_token is None:
            authorize(request, supplied_key, bearer_token)
        elif not bearer_token or not _same_secret(bearer_token, metrics_token):
            raise HTTPException(401, "Monitoring credential required")

    @app.get(
        "/metrics",
        response_class=PlainTextResponse,
        dependencies=[Depends(authorize_metrics)],
    )
    def metrics():
        legacy_lines = [
            f"typhoon_{name}_total {value}" for name, value in counters.items()
        ]
        return metrics_registry.render(extra_lines=legacy_lines)

    def fresh_response(payload) -> ForecastResponse:
        from datetime import datetime, timedelta, timezone

        result = ForecastResponse.model_validate(payload)
        if result.issue_time < datetime.now(timezone.utc) - timedelta(hours=24):
            warning = "Observations are older than 24 hours"
            if warning not in result.warnings:
                result.warnings.append(warning)
        return result

    def compute(body: ForecastRequest) -> ForecastResponse:
        service = initialize()["forecaster"]
        if body.observations is None:
            track = db().track(body.storm_id)
            if not track:
                raise HTTPException(404, "Storm not found")
            body = body.model_copy(update={"observations": track[-512:]})
        key = service.key(body)
        operational_cache = services["cache"]
        redis_key = None
        if operational_cache is not None:
            redis_key = operational_cache.key(
                storm_id=body.storm_id,
                input_revision=body.model_dump(mode="json"),
                model_revision=getattr(service, "cache_revision", service.version),
            )
            redis_payload = operational_cache.get(redis_key)
            if redis_payload is not None:
                counters["forecast_cache_hits"] += 1
                return fresh_response(redis_payload)
        cached = db().cached(key)
        if cached:
            counters["forecast_cache_hits"] += 1
            return fresh_response(cached)
        try:
            result = service.forecast(body)
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        db().save_forecast(result)
        evaluate_alerts(db(), result.model_dump(mode="json"))
        if operational_cache is not None and redis_key is not None:
            operational_cache.put(redis_key, result.model_dump(mode="json"))
        return result

    @app.post(
        "/forecast",
        response_model=ForecastResponse,
        dependencies=[Depends(authorize)],
        responses=protected_responses,
    )
    def forecast(body: ForecastRequest) -> ForecastResponse:
        return compute(body)

    @app.get(
        "/typhoons/active",
        dependencies=[Depends(authorize_storm_read)],
        responses=protected_responses,
    )
    def active(source: str | None = None):
        if source == "jma":
            try:
                return active_typhoons()
            except JmaLiveError as exc:
                raise HTTPException(503, str(exc)) from exc
        if source not in (None, "stored"):
            raise HTTPException(422, "Unsupported storm source")
        operational_cache = services["cache"]
        cache_key = operational_cache.active_key() if operational_cache else None
        if operational_cache and cache_key:
            cached = operational_cache.get(cache_key)
            if cached is not None:
                return cached
        payload = {"typhoons": db().active(), "disclaimer": DISCLAIMER}
        if operational_cache and cache_key:
            operational_cache.put(cache_key, payload)
        return payload

    @app.get(
        "/typhoons/{storm_id}/track",
        dependencies=[Depends(authorize_storm_read)],
        responses=protected_responses,
    )
    def track(storm_id: str, source: str | None = None):
        if source == "jma":
            try:
                return storm_track(storm_id)
            except KeyError as exc:
                raise HTTPException(404, "Storm is not active") from exc
            except JmaLiveError as exc:
                raise HTTPException(503, str(exc)) from exc
        if source not in (None, "stored"):
            raise HTTPException(422, "Unsupported storm source")
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

    @app.get(
        "/typhoons/{storm_id}/impact",
        dependencies=[Depends(authorize)],
        responses=protected_responses,
    )
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
        ids = update(
            db(),
            initialize()["forecaster"],
            [body],
            cache=services["cache"],
        )
        return {"status": "stored", "forecast_ids": ids}

    @app.get("/subscriptions", tags=["alerts"])
    def subscription_capabilities():
        return {
            "available": False,
            "delivery": "draft-only",
            "error": {
                "message": "Dịch vụ chỉ lưu bản nháp; chưa gửi cảnh báo đến người nhận."
            },
        }

    @app.post("/subscriptions", status_code=201, dependencies=[Depends(authorize)])
    def subscribe(body: Subscription):
        return {"id": db().subscribe(body), "delivery": "draft-only"}

    @app.get("/alerts", dependencies=[Depends(authorize)])
    def alert_drafts():
        return {"alerts": db().alert_drafts(), "delivery": "draft-only"}

    def weather_service() -> WeatherService:
        service = services["weather"]
        if service is None:
            raise HTTPException(503, "Licensed weather provider is not configured")
        return service

    def weather_result(kind: str, location_id: str):
        try:
            return weather_service().get(kind, location_id)
        except (KeyError, LocationNotFoundError) as exc:
            raise HTTPException(404, "Weather location not found") from exc
        except ProviderQuotaError as exc:
            raise HTTPException(
                429, "Weather provider quota exceeded", headers={"Retry-After": "3600"}
            ) from exc
        except ProviderUnavailableError as exc:
            raise HTTPException(503, "Weather provider unavailable") from exc

    @app.get(
        "/api/weather/nchmf",
        tags=["weather"],
        dependencies=[Depends(rate_limit)],
    )
    def nchmf_weather():
        try:
            return nchmf.get()
        except ProviderUnavailableError as exc:
            raise HTTPException(
                503, "NCHMF unavailable or source format changed"
            ) from exc

    @app.get(
        "/api/weather/locations/search",
        tags=["weather"],
        dependencies=[Depends(rate_limit)],
    )
    def weather_locations(q: str = ""):
        return {
            "locations": [
                item.model_dump(mode="json", by_alias=True)
                for item in weather_service().search(q)
            ]
        }

    @app.get(
        "/api/weather/bundle", tags=["weather"], dependencies=[Depends(rate_limit)]
    )
    def weather_bundle(location_id: str = "da-nang"):
        return {
            "current": weather_result("current", location_id),
            "hourly": weather_result("hourly", location_id),
            "daily": weather_result("daily", location_id),
        }

    @app.post("/api/ai/chat", tags=["capabilities"])
    def ai_unavailable():
        raise HTTPException(
            503, "AI chat is available only on a configured Pages deployment"
        )

    @app.get(
        "/api/weather/current", tags=["weather"], dependencies=[Depends(rate_limit)]
    )
    def weather_current(location_id: str = "da-nang"):
        return weather_result("current", location_id)

    @app.get(
        "/api/weather/hourly", tags=["weather"], dependencies=[Depends(rate_limit)]
    )
    def weather_hourly(location_id: str = "da-nang"):
        return {"forecasts": weather_result("hourly", location_id)}

    @app.get("/api/weather/daily", tags=["weather"], dependencies=[Depends(rate_limit)])
    def weather_daily(location_id: str = "da-nang"):
        return {"forecasts": weather_result("daily", location_id)}

    @app.get(
        "/api/weather/alerts", tags=["weather"], dependencies=[Depends(rate_limit)]
    )
    def weather_alerts(location_id: str = "da-nang"):
        return {"alerts": weather_result("alerts", location_id)}

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

        fonts_dir = dashboard / "fonts"
        if fonts_dir.exists():
            app.mount("/fonts", StaticFiles(directory=fonts_dir), name="fonts")

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
