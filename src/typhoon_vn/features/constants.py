"""Fixed domain constants for the Phase 2 cleaning/feature pipeline.

Category lists are intentionally *fixed* (not inferred from data) so that
one-hot encodings keep the same dimensionality between train and inference.
"""

from __future__ import annotations

# --- Geographic scope -------------------------------------------------------
# Vietnam's area of interest (wider than the strict 5-24N / 100-125E focus so
# that approaching storms are still tracked).
LAT_MIN, LAT_MAX = 0.0, 30.0
LON_MIN, LON_MAX = 100.0, 140.0

# --- Physical plausibility ranges -------------------------------------------
PRESSURE_MIN_HPA, PRESSURE_MAX_HPA = 850.0, 1050.0
WIND_MIN_MS, WIND_MAX_MS = 0.0, 110.0  # ~215 kt upper sanity bound

# --- Intensity categories (fixed class list, tropical Northwest Pacific) -----
# Ordered from weakest to strongest; ``UNK`` covers missing/unknown grades.
INTENSITY_CATEGORIES: tuple[str, ...] = ("TD", "TS", "STS", "TY", "STY", "SUPERTY", "UNK")

# --- Record lifecycle flags --------------------------------------------------
# ``END`` in the CMA best-track format marks the last message of a storm.
END_FLAGS: tuple[str, ...] = ("END", "ONGOING")

# --- Vietnam typhoon season (peak months) ------------------------------------
SEASON_MONTHS: frozenset[int] = frozenset({6, 7, 8, 9, 10, 11, 12})

# --- Geographic reference points (approximate centroids) ---------------------
REFERENCE_POINTS: dict[str, tuple[float, float]] = {
    "hoang_sa": (16.55, 112.30),  # Paracel Islands
    "truong_sa": (8.64, 111.92),  # Spratly Islands
    "da_nang_port": (16.07, 108.22),
    "hai_phong_port": (20.86, 106.68),
    "vung_tau_port": (10.35, 107.07),
}

# --- Simplified Vietnam coastline (west -> north, lon/lat pairs) -------------
# Coarse polyline of the mainland coast used for distance/bearing features.
# Sufficient for feature engineering; a high-resolution GSHHG coastline is a
# Phase 1/Geospatial-data task and can replace this table transparently.
VN_COASTLINE: tuple[tuple[float, float], ...] = (
    (8.60, 104.83),  # Ca Mau tip
    (9.30, 105.90),
    (10.35, 106.85),
    (10.90, 108.10),
    (11.90, 109.20),
    (12.90, 109.40),
    (13.80, 109.30),
    (14.60, 109.10),
    (15.60, 108.60),
    (16.10, 108.20),  # Da Nang
    (16.80, 107.40),
    (17.60, 106.50),
    (18.70, 105.80),
    (19.80, 105.90),
    (20.70, 106.70),  # Hai Phong
    (21.40, 107.90),
)
