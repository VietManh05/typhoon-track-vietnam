"""Phase 2 bridge: raw Phase 1 observations -> canonical cleaned frame.

Reads every ``data/raw/observations/source=*/year=*/part-*.parquet`` file,
converts source wind units to m/s (IBTrACS/JMA/JTWC/NCHMF report knots; CMA
reports m/s), keeps provenance columns, and hands the canonical table to the
cleaning pipeline. IBTrACS-only storms keep their pre-1951 history; JMA rows
before its 1951 archive start are still parsed but only merged where the
resolved ATCF storm ID matches.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from typhoon_vn.features.cleaning import normalise_intensity_labels
from typhoon_vn.features.schema import TrackSchema

KNOT_TO_MS = 0.514444

SCHEMA = TrackSchema()

#: Raw wind units by source. Unknown sources keep their raw values and are
#: flagged downstream by the physics validation instead of being converted.
WIND_UNIT_TO_MS: dict[str, float] = {
    "kt": KNOT_TO_MS,
    "knot": KNOT_TO_MS,
    "knots": KNOT_TO_MS,
    "m/s": 1.0,
    "ms": 1.0,
}

#: JMA RSMC best-track archive starts in 1951; earlier IBTrACS rows come from
#: other agencies and must not be dropped by a JMA-coverage rule.
JMA_ARCHIVE_START_YEAR = 1951

#: JMA grade codes (RSMC Tokyo best track) mapped onto the fixed intensity list.
JMA_GRADE_TO_INTENSITY: dict[str, str] = {
    "2": "TS",
    "3": "TS",
    "4": "STS",
    "5": "TY",
    "6": "STY",
    "7": "SUPERTY",
    "9": "UNK",
}


def _wind_to_ms(values: pd.Series, units: pd.Series) -> pd.Series:
    """Convert a raw wind column to m/s and reject unrecognised units."""

    numeric = pd.to_numeric(values, errors="coerce")
    normalised = units.astype("string").str.strip().str.lower()
    unknown = numeric.notna() & ~normalised.isin(WIND_UNIT_TO_MS)
    if unknown.any():
        labels = sorted(normalised.loc[unknown].fillna("<missing>").unique().tolist())
        raise ValueError(f"unsupported wind units: {labels}")
    factor = (
        normalised.map(WIND_UNIT_TO_MS).astype(float)
    )
    return numeric * factor


def _map_intensity(frame: pd.DataFrame) -> np.ndarray:
    """Vectorised intensity mapping (no per-row ``Series.apply``).

    JMA grade codes are translated through :data:`JMA_GRADE_TO_INTENSITY`;
    every other row keeps its raw, upper-cased intensity code. ``np.select``
    evaluates the whole column at once, which is far cheaper than
    ``frame.apply(..., axis=1)`` on the multi-decade archive.
    """

    sources = frame.get("source", pd.Series("", index=frame.index))
    is_jma = sources.astype(str).str.strip().str.lower().eq("jma").to_numpy()

    if "intensity_code" in frame.columns:
        raw_code = frame["intensity_code"]
    else:
        raw_code = pd.Series([None] * len(frame), index=frame.index)

    grade = raw_code.astype(str).str.strip()
    mapped = grade.map(JMA_GRADE_TO_INTENSITY).to_numpy()
    fallback = (
        raw_code.fillna("UNK")
        .astype(str)
        .str.strip()
        .str.upper()
        .replace({"": "UNK"})
        .to_numpy()
    )

    return np.select([is_jma & pd.notna(mapped)], [mapped], default=fallback)


def _filter_jma_archive_coverage(
    frame: pd.DataFrame, schema: TrackSchema
) -> pd.DataFrame:
    """Drop JMA rows dated before the RSMC archive start year.

    JMA's best-track archive begins in :data:`JMA_ARCHIVE_START_YEAR`, so a
    JMA-labelled row dated earlier can only come from a corrupt timestamp.
    IBTrACS rows are exempt: their pre-1951 history comes from other agencies
    and must not be removed by a JMA-coverage rule.
    """

    if schema.timestamp not in frame.columns or schema.source not in frame.columns:
        return frame
    years = pd.to_datetime(frame[schema.timestamp], utc=True, errors="coerce").dt.year
    is_jma = frame[schema.source].astype(str).str.strip().str.lower().eq("jma")
    pre_archive = years.lt(JMA_ARCHIVE_START_YEAR) & is_jma
    if pre_archive.any():
        frame = frame.loc[~pre_archive].copy()
    return frame


def load_raw_observations(data_root: str | Path) -> pd.DataFrame:
    """Load every raw observation partition into one frame with provenance."""

    pattern = "raw/observations/source=*/year=*/*.parquet"
    files = sorted(Path(data_root).glob(pattern))
    if not files:
        root = Path(data_root) / "raw/observations"
        raise FileNotFoundError(f"No raw observation partitions under {root}")
    frames = [pd.read_parquet(path) for path in files]
    return pd.concat(frames, ignore_index=True)


def to_canonical_frame(
    raw: pd.DataFrame, schema: TrackSchema | None = None
) -> pd.DataFrame:
    """Map raw Phase 1 rows onto the canonical cleaned-track schema."""

    schema = schema or SCHEMA
    frame = raw.copy()
    frame["wind_ms"] = _wind_to_ms(frame["wind"], frame["wind_unit"])
    frame["pressure_hpa"] = pd.to_numeric(frame["pressure_hpa"], errors="coerce")
    frame["intensity"] = _map_intensity(frame)
    frame["end_flag"] = "ONGOING"
    frame["interpolated"] = False
    frame["suspicious"] = False
    frame = frame.rename(
        columns={
            "storm_id": schema.storm_id,
            "timestamp": schema.timestamp,
            "latitude": schema.lat,
            "longitude": schema.lon,
            "wind_ms": schema.wind_ms,
            "pressure_hpa": schema.pressure_hpa,
            "intensity": schema.intensity,
            "end_flag": schema.end_flag,
            "source": schema.source,
            "interpolated": schema.interpolated,
            "suspicious": schema.suspicious,
        }
    )
    keep = [c for c in schema.columns() if c in frame.columns]
    out = frame[keep].copy()
    out = _filter_jma_archive_coverage(out, schema)
    return normalise_intensity_labels(out, schema)


__all__ = [
    "JMA_ARCHIVE_START_YEAR",
    "JMA_GRADE_TO_INTENSITY",
    "KNOT_TO_MS",
    "SCHEMA",
    "WIND_UNIT_TO_MS",
    "load_raw_observations",
    "to_canonical_frame",
]
