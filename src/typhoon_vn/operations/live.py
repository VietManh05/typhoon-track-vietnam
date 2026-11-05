"""Near-real-time storm source: NOAA IBTrACS ACTIVE (public domain, keyless).

IBTrACS ACTIVE holds storms still in progress. NCEI refreshes it a few times a
week, so positions can lag by days: it is a free near-real-time feed, not an
operational bulletin. Rows go through the same canonical mapping and cleaning
used for training (knots -> m/s, model domain box, de-duplication) and only
synoptic 6-hourly fixes are kept, matching the model's input step.
"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import pandas as pd

from typhoon_vn.api.schemas import Fix, ObservationBatch
from typhoon_vn.features.bridge import to_canonical_frame
from typhoon_vn.features.cleaning import clean_tracks
from typhoon_vn.ingestion.http import HttpDownloader
from typhoon_vn.ingestion.lineage import write_download_lineage
from typhoon_vn.ingestion.providers.ibtracs import parse_ibtracs_csv

ACTIVE_URL = (
    "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-"
    "stewardship-ibtracs/v04r01/access/csv/ibtracs.ACTIVE.list.v04r01.csv"
)
SOURCE_LABEL = "ibtracs-active"
_INTENSITIES = {"TD", "TS", "STS", "TY", "STY", "SUPERTY"}


def batches_from_ibtracs_csv(
    text: str, *, source_url: str, checksum: str
) -> list[ObservationBatch]:
    observations = parse_ibtracs_csv(text, source_url=source_url, checksum=checksum)
    observations = [o for o in observations if "UNRESOLVED" not in o.storm_id]
    if not observations:
        return []
    raw = pd.DataFrame([asdict(o) for o in observations])
    raw["timestamp"] = pd.to_datetime(raw["timestamp"], utc=True)
    raw = raw[raw["timestamp"].dt.hour % 6 == 0]
    if raw.empty:
        return []
    names = raw.drop_duplicates("storm_id").set_index("storm_id")["storm_name"]
    cleaned, _ = clean_tracks(to_canonical_frame(raw))

    batches = []
    for storm_id, track in cleaned.groupby("storm_id", sort=True):
        track = track.sort_values("timestamp")
        fixes = [
            Fix(
                timestamp=row.timestamp.to_pydatetime(),
                lat=float(row.lat),
                lon=float(row.lon),
                wind_ms=None if pd.isna(row.wind_ms) else float(row.wind_ms),
                pressure_hpa=(
                    None if pd.isna(row.pressure_hpa) else float(row.pressure_hpa)
                ),
                intensity=row.intensity if row.intensity in _INTENSITIES else "UNK",
                source=SOURCE_LABEL,
                source_url=source_url,
            )
            for row in track.itertuples()
        ]
        name = names.get(storm_id) or storm_id
        batches.append(
            ObservationBatch(
                storm_id=storm_id, name=str(name), observations=fixes[-512:]
            )
        )
    return batches


def fetch_ibtracs_active(
    data_root: Path,
    *,
    url: str = ACTIVE_URL,
    downloader: HttpDownloader | None = None,
) -> list[ObservationBatch]:
    """Download ACTIVE with lineage and return validated observation batches."""

    result = (downloader or HttpDownloader()).fetch(
        source="ibtracs",
        url=url,
        destination=data_root / "raw" / "downloads" / "ibtracs" / "ibtracs-active.csv",
    )
    write_download_lineage(
        result,
        data_root=data_root,
        dataset_version="IBTrACS v04r01 ACTIVE",
        parser="parse_ibtracs_csv",
        licence_note="NOAA NCEI IBTrACS v04r01; retain required citation.",
    )
    text = Path(result.local_path).read_text(encoding="utf-8")
    return batches_from_ibtracs_csv(text, source_url=url, checksum=result.sha256)
