"""Explainable analog suggestions served alongside the forecast."""

import json
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import pytest

from typhoon_vn.api.schemas import Fix, ForecastRequest, ForecastResponse
from typhoon_vn.datasets.synthetic import generate_synthetic_catalogue
from typhoon_vn.datasets.typhoon_dataset import DatasetConfig
from typhoon_vn.evaluation.comparison import build_windows
from typhoon_vn.features.build import FEATURE_COLUMNS
from typhoon_vn.inference.analog import AnalogService, save_analog_artifact
from typhoon_vn.inference.service import TyphoonForecaster

HORIZONS = [6, 12, 24, 48, 72]


@pytest.fixture()
def artifact(tmp_path):
    frame = generate_synthetic_catalogue(n_storms=8, n_fixes=24, seed=4)
    windows = build_windows(frame, DatasetConfig(feature_cols=tuple(FEATURE_COLUMNS)))
    return save_analog_artifact(
        tmp_path / "analog.npz",
        x_raw=windows.x_raw,
        y=windows.y,
        storm_ids=windows.storm_ids,
        storm_names=[f"NAME-{s}" for s in windows.storm_ids],
        issue_times=[pd.Timestamp(t).isoformat() for t in windows.issue_times],
        k=5,
        weights={"track": 1.0, "position": 1.0, "season": 0.5},
        horizons_hours=HORIZONS,
        dataset_version="synthetic",
    )


def fixes(n=6, step_h=6):
    start = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    start -= timedelta(hours=start.hour % 6 + step_h * (n - 1))
    return [
        Fix(
            timestamp=start + timedelta(hours=step_h * i),
            lat=14 + 0.3 * i,
            lon=125 - 0.5 * i,
            wind_ms=30,
            pressure_hpa=980,
            intensity="TY",
            source="test",
        )
        for i in range(n)
    ]


def test_suggestion_has_track_and_named_distinct_analogs(artifact) -> None:
    service = AnalogService(artifact)
    observed = fixes()
    suggestion = service.suggest(observed, HORIZONS)
    assert [p.horizon_hours for p in suggestion.points] == HORIZONS
    for point in suggestion.points:
        assert point.valid_time == observed[-1].timestamp + timedelta(
            hours=point.horizon_hours
        )
    names = [a.name for a in suggestion.analogs]
    assert names and all(name.startswith("NAME-") for name in names)
    assert len({a.storm_id for a in suggestion.analogs}) == len(suggestion.analogs)
    assert [a.rank for a in suggestion.analogs] == list(range(1, len(names) + 1))


def test_forecast_response_carries_suggestion_and_round_trips(artifact) -> None:
    forecaster = TyphoonForecaster(analog_artifact=artifact)
    response = forecaster.forecast(ForecastRequest(storm_id="S", observations=fixes()))
    assert response.suggestion is not None
    restored = ForecastResponse.model_validate(json.loads(response.model_dump_json()))
    assert restored.suggestion == response.suggestion


def test_short_or_irregular_tracks_warn_instead_of_failing(artifact) -> None:
    forecaster = TyphoonForecaster(analog_artifact=artifact)
    short = forecaster.forecast(ForecastRequest(storm_id="S", observations=fixes(n=3)))
    assert short.suggestion is None
    assert any("No analog suggestion" in w for w in short.warnings)
    irregular = forecaster.forecast(
        ForecastRequest(storm_id="S", observations=fixes(n=6, step_h=3))
    )
    assert irregular.suggestion is None


def test_artifact_is_pickle_free_and_schema_checked(artifact, tmp_path) -> None:
    with np.load(artifact, allow_pickle=False) as data:
        meta = json.loads(str(data["meta"]))
        arrays = {name: data[name] for name in data.files}
    meta["feature_columns"] = ["lat", "lon"]
    arrays["meta"] = np.asarray(json.dumps(meta))
    broken = tmp_path / "broken.npz"
    np.savez(broken, **arrays)
    with pytest.raises(ValueError, match="feature columns"):
        AnalogService(broken)


def test_cache_key_changes_with_analog_library(artifact) -> None:
    request = ForecastRequest(storm_id="S", observations=fixes())
    assert TyphoonForecaster().key(request) != TyphoonForecaster(
        analog_artifact=artifact
    ).key(request)
