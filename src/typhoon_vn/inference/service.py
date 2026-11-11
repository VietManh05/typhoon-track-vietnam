"""Thread-safe forecasting with provenance and bounded response caching."""

from __future__ import annotations

import hashlib
import json
import logging
import time
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import RLock
from typing import Any, Callable

from typhoon_vn.api.schemas import ForecastPoint, ForecastRequest, ForecastResponse
from typhoon_vn.features.geo import bearing_deg, destination_point, haversine_km

LOGGER = logging.getLogger(__name__)

Bundle = dict[str, Any]
BundleLoader = Callable[[str | Path], Bundle]
BundlePredictor = Callable[[Bundle, list[Any], list[int]], tuple[list[Any], list[Any]]]


def _default_bundle_loader(path: str | Path) -> Bundle:
    """Load a promoted bundle without coupling the service at import time."""

    from typhoon_vn.training.pipeline import load_bundle

    return load_bundle(path)


def _default_bundle_predictor(
    bundle: Bundle, fixes: list[Any], horizons: list[int]
) -> tuple[list[Any], list[Any]]:
    """Run the package bundle adapter behind an injectable boundary."""

    from typhoon_vn.training.pipeline import predict_bundle

    return predict_bundle(bundle, fixes, horizons)


def circle(lat: float, lon: float, radius: float) -> dict[str, object]:
    ring = []
    for angle in range(0, 361, 10):
        y, x = destination_point(lat, lon, angle, radius)
        ring.append([x, y])
    return {"type": "Polygon", "coordinates": [ring]}


