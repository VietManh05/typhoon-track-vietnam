"""Local file-based model registry with a promotion gate and rollback.

Stages: ``staging`` then ``production``. Every promotion is checked against a
:class:`PromotionPolicy`; production additionally requires the version to have
passed staging. Each stage keeps a history so ``rollback`` restores the
previously promoted version. Bundles are pinned by the SHA-256 of their
manifest (which itself pins weights/scaler/split checksums).
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STAGES = ("staging", "production")


@dataclass(frozen=True)
class PromotionPolicy:
    """Thresholds a candidate must meet; metrics come from the test split."""

    max_mean_error_km: float
    min_calibration_coverage: float
    # Candidate error / persistence error at the same horizon; 1.0 = must not
    # be worse than persistence. ``None`` disables the check.
    max_persistence_error_ratio: float | None = None

    def failures(self, metrics: dict[str, float]) -> list[str]:
        required = ["mean_error_km", "calibration_coverage"]
        if self.max_persistence_error_ratio is not None:
            required.append("persistence_error_ratio")
        missing = [key for key in required if key not in metrics]
        if missing:
            return [f"missing metrics: {missing}"]
        failures = []
        if metrics["mean_error_km"] > self.max_mean_error_km:
            failures.append(
                f"mean_error_km {metrics['mean_error_km']:.1f} > "
                f"{self.max_mean_error_km:.1f}"
            )
        if metrics["calibration_coverage"] < self.min_calibration_coverage:
            failures.append(
                f"calibration_coverage {metrics['calibration_coverage']:.2f} < "
                f"{self.min_calibration_coverage:.2f}"
            )
        ratio = self.max_persistence_error_ratio
        if ratio is not None and metrics["persistence_error_ratio"] > ratio:
            failures.append(
                f"error vs persistence {metrics['persistence_error_ratio']:.2f} > "
                f"{ratio:.2f}"
            )
        return failures


def promotion_metrics(
    evaluation: dict[str, Any], *, horizon_h: int
) -> dict[str, float]:
    """Gate metrics at one horizon from ``run_training``'s ``evaluation``."""

    def error(model: str) -> float:
        rows = evaluation["models"][model]
        matches = [row for row in rows if int(row["horizon_h"]) == horizon_h]
        if not matches:
            raise KeyError(f"{model} has no {horizon_h}h evaluation")
        return float(matches[0]["mean_error_km"])

    lstm = error("lstm")
    metrics = {
        "horizon_h": float(horizon_h),
        "mean_error_km": lstm,
        "persistence_error_ratio": lstm / error("persistence"),
    }
    cone = evaluation.get("cone")
    if cone is not None:
        metrics["calibration_coverage"] = float(cone["test_coverage"][str(horizon_h)])
    return metrics


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class RegistryEntry:
    version: str
    manifest: str
    manifest_sha256: str
    registered_at: str
    metadata: dict[str, Any] = field(default_factory=dict)
    promotions: list[dict[str, Any]] = field(default_factory=list)


class ModelRegistry:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.path = self.root / "registry.json"
        if self.path.exists():
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            payload = {"entries": {}, "stages": {stage: [] for stage in STAGES}}
        self._entries = {
            version: RegistryEntry(**entry)
            for version, entry in payload["entries"].items()
        }
        self._stages: dict[str, list[str]] = payload["stages"]

    def _save(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        payload = {
            "entries": {v: asdict(e) for v, e in self._entries.items()},
            "stages": self._stages,
        }
        temporary = self.path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        os.replace(temporary, self.path)

    def register(
        self,
        manifest: str | Path,
        *,
        version: str,
        metadata: dict[str, Any] | None = None,
    ) -> RegistryEntry:
        if version in self._entries:
            raise ValueError(f"version {version} is already registered")
        manifest = Path(manifest).resolve()
        entry = RegistryEntry(
            version=version,
            manifest=str(manifest),
            manifest_sha256=_sha256(manifest),
            registered_at=datetime.now(timezone.utc).isoformat(),
            metadata=dict(metadata or {}),
        )
        self._entries[version] = entry
        self._save()
        return entry

    def entry(self, version: str) -> RegistryEntry:
        if version not in self._entries:
            raise KeyError(f"unknown model version {version}")
        return self._entries[version]

    def current(self, stage: str) -> str | None:
        history = self._stages[self._stage(stage)]
        return history[-1] if history else None

    def promote(
        self,
        version: str,
        stage: str,
        *,
        metrics: dict[str, float],
        policy: PromotionPolicy,
    ) -> RegistryEntry:
        stage = self._stage(stage)
        entry = self.entry(version)
        if _sha256(Path(entry.manifest)) != entry.manifest_sha256:
            raise ValueError(f"bundle checksum changed since {version} was registered")
        failures = policy.failures(metrics)
        if failures:
            raise ValueError(f"promotion gate failed for {version}: {failures}")
        if stage == "production" and version not in self._stages["staging"]:
            raise ValueError(f"{version} must pass staging before production")
        self._stages[stage].append(version)
        entry.promotions.append(
            {
                "stage": stage,
                "at": datetime.now(timezone.utc).isoformat(),
                "metrics": dict(metrics),
                "policy": asdict(policy),
            }
        )
        self._save()
        return entry

    def rollback(self, stage: str) -> str:
        history = self._stages[self._stage(stage)]
        if len(history) < 2:
            raise ValueError(f"no earlier {stage} version to roll back to")
        history.pop()
        self._save()
        return history[-1]

    @staticmethod
    def _stage(stage: str) -> str:
        if stage not in STAGES:
            raise ValueError(f"stage must be one of {STAGES}")
        return stage
