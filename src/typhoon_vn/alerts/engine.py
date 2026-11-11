"""Deterministic alert rules and draft-first delivery orchestration."""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from typing import Callable, Protocol


class Severity(StrEnum):
    WATCH = "watch"
    WARNING = "warning"
    EMERGENCY = "emergency"


@dataclass(frozen=True, slots=True)
class AlertRule:
    radius_km: float = 200
    lead_hours: int = 72
    cooldown_hours: int = 12
    warning_km: float = 120
    emergency_km: float = 60

    def __post_init__(self) -> None:
        if not 0 < self.emergency_km <= self.warning_km <= self.radius_km:
            raise ValueError("distance thresholds must be positive and ordered")
        if not 0 < self.lead_hours <= 168 or self.cooldown_hours < 0:
            raise ValueError("invalid lead/cooldown")

    def severity(self, distance_km: float) -> Severity | None:
        if distance_km < 0:
            raise ValueError("distance cannot be negative")
        if distance_km <= self.emergency_km:
            return Severity.EMERGENCY
        if distance_km <= self.warning_km:
            return Severity.WARNING
        if distance_km <= self.radius_km:
            return Severity.WATCH
        return None


@dataclass(frozen=True, slots=True)
class AlertDraft:
    id: str
    subscription_id: str
    forecast_id: str
    storm_id: str
    severity: Severity
    closest_km: float
    horizon_hours: int
    issue_time: str
    source: tuple[str, ...]
    message: str
    disclaimer: str
    status: str = "draft"


@dataclass(frozen=True, slots=True)
class DeliveryResult:
    delivery_id: str
    status: str
    attempts: int
    error: str | None = None


class Transport(Protocol):
    def send(self, draft: AlertDraft, delivery_id: str) -> None: ...


@dataclass(slots=True)
class InMemoryDeliveryState:
    delivered: set[str] = field(default_factory=set)
    last_by_subscription_storm: dict[tuple[str, str], datetime] = field(
        default_factory=dict
    )
    history: list[DeliveryResult] = field(default_factory=list)


def evaluate(
    subscription_id: str, subscription: dict, forecast: dict
) -> AlertDraft | None:
    rule = AlertRule(
        radius_km=float(subscription["radius_km"]),
        lead_hours=int(subscription["lead_hours"]),
        cooldown_hours=int(subscription.get("cooldown_hours", 12)),
    )
    eligible = [
        p for p in forecast["points"] if int(p["horizon_hours"]) <= rule.lead_hours
    ]
    if not eligible:
        return None
    point = min(eligible, key=lambda p: float(p["distance_km"]))
    distance = float(point["distance_km"])
    severity = rule.severity(distance)
    if severity is None:
        return None
    identifier = hashlib.sha256(
        f'{subscription_id}:{forecast["forecast_id"]}'.encode()
    ).hexdigest()
    sources = tuple(str(s) for s in forecast.get("sources", ()))
    source_text = ", ".join(sources) if sources else "unknown/unverified"
    message = f'{severity.value.upper()}: {forecast["storm_id"]} is forecast within {distance:.1f} km of {subscription["label"]} at +{point["horizon_hours"]}h. Source: {source_text}; issue time: {forecast["issue_time"]}.'
    return AlertDraft(
        identifier,
        subscription_id,
        str(forecast["forecast_id"]),
        str(forecast["storm_id"]),
        severity,
        distance,
        int(point["horizon_hours"]),
        str(forecast["issue_time"]),
        sources,
        message,
        str(forecast["disclaimer"]),
    )


def deliver(
    draft: AlertDraft,
    transport: Transport,
    state: InMemoryDeliveryState,
    *,
    cooldown_hours: int = 12,
    max_attempts: int = 3,
    now: datetime | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> DeliveryResult:
    now = now or datetime.now(timezone.utc)
    key = (draft.subscription_id, draft.storm_id)
    previous = state.last_by_subscription_storm.get(key)
    if draft.id in state.delivered:
        result = DeliveryResult(draft.id, "duplicate", 0)
        state.history.append(result)
        return result
    if previous and now - previous < timedelta(hours=cooldown_hours):
        result = DeliveryResult(draft.id, "throttled", 0)
        state.history.append(result)
        return result
    error = None
    for attempt in range(1, max_attempts + 1):
        try:
            transport.send(draft, draft.id)
            state.delivered.add(draft.id)
            state.last_by_subscription_storm[key] = now
            result = DeliveryResult(draft.id, "delivered", attempt)
            state.history.append(result)
            return result
        except Exception as exc:
            error = str(exc)
            if attempt < max_attempts:
                sleep(min(2 ** (attempt - 1), 30))
    result = DeliveryResult(draft.id, "dead_letter", max_attempts, error)
    state.history.append(result)
    return result
