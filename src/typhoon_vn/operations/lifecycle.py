"""Lifecycle controls for checkpoint retention, retraining and release gates."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True, slots=True)
class RetentionDecision:
    keep: tuple[Path, ...]
    delete: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class CheckpointRetentionPolicy:
    """Keep newest checkpoints plus explicitly promoted/best artifacts."""

    keep_last: int = 5
    keep_best: bool = True
    max_age_days: int | None = None

    def __post_init__(self) -> None:
        if self.keep_last < 1:
            raise ValueError("keep_last must be >= 1")
        if self.max_age_days is not None and self.max_age_days < 1:
            raise ValueError("max_age_days must be positive when set")

    def plan(
        self, checkpoints: Iterable[Path], *, now: datetime | None = None
    ) -> RetentionDecision:
        existing = [Path(path) for path in checkpoints if Path(path).exists()]
        ordered = sorted(existing, key=lambda path: path.stat().st_mtime, reverse=True)
        keep = set(ordered[: self.keep_last])
        if self.keep_best:
            keep.update(
                path
                for path in existing
                if "best" in path.stem.lower() or "promoted" in path.stem.lower()
            )
        if self.max_age_days is not None:
            cutoff = (now or datetime.now(timezone.utc)) - timedelta(
                days=self.max_age_days
            )
            cutoff_ts = cutoff.timestamp()
            delete = tuple(
                path
                for path in ordered
                if path not in keep and path.stat().st_mtime < cutoff_ts
            )
        else:
            delete = tuple(path for path in ordered if path not in keep)
        kept = tuple(path for path in ordered if path not in delete)
        return RetentionDecision(keep=kept, delete=delete)

    def apply(
        self, checkpoints: Iterable[Path], *, dry_run: bool = True
    ) -> RetentionDecision:
        decision = self.plan(checkpoints)
        if not dry_run:
            for path in decision.delete:
                path.unlink(missing_ok=True)
        return decision


@dataclass(frozen=True, slots=True)
class RetrainPolicy:
    interval_days: int = 14
    min_new_observations: int = 24

    def __post_init__(self) -> None:
        if self.interval_days < 1 or self.min_new_observations < 1:
            raise ValueError("retrain thresholds must be positive")

    def due(
        self,
        *,
        last_run_at: datetime | None,
        latest_observation_at: datetime | None,
        new_observations: int,
        now: datetime | None = None,
    ) -> tuple[bool, str]:
        current = now or datetime.now(timezone.utc)
        if latest_observation_at is None:
            return False, "no_observations"
        if new_observations < self.min_new_observations:
            return False, "insufficient_new_observations"
        if last_run_at is None:
            return True, "first_run"
        if current - last_run_at >= timedelta(days=self.interval_days):
            return True, "interval_elapsed"
        return False, "not_due"


@dataclass(frozen=True, slots=True)
class CapacityPlan:
    expected_rps: float
    p95_latency_ms: float
    max_replicas: int
    monthly_budget_usd: float

    def validate(self) -> None:
        if self.expected_rps <= 0 or self.p95_latency_ms <= 0:
            raise ValueError("traffic and latency assumptions must be positive")
        if self.max_replicas < 1:
            raise ValueError("max_replicas must be >= 1")
        if self.monthly_budget_usd < 0:
            raise ValueError("monthly_budget_usd must be non-negative")

    def recommended_replicas(self, *, target_rps_per_replica: float = 10.0) -> int:
        self.validate()
        if target_rps_per_replica <= 0:
            raise ValueError("target_rps_per_replica must be positive")
        needed = int(
            (self.expected_rps + target_rps_per_replica - 1) // target_rps_per_replica
        )
        return max(1, min(self.max_replicas, needed))


@dataclass(frozen=True, slots=True)
class ReleasePlan:
    environment: str
    image_tag: str
    smoke_urls: Sequence[str]
    rollback_revision: str
    credentials_confirmed: bool = False

    def validate(self, *, require_credentials: bool = False) -> list[str]:
        issues: list[str] = []
        if self.environment not in {"staging", "production"}:
            issues.append("environment must be staging or production")
        if not self.image_tag or ":" not in self.image_tag:
            issues.append("image_tag must include an immutable tag")
        if not self.smoke_urls:
            issues.append("at least one smoke URL is required")
        if not self.rollback_revision:
            issues.append("rollback_revision is required")
        if require_credentials and not self.credentials_confirmed:
            issues.append("deployment credentials are not confirmed")
        return issues
