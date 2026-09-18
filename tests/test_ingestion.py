import unittest
from datetime import date, datetime, timezone

from typhoon_vn.ingestion.identifiers import canonical_storm_id
from typhoon_vn.ingestion.merge_sources import merge_observations
from typhoon_vn.ingestion.models import Observation
from typhoon_vn.ingestion.providers.cma import parse_cma_text
from typhoon_vn.ingestion.providers.environment import (
    Era5PressureLevelRequest,
    gfs_url,
    oisst_url,
)
from typhoon_vn.ingestion.providers.ibtracs import parse_ibtracs_csv
from typhoon_vn.ingestion.providers.jma import parse_jma_text
from typhoon_vn.ingestion.providers.jtwc import parse_jtwc_atcf
from typhoon_vn.ingestion.schedule import should_run_weekly, update_cadence


class IdentifierTests(unittest.TestCase):
    def test_normalises_jma_and_atcf_ids(self) -> None:
        self.assertEqual(canonical_storm_id("2401"), "WP012024")
        self.assertEqual(canonical_storm_id("WP012024"), "WP012024")


class ProviderParserTests(unittest.TestCase):
    def test_parses_cma_records(self) -> None:
        records = parse_cma_text(
            "66666 2024 2401 1\n2024070100 3 100 1200 990 20\n",
            source_url="https://example.test/cma.txt",
            checksum="a" * 64,
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].storm_id, "WP012024")
        self.assertEqual(records[0].wind_unit, "m/s")

    def test_parses_jma_records(self) -> None:
        records = parse_jma_text(
            "66666 2401  001 0001 2401 0 6 NAME 20240101\n"
            "24010100 002 3 100 1300 990 035\n",
            source_url="https://example.test/jma.txt",
            checksum="b" * 64,
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].storm_id, "WP012024")
        self.assertEqual(records[0].longitude, 130.0)

    def test_parses_jtwc_atcf_records(self) -> None:
        records = parse_jtwc_atcf(
            "WP, 01, 2024070100, BEST, 0, , 100N, 1200E, 35, 990, TS\n",
            source_url="https://example.test/jtwc.dat",
            checksum="c" * 64,
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].latitude, 10.0)
        self.assertEqual(records[0].wind, 35.0)

    def test_parses_ibtracs_records(self) -> None:
        records = parse_ibtracs_csv(
            "SID,BASIN,ISO_TIME,LAT,LON,USA_ATCF_ID,USA_WIND,USA_PRES,NAME\n"
            "2024TEST,WP,2024-07-01 00:00:00,10,120,WP012024,35,990,TEST\n",
            source_url="https://example.test/ibtracs.csv",
            checksum="d" * 64,
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].storm_id, "WP012024")


class MergeTests(unittest.TestCase):
    def test_selects_ibtracs_and_retains_conflict(self) -> None:
        timestamp = datetime(2024, 7, 1, tzinfo=timezone.utc)
        shared = {
            "storm_id": "WP012024",
            "timestamp": timestamp,
            "latitude": 10.0,
            "longitude": 120.0,
            "source_url": "https://example.test",
            "source_file_checksum": "e" * 64,
        }
        records = [
            Observation(source="cma", source_storm_id="2401", wind=20, **shared),
            Observation(source="ibtracs", source_storm_id="test", wind=35, **shared),
        ]
        merged = merge_observations(records)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0].source, "ibtracs")
        self.assertEqual(set(merged[0].contributing_sources), {"cma", "ibtracs"})


class EnvironmentAndScheduleTests(unittest.TestCase):
    def test_builds_environment_urls_and_cadence(self) -> None:
        self.assertIn("202409", oisst_url(date(2024, 9, 1)))
        self.assertIn("f006", gfs_url(date(2024, 9, 1), lead_hour=6))
        self.assertEqual(update_cadence(date(2024, 9, 1)), "daily")
        self.assertTrue(should_run_weekly(date(2024, 1, 1)))


    def test_builds_era5_pressure_level_request(self) -> None:
        request = Era5PressureLevelRequest(
            years=("2024",),
            months=("09",),
            days=("01",),
            hours=("00:00",),
        )

        payload = request.as_cds_request()

        self.assertEqual(payload["pressure_level"], ["850", "200"])
        self.assertIn("relative_humidity", payload["variable"])

if __name__ == "__main__":
    unittest.main()
