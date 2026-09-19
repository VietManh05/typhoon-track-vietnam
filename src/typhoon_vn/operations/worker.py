"""Idempotent local/production update worker. Never sends external messages."""

import json
import logging
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from typhoon_vn.api.schemas import Fix, ForecastRequest, ObservationBatch
from typhoon_vn.features.geo import haversine_km

logger = logging.getLogger(__name__)


def evaluate_alerts(store, forecast):
    count = 0
    for identifier, subscription in store.list_subscriptions():
        points = [
            p
            for p in forecast["points"]
            if p["horizon_hours"] <= subscription["lead_hours"]
        ]
        if not points:
            continue
        closest = min(
            haversine_km(subscription["lat"], subscription["lon"], p["lat"], p["lon"])
            for p in points
        )
        if closest <= subscription["radius_km"]:
            count += store.record_alert(identifier, forecast, subscription, closest)
    return count


def update(store, forecaster, batches):
    # Validate the entire incoming snapshot before any writes.
    batches = [ObservationBatch.model_validate(b) for b in batches]
    results = []
    for batch in batches:
        store.upsert_observations(batch)
        track = store.track(batch.storm_id)
        if len(track) < 2:
            continue
        request = ForecastRequest(storm_id=batch.storm_id, observations=track[-512:])
        try:
            result = forecaster.forecast(request)
        except ValueError:
            logger.exception("Forecast rejected for %s", batch.storm_id)
            continue
        store.save_forecast(result)
        evaluate_alerts(store, result.model_dump(mode="json"))
        results.append(result.forecast_id)
    return results


def demo_batches():
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    return [
        ObservationBatch(
            storm_id="DEMO-01",
            name="Demo / Bao mo phong",
            observations=[
                Fix(
                    timestamp=now - timedelta(hours=(7 - i) * 6),
                    lat=13.5 + i * 0.28,
                    lon=119 - i * 0.45,
                    wind_ms=30 + i,
                    pressure_hpa=980 - i,
                    intensity="TY",
                    source="synthetic-demo",
                )
                for i in range(8)
            ],
        )
    ]


def run_worker(store, forecaster, snapshot: Path, interval=1800, once=False):
    if interval < 1:
        raise ValueError("interval must be positive")
    while True:
        try:
            batches = json.loads(snapshot.read_text(encoding="utf-8"))
            update(store, forecaster, batches)
            logger.info("Snapshot processed: %s", snapshot)
        except Exception:
            logger.exception("Snapshot update failed")
            if once:
                raise
        if once:
            return
        time.sleep(interval)
