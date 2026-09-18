"""Validated model-bundle export, load and inference utilities."""

from __future__ import annotations

import hashlib
import json
from datetime import timezone
from pathlib import Path
from typing import Any, Sequence

import numpy as np
import pandas as pd
import torch

from typhoon_vn.api.schemas import Fix
from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.models.lstm import LSTMTrackForecaster

BUNDLE_SCHEMA_VERSION = 1
INTENSITY_LABELS = ("TD", "TS", "STS", "TY", "STY", "SUPERTY", "UNK")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _feature_hash(columns: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(columns).encode()).hexdigest()


def _scaler_state(scaler: FeatureScaler) -> dict[str, Any]:
    if not scaler.is_fitted:
        raise ValueError("bundle scaler must be fitted")
    return {
        "feature_columns": scaler.feature_columns,
        "fill_values": scaler._fill_values.tolist(),
        "mean": scaler._scaler.mean_.tolist(),
        "scale": scaler._scaler.scale_.tolist(),
        "var": scaler._scaler.var_.tolist(),
        "n_samples_seen": np.asarray(scaler._scaler.n_samples_seen_).tolist(),
    }


def _scaler_from_state(state: dict[str, Any]) -> FeatureScaler:
    required = {"feature_columns", "fill_values", "mean", "scale", "var", "n_samples_seen"}
    if set(state) != required:
        raise ValueError("invalid scaler schema")
    scaler = FeatureScaler(list(state["feature_columns"]))
    n = len(scaler.feature_columns)
    arrays = {
        name: np.asarray(state[name], dtype=float)
        for name in ("fill_values", "mean", "scale", "var")
    }
    if any(value.shape != (n,) or not np.isfinite(value).all() for value in arrays.values()):
        raise ValueError("invalid scaler values")
    scaler._fill_values = arrays["fill_values"]
    scaler._scaler.mean_ = arrays["mean"]
    scaler._scaler.scale_ = arrays["scale"]
    scaler._scaler.var_ = arrays["var"]
    scaler._scaler.n_features_in_ = n
    scaler._scaler.n_samples_seen_ = np.asarray(state["n_samples_seen"])
    scaler._fitted = True
    return scaler


def export_bundle(
    directory: str | Path,
    model: LSTMTrackForecaster,
    scaler: FeatureScaler,
    *,
    version: str,
    dataset_version: str,
    dataset_sha256: str,
    model_config: dict[str, Any],
    input_len: int,
    horizons_hours: Sequence[int],
    validation_radius_km: dict[str, float],
    split_manifest: dict[str, Any],
    synthetic: bool = False,
) -> Path:
    """Export a deterministic, checksum-verified directory bundle."""

    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    if scaler.feature_columns != list(FEATURE_COLUMNS):
        raise ValueError("scaler feature contract does not match FEATURE_COLUMNS")
    if sorted(map(int, validation_radius_km)) != sorted(horizons_hours):
        raise ValueError("calibration radii must cover every horizon")

    weights = directory / "weights.pt"
    scaler_path = directory / "scaler.json"
    split_path = directory / "split-manifest.json"
    torch.save(model.state_dict(), weights)
    scaler_path.write_text(json.dumps(_scaler_state(scaler), sort_keys=True), encoding="utf-8")
    split_path.write_text(json.dumps(split_manifest, sort_keys=True), encoding="utf-8")
    manifest = {
        "bundle_schema_version": BUNDLE_SCHEMA_VERSION,
        "version": version,
        "dataset_version": dataset_version,
        "dataset_sha256": dataset_sha256,
        "synthetic": synthetic,
        "model": {"type": "LSTMTrackForecaster", "constructor": model_config},
        "input_len": input_len,
        "time_step_hours": 6,
        "feature_columns": list(FEATURE_COLUMNS),
        "feature_schema_sha256": _feature_hash(FEATURE_COLUMNS),
        "horizons_hours": list(horizons_hours),
        "intensity_labels": list(INTENSITY_LABELS),
        "validation_radius_km": validation_radius_km,
        "uncertainty_method": "held-out validation radial error; not calibrated coverage",
        "split_manifest_sha256": _sha256(split_path),
        "files": {
            "weights.pt": _sha256(weights),
            "scaler.json": _sha256(scaler_path),
            "split-manifest.json": _sha256(split_path),
        },
    }
    manifest_path = directory / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest_path


