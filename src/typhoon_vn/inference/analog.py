"""Serve k-NN analog suggestions: a track plus the historical storms behind it.

The artifact is a pickle-free ``.npz`` holding the analog library (raw input
windows, observed future positions, storm ids/names, issue times) and the
validation-selected hyper-parameters, so loading it cannot execute code.
"""

from __future__ import annotations

import hashlib
import json
from datetime import timedelta, timezone
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd

from typhoon_vn.api.schemas import AnalogStorm, Fix, Suggestion, SuggestionPoint
from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.models.classical import AnalogForecaster

FORMAT_VERSION = 1


def save_analog_artifact(
    path: str | Path,
    *,
    x_raw: np.ndarray,
    y: np.ndarray,
    storm_ids: Sequence[str],
    storm_names: Sequence[str],
    issue_times: Sequence[str],
    k: int,
    weights: dict[str, float],
    horizons_hours: Sequence[int],
    dataset_version: str,
) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = {
        "format_version": FORMAT_VERSION,
        "feature_columns": list(FEATURE_COLUMNS),
        "input_len": int(x_raw.shape[1]),
        "horizons_hours": [int(h) for h in horizons_hours],
        "k": int(k),
        "weights": {key: float(value) for key, value in weights.items()},
        "dataset_version": dataset_version,
    }
    np.savez_compressed(
        path,
        x_raw=x_raw.astype(np.float32),
        y=y.astype(np.float32),
        storm_ids=np.asarray(storm_ids, dtype=str),
        storm_names=np.asarray(storm_names, dtype=str),
        issue_times=np.asarray(issue_times, dtype=str),
        meta=np.asarray(json.dumps(meta, sort_keys=True)),
    )
    return path


class AnalogService:
    """Load the analog library once; suggest tracks for incoming fixes."""

    def __init__(self, path: str | Path) -> None:
        path = Path(path)
        with np.load(path, allow_pickle=False) as data:
            self.meta = json.loads(str(data["meta"]))
            arrays = {name: data[name] for name in data.files if name != "meta"}
        if self.meta.get("format_version") != FORMAT_VERSION:
            raise ValueError("unsupported analog artifact version")
        if self.meta["feature_columns"] != list(FEATURE_COLUMNS):
            raise ValueError("analog artifact feature columns mismatch")
        self.version = (
            "analog-knn-" + hashlib.sha256(path.read_bytes()).hexdigest()[:12]
        )
        self.input_len = int(self.meta["input_len"])
        self.horizons = list(self.meta["horizons_hours"])
        self.names = dict(
            zip(arrays["storm_ids"].tolist(), arrays["storm_names"].tolist())
        )
        self.model = AnalogForecaster(
            k=self.meta["k"], weights=self.meta["weights"]
        ).fit(
            arrays["x_raw"].astype(float),
            arrays["y"].astype(float),
            arrays["storm_ids"],
            arrays["issue_times"],
        )

    def _window(self, fixes: Sequence[Fix]) -> np.ndarray:
        if len(fixes) < self.input_len:
            raise ValueError(f"at least {self.input_len} observations are required")
        frame = pd.DataFrame(
            {
                "storm_id": ["inference"] * len(fixes),
                "timestamp": [f.timestamp.astimezone(timezone.utc) for f in fixes],
                "lat": [f.lat for f in fixes],
                "lon": [f.lon for f in fixes],
                "wind_ms": [f.wind_ms for f in fixes],
                "pressure_hpa": [f.pressure_hpa for f in fixes],
                "intensity": [f.intensity for f in fixes],
            }
        )
        times = pd.to_datetime(frame["timestamp"], utc=True).iloc[-self.input_len :]
        if not (times.diff().dropna() == pd.Timedelta(hours=6)).all():
            raise ValueError("analog suggestion needs a regular 6-hour input window")
        matrix = FeatureBuilder().feature_matrix(frame)
        return matrix.iloc[-self.input_len :].to_numpy(dtype=float)[None, :, :]

    def suggest(
        self, fixes: Sequence[Fix], horizons: Sequence[int], top: int = 5
    ) -> Suggestion:
        missing = [h for h in horizons if h not in self.horizons]
        if missing:
            raise ValueError(f"analog library has no horizons {missing}")
        window = self._window(fixes)
        track = self.model.predict(window)[0]
        issue = fixes[-1].timestamp
        points = [
            SuggestionPoint(
                horizon_hours=h,
                valid_time=issue + timedelta(hours=h),
                lat=float(track[self.horizons.index(h), 0]),
                lon=float(((track[self.horizons.index(h), 1] + 180) % 360) - 180),
            )
            for h in horizons
        ]
        analogs = [
            AnalogStorm(
                rank=rank,
                storm_id=item["storm_id"],
                name=self.names.get(item["storm_id"]) or item["storm_id"],
                year=pd.Timestamp(item["issue_time"]).year,
                issue_time=pd.Timestamp(item["issue_time"]).to_pydatetime(),
            )
            for rank, item in enumerate(self.model.explain(window, top=top)[0], 1)
        ]
        return Suggestion(
            method=(
                f"k-NN analog (k={self.meta['k']}) over "
                f"{self.meta['dataset_version']}"
            ),
            note=(
                "Weighted average of what the most similar historical situations "
                "did next; same skill as the trained model on 2021-2024 test storms."
            ),
            points=points,
            analogs=analogs,
        )
