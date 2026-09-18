"""Scheduling policy shared by a cron job today and an orchestrator later."""

from __future__ import annotations

from datetime import date

TYPHOON_SEASON_MONTHS = frozenset({6, 7, 8, 9, 10, 11})


def update_cadence(run_date: date) -> str:
    """Return daily in the June-November season, weekly otherwise."""

    return "daily" if run_date.month in TYPHOON_SEASON_MONTHS else "weekly"


def should_run_weekly(run_date: date) -> bool:
    """Run Monday updates only outside the configured active season."""

    return update_cadence(run_date) == "weekly" and run_date.weekday() == 0
