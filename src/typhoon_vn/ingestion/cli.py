"""Explicit Phase 1 acquisition and parsing commands."""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from typhoon_vn.ingestion.errors import IngestionError
from typhoon_vn.ingestion.ingest import parse_and_store
from typhoon_vn.ingestion.providers.cma import CMAProvider
from typhoon_vn.ingestion.providers.environment import download_gfs, download_oisst
from typhoon_vn.ingestion.providers.geospatial import (
    download_gadm_vietnam,
    download_gshhg,
)
from typhoon_vn.ingestion.providers.ibtracs import IBTrACSProvider
from typhoon_vn.ingestion.providers.jma import JMAProvider
from typhoon_vn.ingestion.providers.jtwc import download_manifest


def build_parser() -> argparse.ArgumentParser:
    """Construct a no-surprise interface for fetching and parsing raw sources."""

    parser = argparse.ArgumentParser(prog="typhoon-vn-ingestion")
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    commands = parser.add_subparsers(dest="command", required=True)
    fetch = commands.add_parser("fetch", help="download a raw source with lineage")
    fetch_sources = fetch.add_subparsers(dest="source", required=True)

    cma = fetch_sources.add_parser("cma", help="CMA annual best-track files")
    cma.add_argument("--start-year", type=int, default=1949)
    cma.add_argument("--end-year", type=int, default=datetime.now(timezone.utc).year)
    fetch_sources.add_parser("ibtracs", help="NOAA IBTrACS WP CSV")
    fetch_sources.add_parser("jma", help="JMA all-years best-track archive")
    jtwc = fetch_sources.add_parser("jtwc", help="URLs listed in an approved manifest")
    jtwc.add_argument("--manifest", type=Path, required=True)
    fetch_sources.add_parser("gadm", help="GADM Vietnam level-1 boundaries")
    gshhg = fetch_sources.add_parser("gshhg", help="approved GSHHG release URL")
    gshhg.add_argument("--url")
    oisst = fetch_sources.add_parser("oisst", help="NOAA OISST daily NetCDF")
    oisst.add_argument("--date", type=_iso_date, required=True)
    gfs = fetch_sources.add_parser("gfs", help="optional NCEP GFS GRIB2")
    gfs.add_argument("--date", type=_iso_date, required=True)
    gfs.add_argument("--cycle", choices=("00", "06", "12", "18"), default="00")
    gfs.add_argument("--lead-hour", type=int, default=0)

    parse = commands.add_parser("parse", help="parse one verified raw object")
    parse.add_argument(
        "source",
        choices=("cma", "ibtracs", "jma", "jtwc", "nchmf", "pctt"),
    )
    parse.add_argument("--input", type=Path, required=True)
    parse.add_argument("--source-url", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Perform one declared action and return a shell-friendly status code."""

    args = build_parser().parse_args(argv)
    try:
        paths = _dispatch(args)
    except IngestionError as error:
        print(f"ingestion error: {error}", file=sys.stderr)
        return 2
    for path in paths:
        print(path)
    return 0


def _dispatch(args: argparse.Namespace) -> list[str]:
    if args.command == "parse":
        return [
            str(path)
            for path in parse_and_store(
                args.source,
                input_path=args.input,
                source_url=args.source_url,
                data_root=args.data_root,
            )
        ]
    if args.command != "fetch":
        raise IngestionError(f"unsupported command: {args.command}")
    if args.source == "cma":
        if args.start_year > args.end_year:
            raise IngestionError("--start-year must not be later than --end-year")
        return [
            item.local_path
            for item in CMAProvider().download_years(
                range(args.start_year, args.end_year + 1),
                data_root=args.data_root,
            )
        ]
    if args.source == "ibtracs":
        return [str(IBTrACSProvider().download(data_root=args.data_root).local_path)]
    if args.source == "jma":
        return [str(JMAProvider().download(data_root=args.data_root).local_path)]
    if args.source == "jtwc":
        return [
            item.local_path
            for item in download_manifest(args.manifest, data_root=args.data_root)
        ]
    if args.source == "gadm":
        return [str(download_gadm_vietnam(data_root=args.data_root).local_path)]
    if args.source == "gshhg":
        return [str(download_gshhg(data_root=args.data_root, url=args.url).local_path)]
    if args.source == "oisst":
        return [str(download_oisst(args.date, data_root=args.data_root).local_path)]
    if args.source == "gfs":
        return [
            str(
                download_gfs(
                    args.date,
                    data_root=args.data_root,
                    cycle=args.cycle,
                    lead_hour=args.lead_hour,
                ).local_path
            )
        ]
    raise IngestionError(f"unsupported source: {args.source}")


def _iso_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from error


if __name__ == "__main__":
    raise SystemExit(main())
