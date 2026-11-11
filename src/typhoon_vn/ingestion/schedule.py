"""Scheduling policy shared by a cron job today and an orchestrator later."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

TYPHOON_SEASON_MONTHS = frozenset({6, 7, 8, 9, 10, 11})


def update_cadence(run_date: date) -> str:
    """Return daily in the June-November season, weekly otherwise."""

    return "daily" if run_date.month in TYPHOON_SEASON_MONTHS else "weekly"


def should_run_weekly(run_date: date) -> bool:
    """Run Monday updates only outside the configured active season."""

    return update_cadence(run_date) == "weekly" and run_date.weekday() == 0


@dataclass(frozen=True, slots=True)
class IngestionSchedule:
    """Deterministic live/backfill schedule with a bounded catch-up window."""

    season_months: frozenset[int] = TYPHOON_SEASON_MONTHS
    live_hour_utc: int = 0
    max_backfill_runs: int = 31

    def __post_init__(self) -> None:
        if not self.season_months or not self.season_months <= frozenset(range(1, 13)):
            raise ValueError("season_months must contain valid month numbers")
        if not 0 <= self.live_hour_utc <= 23:
            raise ValueError("live_hour_utc must be in 0..23")
        if self.max_backfill_runs < 1:
            raise ValueError("max_backfill_runs must be positive")

    def is_due(self, moment: datetime) -> bool:
        if moment.tzinfo is None or moment.utcoffset() is None:
            raise ValueError("schedule time must include a timezone")
        utc = moment.astimezone(timezone.utc)
        if utc.hour != self.live_hour_utc:
            return False
        return utc.month in self.season_months or utc.weekday() == 0

    def due_runs(
        self, *, last_success: datetime | None, now: datetime
    ) -> tuple[datetime, ...]:
        """Return missed live slots after a durable checkpoint, oldest first."""
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("now must include a timezone")
        now = now.astimezone(timezone.utc)
        if last_success is not None:
            if last_success.tzinfo is None or last_success.utcoffset() is None:
                raise ValueError("last_success must include a timezone")
            cursor = last_success.astimezone(timezone.utc) + timedelta(days=1)
        else:
            cursor = now
        cursor = cursor.replace(
            hour=self.live_hour_utc, minute=0, second=0, microsecond=0
        )
        slots: list[datetime] = []
        while cursor <= now and len(slots) < self.max_backfill_runs:
            if self.is_due(cursor):
                slots.append(cursor)
            cursor += timedelta(days=1)
        return tuple(slots)


__all__ = [
    "IngestionSchedule",
    "TYPHOON_SEASON_MONTHS",
    "should_run_weekly",
    "update_cadence",
]
