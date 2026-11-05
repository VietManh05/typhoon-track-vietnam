"""Export hindcasts of real storms that affected Vietnam as static JSON.

For each 2021-2024 test storm passing within ``--vn-km`` of Vietnam's coast,
pick the issue time whose +72 h position is closest to the coast, run the
*served* forecaster (trained LSTM bundle + k-NN analog library) on the fixes
observed up to that time, and attach the observed best track afterwards.
Neither model saw these storms in training (year split).

Output (``StormTrackResponse`` shape used by the Pages app):

* ``<out>/index.json`` — list of hindcast storms
* ``<out>/<HC-storm>.json`` — observations, forecast (+ suggestion),
  ``actual_track`` and per-horizon errors

Usage::

    python scripts/export_hindcast.py --data-root data \
        --bundle runs/ibtracs-benchmark/bundle \
        --analog runs/analog/analog-wp.npz \
        --out viz/frontend/public/data/hindcast
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from typhoon_vn.api.schemas import Fix, ForecastRequest
from typhoon_vn.datasets.ibtracs import load_ibtracs_tracks
from typhoon_vn.datasets.typhoon_dataset import split_by_storm_or_year
from typhoon_vn.evaluation.comparison import vietnam_storms
from typhoon_vn.features import constants as C
from typhoon_vn.features.geo import haversine_km
from typhoon_vn.inference.service import TyphoonForecaster

HORIZONS = [6, 12, 24, 48, 72]
SOURCE = "IBTrACS v04r01 best track (hindcast)"
STALE = "Observations are older than 24 hours"


def _coast_distance_km(lat: float, lon: float) -> float:
    return min(haversine_km(lat, lon, clat, clon) for clat, clon in C.VN_COASTLINE)


def choose_issue(track: pd.DataFrame, input_len: int = 4) -> int | None:
    """Index of the issue time whose +72 h fix is closest to Vietnam."""

    times = list(pd.to_datetime(track["timestamp"], utc=True))
    index = {t: i for i, t in enumerate(times)}
    six = pd.Timedelta(hours=6)
    best, best_distance = None, np.inf
    for i in range(input_len - 1, len(times)):
        window = times[i - input_len + 1 : i + 1]
        if any(b - a != six for a, b in zip(window, window[1:])):
            continue
        targets = [index.get(times[i] + pd.Timedelta(hours=h)) for h in HORIZONS]
        if any(t is None for t in targets):
            continue
        row = track.iloc[targets[-1]]
        distance = _coast_distance_km(float(row.lat), float(row.lon))
        if distance < best_distance:
            best, best_distance = i, distance
    return best


def _fix(row) -> Fix:
    return Fix(
        timestamp=pd.Timestamp(row.timestamp).to_pydatetime(),
        lat=float(row.lat),
        lon=float(row.lon),
        wind_ms=None if pd.isna(row.wind_ms) else round(float(row.wind_ms), 1),
        pressure_hpa=None if pd.isna(row.pressure_hpa) else float(row.pressure_hpa),
        intensity="UNK",
        source=SOURCE,
    )


def hindcast_record(
    storm_id: str, name: str, track: pd.DataFrame, forecaster: TyphoonForecaster
) -> dict | None:
    track = track.sort_values("timestamp").reset_index(drop=True)
    issue_index = choose_issue(track)
    if issue_index is None:
        return None
    fixes = [_fix(row) for row in track.iloc[: issue_index + 1].itertuples()]
    hc_id = f"HC-{storm_id}"
    forecast = forecaster.forecast(
        ForecastRequest(storm_id=hc_id, observations=fixes[-512:], horizons=HORIZONS)
    )
    issue = fixes[-1].timestamp
    warnings = [w for w in forecast.warnings if w != STALE]
    warnings.insert(
        0,
        "Hindcast (dự báo lại) trên bão đã qua; mô hình chưa thấy bão này khi huấn "
        "luyện. Không phải bão đang hoạt động.",
    )
    forecast = forecast.model_copy(update={"warnings": warnings})

    by_time = {pd.Timestamp(t): i for i, t in enumerate(track["timestamp"])}
    actual = []
    for h in HORIZONS:
        row = track.iloc[by_time[pd.Timestamp(issue) + pd.Timedelta(hours=h)]]
        actual.append(
            {
                "horizon_hours": h,
                "valid_time": (pd.Timestamp(issue) + pd.Timedelta(hours=h)).isoformat(),
                "lat": float(row.lat),
                "lon": float(row.lon),
                "wind_ms": (
                    None if pd.isna(row.wind_ms) else round(float(row.wind_ms), 1)
                ),
                "pressure_hpa": (
                    None if pd.isna(row.pressure_hpa) else float(row.pressure_hpa)
                ),
                "source": "IBTrACS v04r01 best track",
            }
        )

    def errors(points) -> dict[str, float]:
        return {
            str(p.horizon_hours): round(
                haversine_km(p.lat, p.lon, a["lat"], a["lon"]), 1
            )
            for p, a in zip(points, actual)
        }

    payload = json.loads(forecast.model_dump_json())
    return {
        "storm_id": hc_id,
        "observations": [json.loads(f.model_dump_json()) for f in fixes],
        "forecast": payload,
        "actual_track": actual,
        "hindcast": {
            "best_track_id": storm_id,
            "name": name,
            "issue_time": issue.isoformat(),
            "errors_km": {
                "model": errors(forecast.points),
                "analog": (
                    errors(forecast.suggestion.points) if forecast.suggestion else None
                ),
            },
            "inside_cone": {
                str(p.horizon_hours): haversine_km(p.lat, p.lon, a["lat"], a["lon"])
                <= p.radius_km
                for p, a in zip(forecast.points, actual)
            },
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--analog", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--years", type=int, nargs=2, default=(1980, 2024))
    parser.add_argument("--vn-km", type=float, default=300.0)
    args = parser.parse_args(argv)

    raw, cleaned, _ = load_ibtracs_tracks(args.data_root, tuple(args.years))
    _, _, test = split_by_storm_or_year(
        cleaned, val_ratio=0.1, test_ratio=0.1, by_year=True
    )
    names = (
        raw.dropna(subset=["storm_name"])
        .drop_duplicates("storm_id")
        .set_index("storm_id")["storm_name"]
        .astype(str)
    )
    forecaster = TyphoonForecaster(
        args.bundle, allow_baseline=False, analog_artifact=args.analog
    )
    args.out.mkdir(parents=True, exist_ok=True)
    for old in args.out.glob("HC-*.json"):
        old.unlink()

    items = []
    for storm_id in sorted(vietnam_storms(test, within_km=args.vn_km)):
        name = names.get(storm_id, storm_id).title()
        record = hindcast_record(
            storm_id, name, test[test.storm_id == storm_id], forecaster
        )
        if record is None:
            continue
        (args.out / f"{record['storm_id']}.json").write_text(
            json.dumps(record, ensure_ascii=False), encoding="utf-8"
        )
        latest = record["observations"][-1]
        items.append(
            {
                "id": record["storm_id"],
                "name": name,
                "name_vi": f"{name} ({storm_id[-4:]}) – dự báo lại",
                "year": int(storm_id[-4:]),
                "latest": latest,
                "observation_count": len(record["observations"]),
                "status": "dissipated",
                "hindcast": record["hindcast"],
            }
        )
    items.sort(key=lambda item: item["hindcast"]["issue_time"], reverse=True)
    model = [r["hindcast"]["errors_km"]["model"]["72"] for r in items]
    index = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model_version": forecaster.version,
        "dataset_version": forecaster.dataset,
        "analog_version": forecaster.analog.version if forecaster.analog else None,
        "description": (
            "Hindcasts of 2021-2024 storms that passed within "
            f"{args.vn_km:.0f} km of Vietnam; models trained on 1980-2016 "
            "(analog library 1980-2020)."
        ),
        "mean_72h_error_km": round(float(np.mean(model)), 1) if model else None,
        "typhoons": items,
    }
    (args.out / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"wrote {len(items)} hindcasts to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
