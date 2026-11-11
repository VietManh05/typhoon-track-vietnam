"""Idempotent local/production update worker. Never sends external messages."""

import json
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Protocol

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


def update(store, forecaster, batches, *, cache=None):
    # Validate the entire incoming snapshot before any writes.
    batches = [ObservationBatch.model_validate(b) for b in batches]
    results = []
    for batch in batches:
        observations_changed = store.upsert_observations(batch)
        if observations_changed and cache is not None:
            cache.invalidate_storm(batch.storm_id)
        track = store.track(batch.storm_id)
        if len(track) < 2:
            continue
        request = ForecastRequest(storm_id=batch.storm_id, observations=track[-512:])
        forecast_key = forecaster.key(request)
        stored = store.cached(forecast_key)
        if stored is not None:
            # Subscriptions created since the forecast still need evaluating.
            evaluate_alerts(store, stored)
            logger.info(
                "Observation revision already processed",
                extra={"storm_id": batch.storm_id, "forecast_id": forecast_key},
            )
            continue
        try:
            result = forecaster.forecast(request)
        except ValueError:
            logger.exception("Forecast rejected for %s", batch.storm_id)
            continue
        store.save_forecast(result)
        if cache is not None:
            cache_key = cache.key(
                storm_id=batch.storm_id,
                input_revision=request.model_dump(mode="json"),
                model_revision=getattr(
                    forecaster, "cache_revision", result.model_version
                ),
            )
            cache.put(cache_key, result.model_dump(mode="json"))
        evaluate_alerts(store, result.model_dump(mode="json"))
        results.append(result.forecast_id)
    return results


class ObservationProvider(Protocol):
    def fetch_latest(self) -> list[ObservationBatch | dict]: ...


@dataclass(slots=True)
class WorkerStatus:
    runs: int = 0
    failures: int = 0
    forecasts_created: int = 0
    last_success_at: datetime | None = None
    last_error: str | None = None


class LiveWorker:
    """Bounded-retry provider worker suitable for cron or a long-lived process."""

    def __init__(
        self,
        *,
        store,
        forecaster,
        provider: ObservationProvider,
        cache=None,
        max_attempts: int = 3,
        backoff_seconds: float = 1.0,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if max_attempts < 1 or backoff_seconds < 0:
            raise ValueError("retry configuration is invalid")
        self.store = store
        self.forecaster = forecaster
        self.provider = provider
        self.cache = cache
        self.max_attempts = max_attempts
        self.backoff_seconds = backoff_seconds
        self.sleep = sleep
        self.status = WorkerStatus()

    def run_once(self) -> list[str]:
        self.status.runs += 1
        for attempt in range(1, self.max_attempts + 1):
            try:
                batches = self.provider.fetch_latest()
                identifiers = update(
                    self.store,
                    self.forecaster,
                    batches,
                    cache=self.cache,
                )
                self.status.forecasts_created += len(identifiers)
                self.status.last_success_at = datetime.now(timezone.utc)
                self.status.last_error = None
                logger.info(
                    "worker run completed",
                    extra={
                        "attempt": attempt,
                        "forecast_count": len(identifiers),
                    },
                )
                return identifiers
            except Exception as exc:
                self.status.failures += 1
                self.status.last_error = str(exc)
                logger.warning(
                    "worker attempt failed",
                    extra={"attempt": attempt, "max_attempts": self.max_attempts},
                    exc_info=True,
                )
                if attempt == self.max_attempts:
                    raise
                self.sleep(self.backoff_seconds * (2 ** (attempt - 1)))
        raise RuntimeError("unreachable retry state")


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


def run_worker(
    store, forecaster, snapshot: Path, interval=1800, once=False, *, cache=None
):
    if interval < 1:
        raise ValueError("interval must be positive")
    while True:
        try:
            batches = json.loads(snapshot.read_text(encoding="utf-8"))
            update(store, forecaster, batches, cache=cache)
            logger.info("Snapshot processed: %s", snapshot)
        except Exception:
            logger.exception("Snapshot update failed")
            if once:
                raise
        if once:
            return
        time.sleep(interval)


def main():
    """Run a validated observation snapshot on a configurable schedule."""
    import argparse

    from typhoon_vn.inference.service import TyphoonForecaster
    from typhoon_vn.operations.store import Store
    from typhoon_vn.settings import Settings

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--interval", type=int, default=1800)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    if not args.snapshot.is_file():
        parser.error("Snapshot file does not exist")
    settings = Settings()
    logging.basicConfig(level=settings.log_level)
    store = Store(settings.operational_database_url)
    client = None
    try:
        cache = None
        if settings.cache_enabled:
            import redis

            from typhoon_vn.operations.cache import ForecastCache

            client = redis.Redis.from_url(
                settings.redis_url, socket_connect_timeout=1, socket_timeout=1
            )
            cache = ForecastCache(
                client, ttl_seconds=settings.forecast_cache_ttl_seconds
            )
        run_worker(
            store,
            TyphoonForecaster(
                settings.model_artifact,
                settings.allow_baseline,
                allow_environment_fallback=settings.allow_baseline,
            ),
            args.snapshot,
            interval=args.interval,
            once=args.once,
            cache=cache,
        )
    finally:
        if client is not None:
            client.close()
        store.engine.dispose()


if __name__ == "__main__":
    main()
