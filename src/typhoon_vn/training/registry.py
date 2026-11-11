"""Checksum-verified local model registry with audited promotion and rollback."""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True, slots=True)
class PromotionPolicy:
    max_mean_error_km: float
    min_calibration_coverage: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.max_mean_error_km) or self.max_mean_error_km < 0:
            raise ValueError("maximum error must be finite and non-negative")
        if not math.isfinite(self.min_calibration_coverage) or not (
            0 <= self.min_calibration_coverage <= 1
        ):
            raise ValueError("minimum coverage must be finite and within [0, 1]")

    def validate(self, metrics: dict[str, float]) -> None:
        required = {"mean_error_km", "calibration_coverage"}
        if not required.issubset(metrics):
            raise ValueError(f"promotion gate requires metrics: {sorted(required)}")
        if not all(math.isfinite(float(value)) for value in metrics.values()):
            raise ValueError("promotion gate requires finite metrics")
        if float(metrics["mean_error_km"]) < 0 or not (
            0 <= float(metrics["calibration_coverage"]) <= 1
        ):
            raise ValueError("promotion gate metrics are outside valid bounds")
        if float(metrics["mean_error_km"]) > self.max_mean_error_km:
            raise ValueError("promotion gate rejected mean track error")
        if float(metrics["calibration_coverage"]) < self.min_calibration_coverage:
            raise ValueError("promotion gate rejected calibration coverage")


@dataclass(frozen=True, slots=True)
class RegisteredModel:
    version: str
    bundle_path: Path
    manifest_sha256: str
    metadata: dict[str, Any]


class ModelRegistry:
    """Filesystem registry suitable for local/offline workflows and tests."""

    _STAGES = {"staging", "production"}

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.state_path = self.root / "registry.json"
        if not self.state_path.exists():
            self._write({"versions": {}, "stages": {}, "history": []})

    def _read(self) -> dict[str, Any]:
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def _write(self, payload: dict[str, Any]) -> None:
        temporary = self.state_path.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
        )
        os.replace(temporary, self.state_path)

    def register(
        self,
        manifest: str | Path,
        *,
        version: str,
        metadata: dict[str, Any],
    ) -> RegisteredModel:
        source_manifest = Path(manifest)
        if not source_manifest.is_file() or source_manifest.name != "manifest.json":
            raise ValueError("registry input must be an existing manifest.json")
        if not version or any(character in version for character in "\\/"):
            raise ValueError("version must be a non-empty path-safe name")
        if "dataset_version" not in metadata:
            raise ValueError("registry metadata requires dataset_version")
        state = self._read()
        if version in state["versions"]:
            raise ValueError(f"model version already exists: {version}")
        destination = self.root / "versions" / version
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_manifest.parent, destination)
        copied_manifest = destination / "manifest.json"
        digest = _sha256(copied_manifest)
        state["versions"][version] = {
            "bundle_path": str(destination.resolve()),
            "manifest_sha256": digest,
            "metadata": metadata,
        }
        self._write(state)
        return RegisteredModel(version, destination, digest, dict(metadata))

    def resolve(self, version_or_stage: str) -> RegisteredModel:
        state = self._read()
        version = state["stages"].get(version_or_stage, version_or_stage)
        try:
            entry = state["versions"][version]
        except KeyError as exc:
            raise KeyError(
                f"unknown model version or stage: {version_or_stage}"
            ) from exc
        manifest = Path(entry["bundle_path"]) / "manifest.json"
        if not manifest.is_file() or _sha256(manifest) != entry["manifest_sha256"]:
            raise ValueError("registered bundle manifest checksum mismatch")
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        files = payload.get("files")
        if isinstance(files, dict):
            for name, expected in files.items():
                artifact = manifest.parent / name
                if not artifact.is_file() or _sha256(artifact) != expected:
                    raise ValueError(
                        f"registered bundle artifact checksum mismatch: {name}"
                    )
        return RegisteredModel(
            version,
            Path(entry["bundle_path"]),
            entry["manifest_sha256"],
            dict(entry["metadata"]),
        )

    def promote(
        self,
        version: str,
        stage: str,
        *,
        metrics: dict[str, float],
        policy: PromotionPolicy,
    ) -> RegisteredModel:
        if stage not in self._STAGES:
            raise ValueError(f"stage must be one of {sorted(self._STAGES)}")
        model = self.resolve(version)
        policy.validate(metrics)
        state = self._read()
        if stage == "production" and state["stages"].get("staging") != version:
            raise ValueError("production promotion requires the same staging version")
        previous = state["stages"].get(stage)
        state["stages"][stage] = version
        state["history"].append(
            {
                "action": "promote",
                "stage": stage,
                "version": version,
                "previous": previous,
                "metrics": {key: float(value) for key, value in metrics.items()},
            }
        )
        self._write(state)
        return model

    def rollback(self, stage: str = "production") -> str:
        if stage not in self._STAGES:
            raise ValueError(f"stage must be one of {sorted(self._STAGES)}")
        state = self._read()
        current = state["stages"].get(stage)
        if current is None:
            raise ValueError(f"stage has no current model: {stage}")
        candidates = [
            event["previous"]
            for event in reversed(state["history"])
            if event["action"] == "promote"
            and event["stage"] == stage
            and event["version"] == current
            and event["previous"] is not None
        ]
        if not candidates:
            raise ValueError(f"stage has no rollback target: {stage}")
        target = candidates[0]
        self.resolve(target)
        state["stages"][stage] = target
        state["history"].append(
            {
                "action": "rollback",
                "stage": stage,
                "version": target,
                "previous": current,
            }
        )
        self._write(state)
        return target
