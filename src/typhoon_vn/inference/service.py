"""Thread-safe, reusable forecasting with explicit model provenance."""
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import RLock

from typhoon_vn.api.schemas import ForecastPoint, ForecastRequest, ForecastResponse
from typhoon_vn.features.geo import bearing_deg, destination_point, haversine_km

def circle(lat, lon, radius):
    ring = []
    for angle in range(0, 361, 10):
        y, x = destination_point(lat, lon, angle, radius)
        ring.append([x, y])
    return {"type": "Polygon", "coordinates": [ring]}

class TyphoonForecaster:
    def __init__(self, artifact: Path | None = None, allow_baseline=True):
        self.lock = RLock()
        self.bundle = None
        if artifact:
            from typhoon_vn.training.pipeline import load_bundle
            self.bundle = load_bundle(artifact)
        elif not allow_baseline:
            raise ValueError("A promoted model artifact is required")
        self.version = self.bundle["manifest"]["version"] if self.bundle else "persistence-v1"
        self.kind = "trained-model" if self.bundle else "motion-baseline"
        self.dataset = self.bundle["manifest"]["dataset_version"] if self.bundle else "none"

    def key(self, request):
        body = request.model_dump_json() + self.version
        return hashlib.sha256(body.encode()).hexdigest()

    def forecast(self, request: ForecastRequest) -> ForecastResponse:
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
        if last.timestamp < datetime.now(timezone.utc) - timedelta(hours=24):
            warnings.append("Observations are older than 24 hours")
        if last.timestamp > datetime.now(timezone.utc) + timedelta(minutes=10):
            raise ValueError("Observation timestamp is in the future")
        if self.bundle:
            from typhoon_vn.training.pipeline import predict_bundle
            with self.lock:
                coords, classes = predict_bundle(self.bundle, fixes, request.horizons)
            radii = [self.bundle["manifest"]["validation_radius_km"][str(h)]
                     for h in request.horizons]
            uncertainty = "80th percentile validation radial error; not calibrated coverage"
            warnings.append("Experimental model; held-out validation is not operational certification")
        else:
            direction = bearing_deg(first.lat, first.lon, last.lat, last.lon)
            coords = [destination_point(last.lat, last.lon, direction, speed*h)
                      for h in request.horizons]
            classes = [last.intensity] * len(coords)
            radii = [max(30.0, h*5.0) for h in request.horizons]
            uncertainty = "Illustrative radius 5 km/hour (minimum 30 km); not calibrated"
            warnings.append("Untrained constant-motion baseline; illustrative uncertainty")
        if any(f.source == "synthetic-demo" for f in fixes):
            warnings.append("SYNTHETIC DEMO DATA - not a real storm")
        points = [
            ForecastPoint(horizon_hours=h, valid_time=last.timestamp+timedelta(hours=h),
                          lat=float(lat), lon=float(lon), intensity=str(intensity),
                          radius_km=float(radius), cone=circle(lat, lon, radius))
            for h, (lat, lon), intensity, radius in zip(
                request.horizons, coords, classes, radii)
        ]
        return ForecastResponse(
            forecast_id=self.key(request), storm_id=request.storm_id,
            issue_time=last.timestamp, generated_at=datetime.now(timezone.utc),
            model_version=self.version, model_kind=self.kind, dataset_version=self.dataset,
            sources=sorted({f.source for f in fixes}), uncertainty_method=uncertainty,
            warnings=warnings, points=points,
        )
