"""Model bundle export/load/prediction contract."""

from datetime import timedelta

import pandas as pd
import pytest

from typhoon_vn.api.schemas import Fix
from typhoon_vn.datasets.synthetic import generate_storm_track
from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.models.lstm import LSTMTrackForecaster
from typhoon_vn.training.pipeline import export_bundle, load_bundle, predict_bundle


def make_bundle(tmp_path):
    frame = generate_storm_track("WP012024", n_fixes=20)
    matrix = FeatureBuilder().feature_matrix(frame)
    scaler = FeatureScaler(list(FEATURE_COLUMNS)).fit(matrix)
    config = {
        "n_features": len(FEATURE_COLUMNS),
        "n_horizons": 5,
        "n_classes": 7,
        "hidden_size": 8,
        "num_layers": 1,
        "dropout": 0.0,
    }
    model = LSTMTrackForecaster(**config)
    export_bundle(
        tmp_path / "bundle",
        model,
        scaler,
        version="test-v1",
        dataset_version="synthetic-v1",
        dataset_sha256="a" * 64,
        model_config=config,
        input_len=4,
        horizons_hours=[6, 12, 24, 48, 72],
        validation_radius_km={str(h): float(h) for h in [6, 12, 24, 48, 72]},
        split_manifest={"seed": 42, "train": ["WP012024"], "val": [], "test": []},
        synthetic=True,
    )
    return tmp_path / "bundle", frame


def frame_to_fixes(frame: pd.DataFrame) -> list[Fix]:
    return [
        Fix(
            timestamp=row.timestamp,
            lat=row.lat,
            lon=row.lon,
            wind_ms=row.wind_ms,
            pressure_hpa=row.pressure_hpa,
            intensity=row.intensity,
            source="synthetic-demo",
        )
        for row in frame.itertuples()
    ]


def test_bundle_round_trip_and_horizon_mapping(tmp_path) -> None:
    root, frame = make_bundle(tmp_path)
    bundle = load_bundle(root)
    coords, classes = predict_bundle(
        bundle, frame_to_fixes(frame.iloc[:8]), [6, 24, 72]
    )
    assert len(coords) == len(classes) == 3
    assert bundle["manifest"]["synthetic"] is True
    assert bundle["scaler"].feature_columns == list(FEATURE_COLUMNS)


def test_corrupt_payload_and_schema_mismatch_fail_closed(tmp_path) -> None:
    root, _ = make_bundle(tmp_path)
    with (root / "weights.pt").open("ab") as handle:
        handle.write(b"corrupt")
    with pytest.raises(ValueError, match="checksum mismatch"):
        load_bundle(root)

    root, _ = make_bundle(tmp_path / "other")
    manifest_path = root / "manifest.json"
    manifest = __import__("json").loads(manifest_path.read_text())
    manifest["feature_columns"] = list(reversed(manifest["feature_columns"]))
    manifest_path.write_text(__import__("json").dumps(manifest))
    with pytest.raises(ValueError, match="feature columns mismatch"):
        load_bundle(root)


def test_predict_rejects_irregular_window(tmp_path) -> None:
    root, frame = make_bundle(tmp_path)
    fixes = frame_to_fixes(frame.iloc[:8])
    fixes[-2] = fixes[-2].model_copy(
        update={"timestamp": fixes[-2].timestamp + timedelta(hours=1)}
    )
    with pytest.raises(ValueError, match="regular"):
        predict_bundle(load_bundle(root), fixes, [6])
