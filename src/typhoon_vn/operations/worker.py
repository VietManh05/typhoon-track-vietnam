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
        except ValueError as exc:
            # Expected for short/irregular tracks; not an operational error.
            logger.warning("Forecast skipped for %s: %s", batch.storm_id, exc)
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


def snapshot_source(snapshot: Path):
    """Batches from a JSON snapshot file (list of ObservationBatch payloads)."""

    def load():
        return json.loads(Path(snapshot).read_text(encoding="utf-8"))

    return load


def run_worker(store, forecaster, *, source, interval=1800, once=False, delivery=None):
    """Poll ``source()`` for observation batches and refresh forecasts.

    ``source`` is any callable returning ObservationBatch objects or payloads,
    e.g. :func:`snapshot_source` or ``typhoon_vn.operations.live``. When an
    enabled ``delivery`` config (``operations.delivery``) is given, pending alert
    drafts are sent after each cycle.
    """

    if interval < 1:
        raise ValueError("interval must be positive")
    while True:
        try:
            batches = source()
            ids = update(store, forecaster, batches)
            logger.info("Processed %d batches, %d forecasts", len(batches), len(ids))
            if delivery is not None and delivery.enabled:
                from typhoon_vn.operations.delivery import deliver_pending

                logger.info("Alert delivery: %s", deliver_pending(store, delivery))
        except Exception:
            logger.exception("Worker update failed")
            if once:
                raise
        if once:
            return
        time.sleep(interval)
