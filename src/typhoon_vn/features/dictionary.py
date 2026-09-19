"""Versioned data dictionary for the official model feature vocabulary."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass

from typhoon_vn.features.build import FEATURE_COLUMNS

FEATURE_SCHEMA_VERSION = "1.0.0"


@dataclass(frozen=True, slots=True)
class FeatureDefinition:
    name: str
    dtype: str
    unit: str
    description: str
    source: str
    missing_policy: str


def _definition(name: str) -> FeatureDefinition:
    unit = "1"
    source = "derived"
    missing = "reject non-finite after train-only imputation"
    if name in {"lat", "lon"} or name.startswith(("lat_lag", "lon_lag")):
        unit = "degree"
        source = "best-track observation"
    elif name.endswith("_km") or name == "step_km":
        unit = "km"
    elif "bearing" in name and not name.endswith(("_sin", "_cos")):
        unit = "degree"
    elif name == "speed_kmh":
        unit = "km/h"
    elif name == "accel_kmh2":
        unit = "km/h^2"
    elif name == "turn_rate_deg_per_h":
        unit = "degree/h"
    elif name in {"wind_ms", "wind_change_ms"}:
        unit = "m/s"
        source = "best-track observation"
    elif name in {"pressure_hpa", "pressure_change_hpa"}:
        unit = "hPa"
        source = "best-track observation"
    elif name in {"dlat", "dlon"}:
        unit = "degree/step"
    if name.startswith("intensity_"):
        missing = "map unknown labels to intensity_UNK"
    return FeatureDefinition(
        name=name,
        dtype="float32",
        unit=unit,
        description=name.replace("_", " "),
        source=source,
        missing_policy=missing,
    )


def feature_dictionary() -> tuple[FeatureDefinition, ...]:
    return tuple(_definition(name) for name in FEATURE_COLUMNS)


def feature_schema_fingerprint() -> str:
    payload = {
        "version": FEATURE_SCHEMA_VERSION,
        "features": [asdict(item) for item in feature_dictionary()],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


__all__ = [
    "FEATURE_SCHEMA_VERSION",
    "FeatureDefinition",
    "feature_dictionary",
    "feature_schema_fingerprint",
]
