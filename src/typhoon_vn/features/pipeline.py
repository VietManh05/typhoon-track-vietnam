"""Auditable raw-to-feature pipeline used by the Phase-2 data gate."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import pandas as pd

from typhoon_vn.features.bridge import to_canonical_frame
from typhoon_vn.features.build import FeatureBuilder
from typhoon_vn.features.cleaning import clean_tracks, quality_summary
from typhoon_vn.features.schema import CleaningReport


@dataclass(slots=True)
class Phase2Pipeline:
    """Compose parse, validation, merge, sort, interpolation and features."""

    builder: FeatureBuilder = field(default_factory=FeatureBuilder)

    def parse(self, frame: pd.DataFrame) -> pd.DataFrame:
        return to_canonical_frame(frame)

    def merge(self, frames: Iterable[pd.DataFrame]) -> pd.DataFrame:
        materialised = [self.parse(frame) for frame in frames]
        if not materialised:
            raise ValueError("at least one source frame is required")
        return pd.concat(materialised, ignore_index=True)

    def run(
        self, frames: Iterable[pd.DataFrame]
    ) -> tuple[pd.DataFrame, CleaningReport]:
        merged = self.merge(frames)
        cleaned, report = clean_tracks(merged)
        featured = self.builder.transform(cleaned)
        return featured, report

    def export(
        self,
        frame: pd.DataFrame,
        report: CleaningReport,
        destination: str | Path,
    ) -> Path:
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(f".{destination.name}.tmp")
        try:
            frame.to_parquet(temporary, index=False)
            os.replace(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)
        payload = {"cleaning": report.as_dict(), "quality": quality_summary(frame)}
        report_path = destination.with_suffix(".quality.json")
        report_tmp = report_path.with_name(f".{report_path.name}.tmp")
        report_tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        os.replace(report_tmp, report_path)
        return destination


__all__ = ["Phase2Pipeline"]
