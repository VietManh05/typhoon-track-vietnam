"""Acquisition adapters for OISST, ERA5, and optional GFS fields."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from typhoon_vn.ingestion.errors import OptionalDependencyError
from typhoon_vn.ingestion.http import HttpDownloader
from typhoon_vn.ingestion.lineage import write_download_lineage
from typhoon_vn.ingestion.models import DownloadResult

DEFAULT_OISST_BASE_URL = (
    "https://www.ncei.noaa.gov/data/sea-surface-temperature-optimum-"
    "interpolation/v2.1/access/avhrr"
)
DEFAULT_GFS_BASE_URL = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod"


def oisst_url(observation_date: date, base_url: str | None = None) -> str:
    """Return the official OISST v2.1 daily NetCDF URL for one UTC date."""

    root = (base_url or os.getenv("OISST_BASE_URL") or DEFAULT_OISST_BASE_URL).rstrip(
        "/"
    )
    month = observation_date.strftime("%Y%m")
    stamp = observation_date.strftime("%Y%m%d")
    return f"{root}/{month}/oisst-avhrr-v02r01.{stamp}.nc"


def download_oisst(
    observation_date: date,
    *,
    data_root: Path,
    downloader: HttpDownloader | None = None,
) -> DownloadResult:
    """Download and record one daily OISST field for cacheable sampling."""

    url = oisst_url(observation_date)
    result = (downloader or HttpDownloader()).fetch(
        source="oisst",
        url=url,
        destination=(
            data_root
            / "raw"
            / "environment"
            / "oisst"
            / str(observation_date.year)
            / f"oisst-{observation_date:%Y%m%d}.nc"
        ),
    )
    write_download_lineage(
        result,
        data_root=data_root,
        dataset_version="NOAA OISST v2.1",
        parser="NetCDF retained raw; sampling is a later feature step.",
        licence_note="NOAA OISST v2.1; cite DOI 10.25921/RE9P-PT57.",
    )
    return result


@dataclass(frozen=True, slots=True)
class Era5Request:
    """A bounded ERA5 single-level request for track-aligned source fields."""

    years: tuple[str, ...]
    months: tuple[str, ...]
    days: tuple[str, ...]
    hours: tuple[str, ...]
    area: tuple[float, float, float, float] = (35.0, 95.0, -5.0, 145.0)
    variables: tuple[str, ...] = (
        "mean_sea_level_pressure",
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
    )

    def as_cds_request(self) -> dict[str, object]:
        """Return a CDS request without embedding credentials."""

        north, west, south, east = self.area
        return {
            "product_type": "reanalysis",
            "variable": list(self.variables),
            "year": list(self.years),
            "month": list(self.months),
            "day": list(self.days),
            "time": list(self.hours),
            "area": [north, west, south, east],
            "format": "netcdf",
        }


def retrieve_era5(request: Era5Request, *, destination: Path) -> Path:
    """Retrieve ERA5 after the operator configures a valid CDS API account."""

    try:
        import cdsapi
    except ImportError as error:
        raise OptionalDependencyError(
            'ERA5 retrieval requires: python -m pip install -e ".[ingestion]"'
        ) from error
    destination.parent.mkdir(parents=True, exist_ok=True)
    client = cdsapi.Client()
    client.retrieve(
        "reanalysis-era5-single-levels",
        request.as_cds_request(),
        str(destination),
    )
    return destination


@dataclass(frozen=True, slots=True)
class Era5PressureLevelRequest:
    """Bounded ERA5 request for 850/200 hPa winds and relative humidity."""

    years: tuple[str, ...]
    months: tuple[str, ...]
    days: tuple[str, ...]
    hours: tuple[str, ...]
    area: tuple[float, float, float, float] = (35.0, 95.0, -5.0, 145.0)
    pressure_levels: tuple[str, ...] = ("850", "200")
    variables: tuple[str, ...] = (
        "u_component_of_wind",
        "v_component_of_wind",
        "relative_humidity",
    )

    def as_cds_request(self) -> dict[str, object]:
        """Return a pressure-level CDS request without a credential."""

        north, west, south, east = self.area
        return {
            "product_type": "reanalysis",
            "variable": list(self.variables),
            "pressure_level": list(self.pressure_levels),
            "year": list(self.years),
            "month": list(self.months),
            "day": list(self.days),
            "time": list(self.hours),
            "area": [north, west, south, east],
            "format": "netcdf",
        }


def retrieve_era5_pressure_levels(
    request: Era5PressureLevelRequest, *, destination: Path
) -> Path:
    """Retrieve 850/200 hPa fields after configuring a CDS API account."""

    try:
        import cdsapi
    except ImportError as error:
        raise OptionalDependencyError(
            'ERA5 retrieval requires: python -m pip install -e ".[ingestion]"'
        ) from error
    destination.parent.mkdir(parents=True, exist_ok=True)
    client = cdsapi.Client()
    client.retrieve(
        "reanalysis-era5-pressure-levels",
        request.as_cds_request(),
        str(destination),
    )
    return destination

def gfs_url(
    run_date: date,
    *,
    cycle: str = "00",
    lead_hour: int = 0,
    base_url: str | None = None,
) -> str:
    """Build the documented NOMADS GFS 0.25-degree file URL."""

    root = (base_url or os.getenv("GFS_BASE_URL") or DEFAULT_GFS_BASE_URL).rstrip("/")
    stamp = run_date.strftime("%Y%m%d")
    return (
        f"{root}/gfs.{stamp}/{cycle}/atmos/gfs.t{cycle}z.pgrb2.0p25."
        f"f{lead_hour:03d}"
    )


def download_gfs(
    run_date: date,
    *,
    data_root: Path,
    cycle: str = "00",
    lead_hour: int = 0,
    downloader: HttpDownloader | None = None,
) -> DownloadResult:
    """Download one optional GFS field, preserving run and lead provenance."""

    url = gfs_url(run_date, cycle=cycle, lead_hour=lead_hour)
    result = (downloader or HttpDownloader()).fetch(
        source="gfs",
        url=url,
        destination=(
            data_root
            / "raw"
            / "environment"
            / "gfs"
            / run_date.strftime("%Y%m%d")
            / f"gfs-t{cycle}z-f{lead_hour:03d}.grib2"
        ),
    )
    write_download_lineage(
        result,
        data_root=data_root,
        dataset_version="NCEP GFS 0.25-degree",
        parser="GRIB2 retained raw; sampling is a later feature step.",
        licence_note="NCEP NOMADS GFS operational output.",
    )
    return result
