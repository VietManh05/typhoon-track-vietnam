"""Cleaning pipeline: parse -> validate -> dedupe -> merge -> sort -> interpolate.

Replaces the ad-hoc ``data_clean.py`` of the sample repo with explicit,
per-storm steps. Invalid rows are dropped with counters; suspicious rows are
*flagged* (never silently deleted); missing wind/pressure values are
interpolated along each storm's own time series (never filled with 0).
"""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd

from typhoon_vn.features import constants as C
from typhoon_vn.features.geo import haversine_km
from typhoon_vn.features.schema import CleaningReport, TrackSchema

#: Jump larger than this between consecutive fixes is physically implausible
#: for a 6-hourly best track and gets flagged as suspicious.
MAX_PLAUSIBLE_STEP_KM = 1200.0


def coerce_frame(df: pd.DataFrame, schema: TrackSchema | None = None) -> pd.DataFrame:
    """Normalise dtypes and fill structural defaults without touching values."""

    schema = schema or TrackSchema()
    out = df.copy()
    out[schema.timestamp] = pd.to_datetime(out[schema.timestamp], utc=True)
    for col in schema.numeric:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    if schema.intensity in out.columns:
        out[schema.intensity] = (
            out[schema.intensity].fillna("UNK").astype(str).str.upper()
        )
    if schema.end_flag in out.columns:
        out[schema.end_flag] = (
            out[schema.end_flag].fillna("ONGOING").astype(str).str.upper()
        )
    if schema.source in out.columns:
        out[schema.source] = out[schema.source].fillna("UNKNOWN").astype(str)
    for flag in (schema.interpolated, schema.suspicious):
        if flag in out.columns:
            out[flag] = out[flag].fillna(False).astype(bool)
        else:
            out[flag] = False
    return out


def validate(
    df: pd.DataFrame,
    schema: TrackSchema | None = None,
    report: CleaningReport | None = None,
) -> pd.DataFrame:
    """Drop rows with invalid coordinates or unphysical wind/pressure values."""

    schema = schema or TrackSchema()
    out = df.copy()
    before = len(out)

    coord_ok = (
        out[schema.lat].between(C.LAT_MIN, C.LAT_MAX)
        & out[schema.lon].between(C.LON_MIN, C.LON_MAX)
        & out[schema.lat].notna()
        & out[schema.lon].notna()
    )
    dropped_coords = int(before - coord_ok.sum())
    out = out.loc[coord_ok].copy()

    physics_ok = pd.Series(True, index=out.index)
    if schema.wind_ms in out.columns:
        physics_ok &= out[schema.wind_ms].isna() | out[schema.wind_ms].between(
            C.WIND_MIN_MS, C.WIND_MAX_MS
        )
    if schema.pressure_hpa in out.columns:
        physics_ok &= out[schema.pressure_hpa].isna() | out[
            schema.pressure_hpa
        ].between(C.PRESSURE_MIN_HPA, C.PRESSURE_MAX_HPA)
    dropped_physics = int(len(out) - physics_ok.sum())
    out = out.loc[physics_ok].copy()

    if report is not None:
        report.n_dropped_invalid_coords += dropped_coords
        report.n_dropped_invalid_physics += dropped_physics
    return out


def deduplicate(
    df: pd.DataFrame,
    schema: TrackSchema | None = None,
    report: CleaningReport | None = None,
    priority_sources: Sequence[str] = ("IBTRACS", "JTWC", "JMA", "CMA", "NCHMF"),
) -> pd.DataFrame:
    """Remove duplicate (storm, timestamp) fixes, keeping the priority source."""

    schema = schema or TrackSchema()
    out = df.copy()
    before = len(out)
    if schema.source in out.columns:
        rank = {name: i for i, name in enumerate(priority_sources)}
        out["_src_rank"] = (
            out[schema.source].astype(str).str.upper().map(rank).fillna(len(rank))
        )
        out = out.sort_values("_src_rank").drop(columns="_src_rank")
    out = out.drop_duplicates(subset=[schema.storm_id, schema.timestamp], keep="first")
    if report is not None:
        report.n_duplicates_removed += int(before - len(out))
    return out


def flag_suspicious_jumps(
    df: pd.DataFrame,
    schema: TrackSchema | None = None,
    report: CleaningReport | None = None,
    max_step_km: float = MAX_PLAUSIBLE_STEP_KM,
) -> pd.DataFrame:
    """Flag (not delete) fixes that jump implausibly far from the previous fix."""

    schema = schema or TrackSchema()
    out = df.copy()
    flagged = 0
    for _, group in out.groupby(schema.storm_id, sort=False):
        idx = group.sort_values(schema.timestamp).index
        prev_lat: float | None = None
        prev_lon: float | None = None
        for i in idx:
            lat = float(out.at[i, schema.lat])
            lon = float(out.at[i, schema.lon])
            if prev_lat is not None:
                step = haversine_km(prev_lat, prev_lon, lat, lon)
                if step > max_step_km:
                    out.at[i, schema.suspicious] = True
                    flagged += 1
            prev_lat, prev_lon = lat, lon
    if report is not None:
        report.n_suspicious_flagged += flagged
    return out


