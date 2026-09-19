"""End-to-end contracts for the G01-G06 Phase-2 data gate."""

from __future__ import annotations

import hashlib
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from typhoon_vn.datasets.synthetic import generate_synthetic_catalogue
from typhoon_vn.datasets.typhoon_dataset import (
    DatasetConfig,
    TyphoonDataset,
    save_split_manifest,
    split_by_storm_or_year,
    split_manifest,
)
from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.features.dictionary import (
    FEATURE_SCHEMA_VERSION,
    feature_dictionary,
    feature_schema_fingerprint,
)
from typhoon_vn.features.environmental import (
    atmospheric_features,
    sample_grid_point,
    sst_features,
)
from typhoon_vn.features.geospatial import (
    SPECIAL_LOCATIONS,
    ProvinceBoundary,
    ProvinceIndex,
    distance_to_coast_km,
    normalise_province_name,
    point_in_polygon,
    require_wgs84,
    simplify_polyline,
)
from typhoon_vn.features.pipeline import Phase2Pipeline
from typhoon_vn.features.store import (
    SchemaDriftError,
    check_schema_drift,
    load_feature_table,
    save_feature_table,
)
from typhoon_vn.ingestion.errors import DownloadError
from typhoon_vn.ingestion.http import DownloadPolicy, HttpDownloader
from typhoon_vn.ingestion.providers.vietnam import ProvinceAlias, parse_impact_csv


class FakeResponse:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload
        self.headers = {"ETag": '"fixture"', "Last-Modified": "fixture-time"}
        self._read = False

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, _size: int) -> bytes:
        if self._read:
            return b""
        self._read = True
        return self.payload


def test_http_download_success_checksum_empty_404_and_429_retry(
    tmp_path: Path, monkeypatch
) -> None:
    from typhoon_vn.ingestion import http

    payload = b"deterministic raw fixture"
    monkeypatch.setattr(http, "urlopen", lambda *_a, **_k: FakeResponse(payload))
    destination = tmp_path / "raw" / "fixture.bin"
    result = HttpDownloader(DownloadPolicy(attempts=2, backoff_seconds=0)).fetch(
        source="fixture", url="https://example.test/raw", destination=destination
    )
    assert destination.read_bytes() == payload
    assert result.sha256 == hashlib.sha256(payload).hexdigest()
    assert result.bytes_written == len(payload)
    assert not list(tmp_path.rglob("*.part"))

    monkeypatch.setattr(http, "urlopen", lambda *_a, **_k: FakeResponse(b""))
    with pytest.raises(DownloadError, match="empty response"):
        HttpDownloader(DownloadPolicy(attempts=1)).fetch(
            source="fixture",
            url="https://example.test/empty",
            destination=tmp_path / "empty.bin",
        )

    calls = []

    def not_found(*_args, **_kwargs):
        calls.append("404")
        raise HTTPError("https://example.test/404", 404, "missing", {}, None)

    monkeypatch.setattr(http, "urlopen", not_found)
    with pytest.raises(DownloadError):
        HttpDownloader(DownloadPolicy(attempts=4, backoff_seconds=0)).fetch(
            source="fixture",
            url="https://example.test/404",
            destination=tmp_path / "404.bin",
        )
    assert calls == ["404"]

    timeout_calls = 0

    def timed_out(*_args, **_kwargs):
        nonlocal timeout_calls
        timeout_calls += 1
        raise TimeoutError("fixture timeout")

    monkeypatch.setattr(http, "urlopen", timed_out)
    monkeypatch.setattr(http.time, "sleep", lambda _seconds: None)
    with pytest.raises(DownloadError, match="fixture timeout"):
        HttpDownloader(DownloadPolicy(attempts=2, backoff_seconds=0)).fetch(
            source="fixture",
            url="https://example.test/timeout",
            destination=tmp_path / "timeout.bin",
        )
    assert timeout_calls == 2

    attempts = 0

    def throttled(*_args, **_kwargs):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise HTTPError("https://example.test/429", 429, "slow", {}, None)
        return FakeResponse(payload)

    monkeypatch.setattr(http, "urlopen", throttled)
    monkeypatch.setattr(http.time, "sleep", lambda _seconds: None)
    HttpDownloader(DownloadPolicy(attempts=2, backoff_seconds=0)).fetch(
        source="fixture",
        url="https://example.test/429",
        destination=tmp_path / "429.bin",
    )
    assert attempts == 2