class TyphoonForecaster:
    """Reusable forecaster with one model load and a bounded TTL LRU cache."""

    def __init__(
        self,
        artifact: Path | None = None,
        allow_baseline: bool = True,
        *,
        cache_ttl_seconds: int = 1800,
        cache_max_entries: int = 1024,
        allow_environment_fallback: bool = True,
        bundle_loader: BundleLoader | None = None,
        bundle_predictor: BundlePredictor | None = None,
    ) -> None:
        if cache_ttl_seconds < 1 or cache_max_entries < 1:
            raise ValueError("cache TTL and maximum entries must be positive")
        self.lock = RLock()
        self.bundle = None
        self.cache_ttl_seconds = cache_ttl_seconds
        self.cache_max_entries = cache_max_entries
        self.allow_environment_fallback = allow_environment_fallback
        self._cache: OrderedDict[str, tuple[float, ForecastResponse]] = OrderedDict()
        self.cache_hits = 0
        self.cache_misses = 0
        self._bundle_predictor = bundle_predictor or _default_bundle_predictor
        if artifact:
            loader = bundle_loader or _default_bundle_loader
            self.bundle = loader(artifact)
        elif not allow_baseline:
            raise ValueError("A promoted model artifact is required")
        self.version = (
            self.bundle["manifest"]["version"] if self.bundle else "persistence-v1"
        )
        self.kind = "trained-model" if self.bundle else "motion-baseline"
        self.dataset = (
            self.bundle["manifest"]["dataset_version"] if self.bundle else "none"
        )
        manifest = self.bundle["manifest"] if self.bundle else {}
        # A rebuilt bundle with the same display version must not reuse old results.
        self.cache_revision = (
            hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
            if self.bundle
            else self.version
        )
        self.feature_schema_version = str(
            manifest.get(
                "feature_schema_sha256",
                "unknown" if self.bundle else "baseline-motion-v1",
            )
        )
        self.scaler_version = str(
            manifest.get("files", {}).get(
                "scaler.json", "unknown" if self.bundle else "none"
            )
        )

    def key(self, request: ForecastRequest) -> str:
        body = request.model_dump_json() + self.cache_revision
        return hashlib.sha256(body.encode()).hexdigest()

    def clear_cache(self) -> None:
        with self.lock:
            self._cache.clear()

    def _cached(self, key: str, now: float) -> ForecastResponse | None:
        item = self._cache.get(key)
        if item is None:
            self.cache_misses += 1
            return None
        created, response = item
        if now - created >= self.cache_ttl_seconds:
            del self._cache[key]
            self.cache_misses += 1
            return None
        self._cache.move_to_end(key)
        self.cache_hits += 1
        return response.model_copy(deep=True)

    def _store(self, key: str, response: ForecastResponse, now: float) -> None:
        self._cache[key] = (now, response.model_copy(deep=True))
        self._cache.move_to_end(key)
        while len(self._cache) > self.cache_max_entries:
            self._cache.popitem(last=False)

    def forecast(self, request: ForecastRequest) -> ForecastResponse:
        key = self.key(request)
        now = time.monotonic()
        with self.lock:
            cached = self._cached(key, now)
            if cached is not None:
                LOGGER.debug("forecast cache hit", extra={"forecast_key": key})
                return cached
        # Compute outside the lock so distinct requests do not queue behind it.
        response = self._forecast_uncached(request, forecast_id=key)
        with self.lock:
            self._store(key, response, now)
        return response.model_copy(deep=True)

    def _forecast_uncached(
        self, request: ForecastRequest, *, forecast_id: str
    ) -> ForecastResponse:
        fixes = request.observations
        if not fixes or len(fixes) < 2:
            raise ValueError("At least two observations are required")
        first, last = fixes[-2:]
        delta = (last.timestamp - first.timestamp).total_seconds() / 3600
        if delta <= 0 or delta > 24:
            raise ValueError("Latest observation interval must be within 24 hours")
        speed = haversine_km(first.lat, first.lon, last.lat, last.lon) / delta
        if speed > 150:
            raise ValueError("Implausible storm motion exceeds 150 km/h")
        warnings = []
        fallback_used = False
        fallback_reason = None
        current_time = datetime.now(timezone.utc)
        if last.timestamp < current_time - timedelta(hours=24):
            warnings.append("Observations are older than 24 hours")
        if last.timestamp > current_time + timedelta(minutes=10):
            raise ValueError("Observation timestamp is in the future")
        required_environment = (
            self.bundle["manifest"].get("required_environmental_features", [])
            if self.bundle
            else []
        )
        missing_environment = bool(required_environment)
        if missing_environment and not self.allow_environment_fallback:
            raise ValueError("Required environmental features are unavailable")
        if self.bundle and not missing_environment:
            with self.lock:  # one shared torch module
                coords, classes = self._bundle_predictor(
                    self.bundle, fixes, request.horizons
                )
            radii = [
                self.bundle["manifest"]["validation_radius_km"][str(h)]
                for h in request.horizons
            ]
            uncertainty = self.bundle["manifest"].get(
                "uncertainty_method", "unspecified; not calibrated coverage"
            )
            warnings.append(
                "Experimental model; held-out validation is not operational certification"
            )
        else:
            if self.bundle and missing_environment:
                fallback_used = True
                fallback_reason = "required environmental features unavailable"
                warnings.append(
                    "Fallback motion baseline used because environmental features are unavailable"
                )
                LOGGER.warning(
                    "inference fallback used",
                    extra={
                        "storm_id": request.storm_id,
                        "reason": fallback_reason,
                        "model_version": self.version,
                    },
                )
            direction = bearing_deg(first.lat, first.lon, last.lat, last.lon)
            coords = [
                destination_point(last.lat, last.lon, direction, speed * h)
                for h in request.horizons
            ]
            classes = [last.intensity] * len(coords)
            radii = [max(30.0, h * 5.0) for h in request.horizons]
            uncertainty = (
                "Illustrative radius 5 km/hour (minimum 30 km); not calibrated"
            )
            warnings.append(
                "Untrained constant-motion baseline; illustrative uncertainty"
            )
        if any(f.source == "synthetic-demo" for f in fixes):
            warnings.append("SYNTHETIC DEMO DATA - not a real storm")
        points = [
            ForecastPoint(
                horizon_hours=h,
                valid_time=last.timestamp + timedelta(hours=h),
                lat=float(lat),
                lon=float(lon),
                intensity=str(intensity),
                radius_km=float(radius),
                cone=circle(lat, lon, radius),
            )
            for h, (lat, lon), intensity, radius in zip(
                request.horizons, coords, classes, radii
            )
        ]
        return ForecastResponse(
            forecast_id=forecast_id,
            run_id=forecast_id,
            storm_id=request.storm_id,
            issue_time=last.timestamp,
            generated_at=current_time,
            model_version=self.version,
            model_kind="motion-baseline" if fallback_used else self.kind,
            dataset_version=self.dataset,
            input_revision=hashlib.sha256(
                request.model_dump_json().encode("utf-8")
            ).hexdigest(),
            feature_schema_version=self.feature_schema_version,
            scaler_version=self.scaler_version,
            fallback_used=fallback_used,
            fallback_reason=fallback_reason,
            sources=sorted({f.source for f in fixes}),
            uncertainty_method=uncertainty,
            warnings=warnings,
            points=points,
        )
