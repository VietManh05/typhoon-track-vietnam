"""Live skill monitoring: verify issued forecasts against later observations.

Every stored forecast point whose valid time now has an observation of the
same storm is scored (great-circle error, and whether the observed position
fell inside the forecast's cone radius). The cone was calibrated for 80%
coverage on validation data, so coverage well below that on enough verified
points means the model is degrading on current storms.

Used by ``/metrics`` (Prometheus gauges) and ``typhoon-vn monitor`` (exit code
2 when degraded, for cron/alerting).
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from typhoon_vn.features.geo import haversine_km

HORIZONS = (6, 12, 24, 48, 72)


def verify_forecasts(store, limit: int = 2000) -> dict:
    tracks: dict[str, dict[datetime, tuple[float, float]]] = {}
    errors: dict[int, list[float]] = defaultdict(list)
    inside: dict[int, list[bool]] = defaultdict(list)
    forecasts = store.recent_forecasts(limit)
    for forecast in forecasts:
        storm = forecast["storm_id"]
        if storm not in tracks:
            tracks[storm] = {f.timestamp: (f.lat, f.lon) for f in store.track(storm)}
        observed = tracks[storm]
        for point in forecast["points"]:
            actual = observed.get(datetime.fromisoformat(point["valid_time"]))
            if actual is None:
                continue
            error = haversine_km(point["lat"], point["lon"], *actual)
            errors[point["horizon_hours"]].append(error)
            inside[point["horizon_hours"]].append(error <= point["radius_km"])
    horizons = []
    for h in sorted(set(HORIZONS) | set(errors)):
        n = len(errors[h])
        horizons.append(
            {
                "horizon_h": h,
                "n": n,
                "mean_error_km": round(sum(errors[h]) / n, 1) if n else None,
                "cone_coverage": round(sum(inside[h]) / n, 3) if n else None,
            }
        )
    return {"forecasts_checked": len(forecasts), "horizons": horizons}


def assess(report: dict, *, min_n: int = 20, min_coverage: float = 0.6) -> dict:
    """``ok`` / ``degraded`` / ``insufficient-data`` with human-readable reasons."""

    reasons, enough = [], False
    for row in report["horizons"]:
        if row["n"] < min_n:
            continue
        enough = True
        if row["cone_coverage"] < min_coverage:
            reasons.append(
                f"{row['horizon_h']} h cone coverage {row['cone_coverage']:.0%} "
                f"< {min_coverage:.0%} over {row['n']} verified points"
            )
    status = "degraded" if reasons else ("ok" if enough else "insufficient-data")
    return {"status": status, "reasons": reasons}
