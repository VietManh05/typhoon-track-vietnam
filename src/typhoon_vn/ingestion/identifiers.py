"""Conservative normalisation of western-North-Pacific storm identifiers."""

from __future__ import annotations

import re

_ATCF_ID = re.compile(r"^(?P<basin>[A-Z]{2})(?P<number>\d{2})(?P<year>\d{4})$")
_YYYY_NUMBER = re.compile(r"^(?P<year>\d{4})(?P<number>\d{2})$")
_YY_NUMBER = re.compile(r"^(?P<year>\d{2})(?P<number>\d{2})$")


def canonical_storm_id(
    source_id: str | None,
    *,
    basin: str = "WP",
    season: int | None = None,
) -> str:
    """Return an ATCF-shaped ID where the source gives enough evidence.

    The function deliberately does not infer an identifier from a storm name or
    from nearby coordinates. Ambiguous records remain source-qualified so a
    later reconciliation rule cannot silently create a false cross-agency join.
    """

    cleaned = re.sub(r"[^A-Za-z0-9]", "", source_id or "").upper()
    basin = re.sub(r"[^A-Za-z]", "", basin.upper())[:2] or "WP"
    if _ATCF_ID.fullmatch(cleaned):
        return cleaned
    match = _YYYY_NUMBER.fullmatch(cleaned)
    if match:
        return f"{basin}{match['number']}{match['year']}"
    match = _YY_NUMBER.fullmatch(cleaned)
    if match:
        century = 1900 if int(match["year"]) >= 50 else 2000
        return f"{basin}{match['number']}{century + int(match['year']):04d}"
    if season is not None and cleaned.isdigit() and len(cleaned) <= 3:
        return f"{basin}{int(cleaned):02d}{season:04d}"
    return f"{basin}-UNRESOLVED-{cleaned or 'UNKNOWN'}"


def is_resolved_storm_id(storm_id: str) -> bool:
    """Return whether an ID is safe to use as a cross-source merge key."""

    return _ATCF_ID.fullmatch(storm_id) is not None