def load_bundle(path: str | Path) -> dict[str, Any]:
    """Load only a strict allowlisted bundle after verifying all checksums."""

    root = Path(path)
    if root.is_file():
        if root.name != "manifest.json":
            raise ValueError("bundle path must be a directory or manifest.json")
        root = root.parent
    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    required = {
        "bundle_schema_version", "version", "dataset_version", "dataset_sha256",
        "synthetic", "model", "input_len", "time_step_hours", "feature_columns",
        "feature_schema_sha256", "horizons_hours", "intensity_labels",
        "validation_radius_km", "uncertainty_method", "split_manifest_sha256", "files",
    }
    if set(manifest) != required:
        raise ValueError("invalid bundle manifest schema")
    if manifest["bundle_schema_version"] != BUNDLE_SCHEMA_VERSION:
        raise ValueError("unsupported bundle schema version")
    if manifest["feature_columns"] != list(FEATURE_COLUMNS):
        raise ValueError("bundle feature columns mismatch")
    if manifest["feature_schema_sha256"] != _feature_hash(FEATURE_COLUMNS):
        raise ValueError("bundle feature schema checksum mismatch")
    if set(manifest["files"]) != {"weights.pt", "scaler.json", "split-manifest.json"}:
        raise ValueError("invalid bundle file list")
    for name, expected in manifest["files"].items():
        file_path = root / name
        if not file_path.is_file() or _sha256(file_path) != expected:
            raise ValueError(f"bundle checksum mismatch: {name}")
    if manifest["split_manifest_sha256"] != manifest["files"]["split-manifest.json"]:
        raise ValueError("split manifest checksum mismatch")
    if manifest["model"].get("type") != "LSTMTrackForecaster":
        raise ValueError("model type is not allowlisted")
    constructor = manifest["model"].get("constructor")
    allowed = {"n_features", "n_horizons", "n_classes", "hidden_size", "num_layers", "dropout"}
    if not isinstance(constructor, dict) or set(constructor) != allowed:
        raise ValueError("invalid model constructor schema")
    if constructor["n_features"] != len(FEATURE_COLUMNS):
        raise ValueError("model feature dimension mismatch")
    if constructor["n_horizons"] != len(manifest["horizons_hours"]):
        raise ValueError("model horizon dimension mismatch")
    if constructor["n_classes"] != len(manifest["intensity_labels"]):
        raise ValueError("model class dimension mismatch")
    if sorted(map(int, manifest["validation_radius_km"])) != sorted(manifest["horizons_hours"]):
        raise ValueError("calibration horizon mismatch")

    scaler_state = json.loads((root / "scaler.json").read_text(encoding="utf-8"))
    scaler = _scaler_from_state(scaler_state)
    if scaler.feature_columns != manifest["feature_columns"]:
        raise ValueError("scaler feature columns mismatch")
    model = LSTMTrackForecaster(**constructor)
    state = torch.load(root / "weights.pt", map_location="cpu", weights_only=True)
    model.load_state_dict(state, strict=True)
    model.eval()
    return {"manifest": manifest, "model": model, "scaler": scaler, "root": root}


def predict_bundle(
    bundle: dict[str, Any], fixes: Sequence[Fix], horizons: Sequence[int]
) -> tuple[list[tuple[float, float]], list[str]]:
    """Run the exact training feature/scaler path without refitting."""

    manifest = bundle["manifest"]
    input_len = int(manifest["input_len"])
    if len(fixes) < input_len:
        raise ValueError(f"at least {input_len} observations are required")
    requested = list(horizons)
    available = list(manifest["horizons_hours"])
    if any(h not in available for h in requested):
        raise ValueError("requested horizon is absent from bundle")
    frame = pd.DataFrame(
        {
            "storm_id": ["inference"] * len(fixes),
            "timestamp": [fix.timestamp.astimezone(timezone.utc) for fix in fixes],
            "lat": [fix.lat for fix in fixes], "lon": [fix.lon for fix in fixes],
            "wind_ms": [fix.wind_ms for fix in fixes],
            "pressure_hpa": [fix.pressure_hpa for fix in fixes],
            "intensity": [fix.intensity for fix in fixes],
        }
    )
    times = pd.to_datetime(frame["timestamp"], utc=True)
    if times.duplicated().any() or not times.is_monotonic_increasing:
        raise ValueError("observations must have unique increasing timestamps")
    window_times = times.iloc[-input_len:]
    expected = pd.Timedelta(hours=int(manifest["time_step_hours"]))
    if not (window_times.diff().dropna() == expected).all():
        raise ValueError("input window must have regular bundle time steps")
    matrix = FeatureBuilder().feature_matrix(frame)
    scaled = bundle["scaler"].transform(matrix)
    x = torch.tensor(scaled.iloc[-input_len:].to_numpy(), dtype=torch.float32).unsqueeze(0)
    mask = torch.ones((1, input_len), dtype=torch.float32)
    with torch.no_grad():
        output = bundle["model"](x, mask)
    indices = [available.index(h) for h in requested]
    coords_array = output["reg"][0, indices].cpu().numpy()
    class_indices = output["cls"][0, indices].argmax(dim=-1).cpu().tolist()
    if not np.isfinite(coords_array).all():
        raise ValueError("model output is non-finite")
    coords = [(float(lat), float(lon)) for lat, lon in coords_array]
    if any(not -90 <= lat <= 90 or not -180 <= lon <= 180 for lat, lon in coords):
        raise ValueError("model output is outside WGS84 bounds")
    labels = [manifest["intensity_labels"][index] for index in class_indices]
    return coords, labels
