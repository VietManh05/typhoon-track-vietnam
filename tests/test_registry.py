"""G15: model registry, promotion gate and rollback."""

import json

import pytest

from typhoon_vn.training.registry import (
    ModelRegistry,
    PromotionPolicy,
    promotion_metrics,
)

GOOD = {
    "mean_error_km": 80.0,
    "calibration_coverage": 0.85,
    "persistence_error_ratio": 0.7,
}


def _bundle(directory, text="bundle"):
    directory.mkdir(parents=True)
    manifest = directory / "manifest.json"
    manifest.write_text(text, encoding="utf-8")
    return manifest


def test_spec_promotion_gate_and_rollback(tmp_path) -> None:
    registry = ModelRegistry(tmp_path / "registry")
    first = registry.register(_bundle(tmp_path / "b1", "one"), version="v1")
    second = registry.register(_bundle(tmp_path / "b2", "two"), version="v2")
    policy = PromotionPolicy(max_mean_error_km=100.0, min_calibration_coverage=0.8)
    ok = {"mean_error_km": 80.0, "calibration_coverage": 0.9}
    registry.promote(first.version, "staging", metrics=ok, policy=policy)
    registry.promote(first.version, "production", metrics=ok, policy=policy)
    with pytest.raises(ValueError, match="promotion gate"):
        registry.promote(
            second.version,
            "production",
            metrics={"mean_error_km": 120.0, "calibration_coverage": 0.9},
            policy=policy,
        )
    better = {"mean_error_km": 70.0, "calibration_coverage": 0.9}
    registry.promote(second.version, "staging", metrics=better, policy=policy)
    registry.promote(second.version, "production", metrics=better, policy=policy)
    assert registry.current("production") == "v2"
    assert registry.rollback("production") == "v1"
    assert registry.current("production") == "v1"


def test_state_persists_and_rejects_bad_requests(tmp_path) -> None:
    root = tmp_path / "registry"
    registry = ModelRegistry(root)
    manifest = _bundle(tmp_path / "b1")
    registry.register(manifest, version="v1", metadata={"dataset_version": "d1"})
    with pytest.raises(ValueError, match="already registered"):
        registry.register(manifest, version="v1")
    policy = PromotionPolicy(max_mean_error_km=100.0, min_calibration_coverage=0.8)
    with pytest.raises(ValueError, match="staging"):
        registry.promote("v1", "production", metrics=GOOD, policy=policy)
    with pytest.raises(KeyError):
        registry.promote("nope", "staging", metrics=GOOD, policy=policy)
    with pytest.raises(ValueError, match="no earlier"):
        registry.rollback("production")

    registry.promote("v1", "staging", metrics=GOOD, policy=policy)
    reloaded = ModelRegistry(root)
    assert reloaded.current("staging") == "v1"
    assert reloaded.entry("v1").metadata == {"dataset_version": "d1"}


def test_tampered_bundle_cannot_be_promoted(tmp_path) -> None:
    registry = ModelRegistry(tmp_path / "registry")
    manifest = _bundle(tmp_path / "b1", "original")
    registry.register(manifest, version="v1")
    manifest.write_text("tampered", encoding="utf-8")
    policy = PromotionPolicy(max_mean_error_km=100.0, min_calibration_coverage=0.8)
    with pytest.raises(ValueError, match="checksum"):
        registry.promote("v1", "staging", metrics=GOOD, policy=policy)


@pytest.mark.parametrize(
    ("metrics", "reason"),
    [
        ({**GOOD, "mean_error_km": 101.0}, "mean_error_km"),
        ({**GOOD, "calibration_coverage": 0.7}, "calibration_coverage"),
        ({**GOOD, "persistence_error_ratio": 1.05}, "persistence"),
        ({"mean_error_km": 80.0}, "missing"),
    ],
)
def test_policy_reports_each_failed_criterion(metrics, reason) -> None:
    policy = PromotionPolicy(
        max_mean_error_km=100.0,
        min_calibration_coverage=0.8,
        max_persistence_error_ratio=1.0,
    )
    failures = policy.failures(metrics)
    assert failures and any(reason in failure for failure in failures)
    assert policy.failures(GOOD) == []


def test_promotion_metrics_from_evaluation() -> None:
    evaluation = {
        "models": {
            "lstm": [
                {"horizon_h": 24, "mean_error_km": 135.0},
                {"horizon_h": 72, "mean_error_km": 470.0},
            ],
            "persistence": [
                {"horizon_h": 24, "mean_error_km": 155.0},
                {"horizon_h": 72, "mean_error_km": 676.0},
            ],
        },
        "cone": {"test_coverage": {"24": 0.86, "72": 0.82}},
    }
    metrics = promotion_metrics(evaluation, horizon_h=72)
    assert metrics["mean_error_km"] == 470.0
    assert metrics["calibration_coverage"] == 0.82
    assert metrics["persistence_error_ratio"] == pytest.approx(470 / 676)
    assert json.dumps(metrics)