def test_geospatial_crs_index_coastline_and_locations() -> None:
    assert require_wgs84("EPSG:4326") == "EPSG:4326"
    with pytest.raises(ValueError, match="WGS84"):
        require_wgs84("EPSG:3857")
    polygon = ((106.0, 15.0), (108.0, 15.0), (108.0, 17.0), (106.0, 17.0))
    boundary = ProvinceBoundary("VN-DN", "Đà Nẵng", polygon)
    index = ProvinceIndex([boundary])
    assert point_in_polygon((107.0, 16.0), polygon)
    assert index.containing((107.0, 16.0)) == boundary
    nearest, distance = index.nearest((109.0, 16.0))
    assert nearest == boundary and distance > 0
    assert distance_to_coast_km((107.0, 16.0), [(106.0, 15.0), (108.0, 17.0)]) < 1
    assert simplify_polyline([(0, 0), (1, 0.01), (2, 0)], 0.02) == [(0, 0), (2, 0)]
    assert normalise_province_name("Đà Nẵng") == "da-nang"
    assert len({item.location_id for item in SPECIAL_LOCATIONS}) == len(
        SPECIAL_LOCATIONS
    )
    assert all(
        item.distance_km(item.latitude, item.longitude) == 0
        for item in SPECIAL_LOCATIONS
    )


def _raw_track() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "storm_id": ["WP012024"] * 5,
            "timestamp": pd.date_range("2024-07-01", periods=5, freq="6h", tz="UTC"),
            "latitude": [10.0, 10.5, 11.0, 11.5, 12.0],
            "longitude": [120.0, 120.5, 121.0, 121.5, 122.0],
            "wind": [30.0, np.nan, 40.0, 45.0, 50.0],
            "wind_unit": ["kt"] * 5,
            "pressure_hpa": [995.0, 990.0, 985.0, 980.0, 975.0],
            "intensity_code": ["2", "3", "3", "4", "5"],
            "source": ["jma"] * 5,
            "source_url": ["https://example.test/jma"] * 5,
            "source_file_checksum": ["a" * 64] * 5,
        }
    )


def test_phase2_pipeline_interpolates_flags_features_and_exports(
    tmp_path: Path,
) -> None:
    pipeline = Phase2Pipeline()
    featured, report = pipeline.run([_raw_track()])
    assert report.n_input == 5 and report.n_output == 5
    assert report.n_interpolated == 1
    assert featured.loc[1, "interpolated"]
    assert set(FEATURE_COLUMNS).issubset(featured.columns)
    destination = pipeline.export(featured, report, tmp_path / "clean.parquet")
    assert pd.read_parquet(destination).shape == featured.shape
    assert destination.with_suffix(".quality.json").exists()


def _grid() -> xr.Dataset:
    times = pd.to_datetime(["2024-07-01T00:00Z", "2024-07-01T06:00Z"])
    coords = {
        "time": times.tz_localize(None),
        "lat": [9.0, 10.0, 11.0],
        "lon": [119.0, 120.0, 121.0],
    }
    base = np.arange(18, dtype=float).reshape(2, 3, 3)
    variables = {
        "sst": (("time", "lat", "lon"), 25.0 + base / 10),
        "mslp_hpa": (("time", "lat", "lon"), 990.0 + base),
        "u850_ms": (("time", "lat", "lon"), 1.0 + base * 0),
        "v850_ms": (("time", "lat", "lon"), 2.0 + base * 0),
        "u200_ms": (("time", "lat", "lon"), 4.0 + base * 0),
        "v200_ms": (("time", "lat", "lon"), 6.0 + base * 0),
        "humidity_pct": (("time", "lat", "lon"), 70.0 + base * 0),
    }
    return xr.Dataset(variables, coords=coords)


