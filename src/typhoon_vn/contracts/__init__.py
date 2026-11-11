"""Stable contracts shared by ingestion, features, training, and serving."""

from typhoon_vn.contracts.track import CleaningReport, TrackSchema

__all__ = ["CleaningReport", "TrackSchema"]
