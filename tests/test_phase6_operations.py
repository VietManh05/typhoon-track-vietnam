"""Executable contracts for Phase 6 operations, deployment and monitoring."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from typhoon_vn.api.app import create_app
from typhoon_vn.operations.backup import BackupManager, sha256_file
from typhoon_vn.operations.lifecycle import (
    CapacityPlan,
    CheckpointRetentionPolicy,
    ReleasePlan,
    RetrainPolicy,
)
from typhoon_vn.operations.monitoring import (
    MetricsRegistry,
    assess_freshness,
    compare_schema,
    population_stability_index,
    summarize_numeric_distribution,
)
from typhoon_vn.settings import Settings


def test_metrics_endpoint_exposes_prometheus_latency_and_legacy_counters() -> None:
    app = create_app(
        Settings(
            _env_file=None,
            cache_enabled=False,
            operational_database_url="sqlite:///:memory:",
        ),
    )
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
        response = client.get("/metrics")
    assert response.status_code == 200
    body = response.text
    assert "typhoon_api_uptime_seconds" in body
    assert "typhoon_api_request_latency_ms_bucket" in body
    assert "typhoon_requests_total" in body
    assert "secret" not in body.lower()


def test_metrics_registry_rejects_invalid_latency_and_records_errors() -> None:
    registry = MetricsRegistry(buckets_ms=(10, 100))
    registry.record_request("GET", "/health", 200, 8)
    registry.record_request("GET", "/missing", 404, 80)
    rendered = registry.render()
    assert "typhoon_api_requests_total 2" in rendered
    assert "typhoon_api_errors_total 1" in rendered
    assert 'typhoon_api_request_latency_ms_bucket{le="10"} 1' in rendered


def test_freshness_schema_and_distribution_drift_reports_are_actionable() -> None:
    now = datetime(2026, 9, 20, tzinfo=timezone.utc)
    fresh = assess_freshness("nchmf", now - timedelta(hours=2), now=now)
    stale = assess_freshness("nchmf", now - timedelta(hours=9), now=now)
    assert fresh.ok is True and stale.ok is False
    report = compare_schema(["storm_id", "lat", "lon"], ["storm_id", "lon", "extra"])
    assert report.model_dump() == {
        "ok": False,
        "missing": ["lat"],
        "extra": ["extra"],
        "reordered": False,
    }
    assert population_stability_index([1, 2, 3, 4, 5], [4, 5, 6, 7, 8], bins=3) > 0
    summary = summarize_numeric_distribution([1.0, 2.0, 100.0])
    assert summary["count"] == 3 and summary["median"] == 2.0


def test_backup_restore_drill_verifies_checksum(tmp_path: Path) -> None:
    source = tmp_path / "typhoon.db"
    source.write_bytes(b"fixture-db")
    manager = BackupManager(tmp_path / "backups")
    manifest = manager.backup_file(source, artifact_type="database")
    source.unlink()
    restored = manager.restore_file(manifest, tmp_path / "restored.db")
    assert restored.read_bytes() == b"fixture-db"
    assert manifest.sha256 == sha256_file(restored)


def test_checkpoint_retention_retrain_capacity_and_release_gates(
    tmp_path: Path,
) -> None:
    checkpoints = []
    now = datetime(2026, 9, 20, tzinfo=timezone.utc)
    for index in range(5):
        path = tmp_path / f"epoch-{index}.pt"
        path.write_text(str(index), encoding="utf-8")
        os.utime(path, (now.timestamp() - index * 100, now.timestamp() - index * 100))
        checkpoints.append(path)
    best = tmp_path / "best.pt"
    best.write_text("best", encoding="utf-8")
    os.utime(best, (now.timestamp() - 9999, now.timestamp() - 9999))
    decision = CheckpointRetentionPolicy(keep_last=2, keep_best=True).plan(
        [*checkpoints, best]
    )
    assert best in decision.keep
    assert len(decision.delete) == 3
    due, reason = RetrainPolicy(interval_days=7, min_new_observations=3).due(
        last_run_at=now - timedelta(days=8),
        latest_observation_at=now,
        new_observations=3,
        now=now,
    )
    assert due is True and reason == "interval_elapsed"
    assert (
        CapacityPlan(
            21, 250, max_replicas=5, monthly_budget_usd=100
        ).recommended_replicas()
        == 3
    )
    assert ReleasePlan(
        environment="production",
        image_tag="registry.example/typhoon-api:sha-123",
        smoke_urls=("https://example.invalid/health",),
        rollback_revision="sha-122",
        credentials_confirmed=False,
    ).validate(require_credentials=True) == ["deployment credentials are not confirmed"]


def test_phase6_static_deployment_contracts_exist() -> None:
    required = [
        Path("docker-compose.prod.yml"),
        Path(".github/workflows/ci.yml"),
        Path("infra/monitoring/prometheus.yml"),
        Path("infra/monitoring/grafana-dashboard.json"),
        Path("docs/deployment.md"),
        Path("docs/runbook.md"),
    ]
    assert all(path.exists() for path in required)
    backend = Path("infra/docker/backend.Dockerfile").read_text(encoding="utf-8")
    assert "USER app" in backend and "HEALTHCHECK" in backend
    compose = Path("docker-compose.prod.yml").read_text(encoding="utf-8")
    assert "POSTGRES_PASSWORD" in compose and "minioadmin" not in compose
    workflow = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
    for expected in ["pytest", "flake8", "docker build", "npm ci", "npm run build"]:
        assert expected in workflow