def test_environment_sampling_units_gradient_shear_and_availability() -> None:
    issue = datetime(2024, 7, 1, 7, tzinfo=timezone.utc)
    match = sample_grid_point(
        _grid(), variable="sst", issue_time=issue, latitude=10, longitude=120
    )
    assert match.valid_time == pd.Timestamp("2024-07-01T06:00Z")
    assert np.isfinite(
        sst_features(_grid(), issue_time=issue, latitude=10, longitude=120)[
            "sst_gradient_c_per_degree"
        ]
    )
    atmosphere = atmospheric_features(
        _grid(), issue_time=issue, latitude=10, longitude=120
    )
    assert atmosphere["wind_shear_ms"] == pytest.approx(5.0)
    with pytest.raises(ValueError, match="not available"):
        sample_grid_point(
            _grid(),
            variable="sst",
            issue_time=issue,
            available_at=issue + timedelta(hours=1),
            latitude=10,
            longitude=120,
        )


def test_feature_dictionary_and_versioned_store_reject_drift(tmp_path: Path) -> None:
    definitions = feature_dictionary()
    assert FEATURE_SCHEMA_VERSION and len(definitions) == len(FEATURE_COLUMNS)
    assert [item.name for item in definitions] == list(FEATURE_COLUMNS)
    assert len(feature_schema_fingerprint()) == 64
    frame = (
        FeatureBuilder()
        .feature_matrix(generate_synthetic_catalogue(n_storms=1, n_fixes=20, seed=9))
        .astype("float32")
    )
    save_feature_table(frame, tmp_path, "v1", {"dataset": "synthetic-fixture"})
    restored = load_feature_table(tmp_path, "v1")
    pd.testing.assert_frame_equal(restored, frame)
    assert check_schema_drift(frame[list(reversed(frame.columns))])
    changed = frame.copy()
    changed[FEATURE_COLUMNS[0]] = changed[FEATURE_COLUMNS[0]].astype("float64")
    manifest_columns = [
        {"name": name, "dtype": str(dtype)}
        for name, dtype in zip(frame.columns, frame.dtypes)
    ]
    assert any(
        "dtype" in issue
        for issue in check_schema_drift(
            changed, list(FEATURE_COLUMNS), manifest_columns
        )
    )
    changed.to_parquet(tmp_path / "v1" / "features.parquet", index=False)
    with pytest.raises(SchemaDriftError, match="dtype"):
        load_feature_table(tmp_path, "v1")


def test_window_horizons_split_manifest_and_no_leakage(tmp_path: Path) -> None:
    catalogue = generate_synthetic_catalogue(n_storms=20, n_fixes=30, seed=11)
    train, validation, test = split_by_storm_or_year(
        catalogue, val_ratio=0.2, test_ratio=0.2, random_seed=11
    )
    manifest = split_manifest(
        train, validation, test, policy="storm-id-random", seed=11
    )
    path = save_split_manifest(manifest, tmp_path / "split.json")
    assert path.exists()
    assert not set(manifest["train_ids"]) & set(manifest["test_ids"])
    config = DatasetConfig(input_len=6, horizon=(1, 2, 4, 8, 12))
    dataset = TyphoonDataset(train, config=config)
    assert dataset[0]["x"].dtype == np.float32
    assert dataset[0]["mask"].tolist() == [1.0] * 6
    assert dataset[0]["meta"]["horizons"] == [1, 2, 4, 8, 12]


def test_impact_labels_effective_mapping_deduplicate_and_conflicts(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "impact.csv"
    csv_path.write_text(
        "storm_id,province,impact_type,severity,event_time,reference\n"
        "WP012024,Da Nang,landfall,high,2024-07-01T00:00:00+0000,A\n"
        "WP012024,Da Nang,landfall,medium,2024-07-01T00:00:00+0000,B\n",
        encoding="utf-8",
    )
    aliases = [ProvinceAlias("Da Nang", "VN-DN", "Đà Nẵng", date(1997, 1, 1))]
    labels = parse_impact_csv(
        csv_path,
        source_url="https://example.test/authorised-export",
        checksum="b" * 64,
        aliases=aliases,
    )
    assert len(labels) == 1
    assert labels[0].province == "Đà Nẵng"
    assert labels[0].metadata["province_code"] == "VN-DN"
    assert labels[0].metadata["duplicate_count"] == 2
    assert labels[0].metadata["conflicts"][0]["severity"] == "medium"
    assert labels[0].source_file_checksum == "b" * 64
