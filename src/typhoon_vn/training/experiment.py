"""Local-first experiment tracking with optional MLflow integration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def flatten_params(payload: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    """Flatten nested config values into MLflow-compatible scalar params."""

    result: dict[str, Any] = {}
    for key, value in payload.items():
        name = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            result.update(flatten_params(value, name))
        elif isinstance(value, (str, int, float, bool)) or value is None:
            result[name] = value
        else:
            result[name] = json.dumps(value, sort_keys=True)
    return result


class ExperimentTracker:
    """Persist an audit record and mirror it to MLflow when enabled."""

    def __init__(
        self,
        output_dir: str | Path,
        *,
        name: str,
        enabled: bool = False,
        tracking_uri: str = "mlruns",
        experiment_name: str = "typhoon_vn",
    ) -> None:
        self.output_dir = Path(output_dir)
        self.name = name
        self.enabled = enabled
        self.tracking_uri = tracking_uri
        self.experiment_name = experiment_name
        self.run_id: str | None = None
        self._mlflow: Any = None
        self._params: dict[str, Any] = {}
        self._metrics: list[dict[str, Any]] = []
        self._artifacts: list[str] = []

    def __enter__(self) -> "ExperimentTracker":
        self.output_dir.mkdir(parents=True, exist_ok=True)
        if self.enabled:
            try:
                import mlflow
            except ImportError as exc:
                raise RuntimeError("MLflow tracking requires the experiment extra") from exc
            mlflow.set_tracking_uri(self.tracking_uri)
            mlflow.set_experiment(self.experiment_name)
            active = mlflow.start_run(run_name=self.name)
            self._mlflow = mlflow
            self.run_id = active.info.run_id
        return self

    def log_params(self, payload: dict[str, Any]) -> None:
        values = flatten_params(payload)
        self._params.update(values)
        if self._mlflow is not None:
            self._mlflow.log_params(values)

    def log_metrics(self, payload: dict[str, float], *, step: int | None = None) -> None:
        values = {key: float(value) for key, value in payload.items()}
        record: dict[str, Any] = {"values": values}
        if step is not None:
            record["step"] = int(step)
        self._metrics.append(record)
        if self._mlflow is not None:
            self._mlflow.log_metrics(values, step=step)

    def log_artifact(self, path: str | Path) -> None:
        artifact = Path(path)
        if not artifact.is_file():
            raise ValueError(f"artifact does not exist: {artifact}")
        self._artifacts.append(str(artifact.resolve()))
        if self._mlflow is not None:
            self._mlflow.log_artifact(str(artifact))

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        status = "FAILED" if exc_type is not None else "FINISHED"
        record = {
            "name": self.name,
            "status": status,
            "run_id": self.run_id,
            "tracking_uri": self.tracking_uri if self.enabled else None,
            "params": self._params,
            "metrics": self._metrics,
            "artifacts": self._artifacts,
        }
        (self.output_dir / "experiment.json").write_text(
            json.dumps(record, indent=2, sort_keys=True), encoding="utf-8"
        )
        if self._mlflow is not None:
            self._mlflow.end_run(status=status)