def interpolate_missing(
    df: pd.DataFrame,
    schema: TrackSchema | None = None,
    report: CleaningReport | None = None,
    columns: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Time-interpolate missing wind/pressure *within* each storm's series.

    Leading/trailing NaNs (no neighbour on one side) are left as NaN and the
    row is flagged suspicious instead of being filled with a fabricated 0.
    """

    schema = schema or TrackSchema()
    out = df.copy()
    targets = list(columns) if columns else [schema.wind_ms, schema.pressure_hpa]
    interpolated = 0
    for _, group in out.groupby(schema.storm_id, sort=False):
        idx = group.sort_values(schema.timestamp).index
        for col in targets:
            if col not in out.columns:
                continue
            series = out.loc[idx, col]
            # ``limit_area="inside"`` fills only gaps surrounded by valid
            # values; leading/trailing NaNs are preserved as NaN.
            inside = series.interpolate(method="linear", limit_area="inside")
            was_missing = series.isna()
            newly_filled = was_missing & inside.notna()
            out.loc[idx, col] = inside
            out.loc[idx[newly_filled], schema.interpolated] = True
            interpolated += int(newly_filled.sum())
        # Edge NaNs that could not be interpolated -> suspicious, keep NaN.
        edge_missing = out.loc[idx, targets].isna().any(axis=1)
        out.loc[idx[edge_missing], schema.suspicious] = True
    if report is not None:
        report.n_interpolated += interpolated
    return out


def clean_tracks(
    df: pd.DataFrame,
    schema: TrackSchema | None = None,
    report: CleaningReport | None = None,
) -> tuple[pd.DataFrame, CleaningReport]:
    """Run the full pipeline and return ``(cleaned_frame, report)``."""

    schema = schema or TrackSchema()
    report = report or CleaningReport()
    report.n_input = len(df)

    out = coerce_frame(df, schema)
    out = validate(out, schema, report)
    out = deduplicate(out, schema, report)
    out = out.sort_values([schema.storm_id, schema.timestamp]).reset_index(drop=True)
    out = interpolate_missing(out, schema, report)
    out = flag_suspicious_jumps(out, schema, report)

    # Keep the canonical column order; tolerate absent optional columns.
    keep = [c for c in schema.columns() if c in out.columns]
    out = out[keep]
    report.n_output = len(out)
    return out, report


def quality_summary(df: pd.DataFrame, schema: TrackSchema | None = None) -> dict:
    """Missing-value / range summary used for the WBS 1.8 quality report."""

    schema = schema or TrackSchema()
    summary: dict[str, object] = {
        "n_rows": len(df),
        "n_storms": int(df[schema.storm_id].nunique()) if len(df) else 0,
    }
    for col in schema.numeric:
        if col in df.columns:
            summary[f"{col}_missing"] = int(df[col].isna().sum())
            summary[f"{col}_min"] = (
                float(df[col].min()) if df[col].notna().any() else None
            )
            summary[f"{col}_max"] = (
                float(df[col].max()) if df[col].notna().any() else None
            )
    if schema.suspicious in df.columns:
        summary["n_suspicious"] = int(df[schema.suspicious].sum())
    if schema.interpolated in df.columns:
        summary["n_interpolated"] = int(df[schema.interpolated].sum())
    return summary


def convert_wind_knots_to_ms(df: pd.DataFrame, column: str = "wind_ms") -> pd.DataFrame:
    """Convert a wind column from knots to m/s (1 kt = 0.514444 m/s)."""

    out = df.copy()
    out[column] = pd.to_numeric(out[column], errors="coerce") * 0.514444
    return out


def normalise_intensity_labels(
    df: pd.DataFrame, schema: TrackSchema | None = None
) -> pd.DataFrame:
    """Map unknown intensity grades onto the fixed category list."""

    schema = schema or TrackSchema()
    out = df.copy()
    if schema.intensity not in out.columns:
        out[schema.intensity] = "UNK"
    labels = out[schema.intensity].astype(str).str.upper()
    out[schema.intensity] = labels.where(labels.isin(C.INTENSITY_CATEGORIES), "UNK")
    return out


__all__ = [
    "MAX_PLAUSIBLE_STEP_KM",
    "clean_tracks",
    "coerce_frame",
    "convert_wind_knots_to_ms",
    "deduplicate",
    "flag_suspicious_jumps",
    "interpolate_missing",
    "normalise_intensity_labels",
    "quality_summary",
    "validate",
]
