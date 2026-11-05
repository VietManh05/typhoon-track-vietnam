"""Download NCEP/NCAR Reanalysis 1 steering fields (free, no account).

Subsets 6-hourly u/v wind and geopotential height at 850/500/200 hPa over the
Western Pacific from NOAA PSL THREDDS via OPeNDAP, one compact ``.npz`` per
variable and year (float32). Kalnay et al. (1996); data: NOAA PSL,
https://psl.noaa.gov/data/gridded/data.ncep.reanalysis.html

Usage::

    python scripts/download_ncep_steering.py --out data/external/ncep_r1 \
        --years 1980 2024 --workers 4
"""

from __future__ import annotations

import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import xarray as xr

BASE = "https://psl.noaa.gov/thredds/dodsC/Datasets/ncep.reanalysis/pressure/"
VARIABLES = ("uwnd", "vwnd", "hgt")
LEVELS = [850, 500, 200]
LAT = slice(62.5, -10.0)  # descending; 800 km ring + 5 deg ridge offset past 0-50N
LON = slice(92.5, 182.5)


def fetch(variable: str, year: int, out: Path, retries: int = 4) -> str:
    target = out / f"{variable}.{year}.npz"
    if target.exists():
        return f"skip {target.name}"
    for attempt in range(1, retries + 1):
        try:
            with xr.open_dataset(f"{BASE}{variable}.{year}.nc") as ds:
                sub = ds[variable].sel(level=LEVELS, lat=LAT, lon=LON)
                blocks = [
                    sub.isel(time=slice(i, i + 366)).values.astype(np.float32)
                    for i in range(0, sub.sizes["time"], 366)
                ]
                times = sub["time"].values.astype("datetime64[s]").astype(np.int64)
                temporary = target.with_suffix(".tmp.npz")
                np.savez_compressed(
                    temporary,
                    data=np.concatenate(blocks, axis=0),
                    time=times,
                    level=np.asarray(LEVELS, dtype=np.int16),
                    lat=sub["lat"].values.astype(np.float32),
                    lon=sub["lon"].values.astype(np.float32),
                )
                temporary.replace(target)
            return f"ok {target.name}"
        except Exception as error:  # network hiccups: retry with backoff
            if attempt == retries:
                return f"FAILED {target.name}: {error}"
            time.sleep(10 * attempt)
    return f"FAILED {target.name}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--years", type=int, nargs=2, default=(1980, 2024))
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    jobs = [(v, y) for y in range(args.years[0], args.years[1] + 1) for v in VARIABLES]
    failed = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(fetch, v, y, args.out) for v, y in jobs]
        for done, future in enumerate(as_completed(futures), 1):
            message = future.result()
            failed += message.startswith("FAILED")
            print(f"[{done}/{len(jobs)}] {message}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
