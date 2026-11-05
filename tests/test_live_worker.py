"""G19: live IBTrACS ACTIVE source feeding the update worker."""

from datetime import datetime, timedelta, timezone

import pytest

from typhoon_vn.api.schemas import ObservationBatch
from typhoon_vn.cli import main
from typhoon_vn.inference.service import TyphoonForecaster
from typhoon_vn.operations.live import batches_from_ibtracs_csv
from typhoon_vn.operations.store import Store
from typhoon_vn.operations.worker import run_worker

HEADER = (
    "SID,SEASON,NUMBER,BASIN,SUBBASIN,NAME,ISO_TIME,NATURE,LAT,LON,"
    "WMO_WIND,WMO_PRES,WMO_AGENCY,TRACK_TYPE,DIST2LAND,LANDFALL,IFLAG,"
    "USA_AGENCY,USA_ATCF_ID,USA_LAT,USA_LON,USA_RECORD,USA_SSHS,USA_WIND,USA_PRES"
)
UNITS = " ,Year, , , , , , ,degrees_north,degrees_east,kts,mb, , ,km,km, , , , , , , ,kts,mb"


def _csv(start: datetime, *, hours=(0, 3, 6, 12, 18), lon0=125.0) -> str:
    rows = [HEADER, UNITS]
    for index, hour in enumerate(hours):
        when = start + timedelta(hours=hour)
        rows.append(
            f"2026300N15125,2026,40,WP,MM,TESTSTORM,{when:%Y-%m-%d %H:%M:%S},TS,"
            f"{15 + 0.3 * index:.1f},{lon0 - 0.5 * index:.1f},,,,main,500,500,,"
            f"jtwc_wp,WP402026,,,,1,{45 + index},{990 - index}"
        )
    # A storm in another basin must be ignored.
    rows.append(
        f"2026300N15265,2026,41,EP,MM,OTHER,{start:%Y-%m-%d %H:%M:%S},TS,"
        "15.0,-95.0,,,,main,500,500,,jtwc_ep,EP412026,,,,1,40,995"
    )
    return "\n".join(rows) + "\n"


def test_active_csv_becomes_six_hourly_batches_with_physical_units() -> None:
    start = datetime(2026, 11, 3, 0, tzinfo=timezone.utc)
    batches = batches_from_ibtracs_csv(
        _csv(start), source_url="https://example.invalid/active.csv", checksum="a" * 64
    )
    assert len(batches) == 1
    batch = batches[0]
    assert batch.storm_id == "WP402026"
    assert batch.name == "TESTSTORM"
    times = [fix.timestamp for fix in batch.observations]
    assert all(t.hour % 6 == 0 for t in times), "3-hourly interpolated rows dropped"
    assert times == sorted(times) and len(times) == 4
    first = batch.observations[0]
    assert first.source == "ibtracs-active"
    assert first.source_url == "https://example.invalid/active.csv"
    assert first.wind_ms == pytest.approx(45 * 0.514444, rel=1e-3)  # knots -> m/s
    assert first.pressure_hpa == 990


def test_storms_outside_the_model_domain_are_dropped() -> None:
    start = datetime(2026, 11, 3, 0, tzinfo=timezone.utc)
    batches = batches_from_ibtracs_csv(
        _csv(start, lon0=170.0), source_url="u", checksum="a" * 64
    )
    assert batches == []


def test_worker_stores_live_batches_and_forecasts(tmp_path) -> None:
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    start = now - timedelta(hours=now.hour % 6) - timedelta(hours=18)
    batches = batches_from_ibtracs_csv(_csv(start), source_url="u", checksum="a" * 64)
    store = Store(f"sqlite:///{tmp_path / 'live.db'}")
    run_worker(store, TyphoonForecaster(), source=lambda: batches, once=True)
    old = ObservationBatch(
        storm_id="OLD", name="OLD", observations=store.track("WP402026")[:2]
    )
    store.upsert_observations(
        old.model_copy(
            update={
                "observations": [
                    f.model_copy(update={"timestamp": f.timestamp - timedelta(days=5)})
                    for f in old.observations
                ]
            }
        )
    )
    active = store.active()
    assert [entry["id"] for entry in active] == ["WP402026"]
    assert active[0]["observation_count"] == 4
    assert active[0]["latest"] == store.track("WP402026")[-1].model_dump(mode="json")
    assert len(store.track("WP402026")) == 4


def test_worker_cli_requires_exactly_one_source(tmp_path, capsys) -> None:
    with pytest.raises(SystemExit):
        main(["worker", "--once"])
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text("[]", encoding="utf-8")
    db = f"sqlite:///{tmp_path / 'cli.db'}"
    assert main(["worker", "--once", "--snapshot", str(snapshot), "--db", db]) == 0
