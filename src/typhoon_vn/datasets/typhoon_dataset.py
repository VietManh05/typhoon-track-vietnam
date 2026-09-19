"""Multi-horizon typhoon track dataset.

Replaces the original ``data_loader.py`` (fixed 4-step input, 1-step output,
index-based train/val split) with a configurable sliding-window dataset that
splits by storm ID or year to avoid leakage.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch

from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.features.schema import DEFAULT_SCHEMA, TrackSchema


@dataclass(frozen=True)
class DatasetConfig:
    """Configuration for ``TyphoonDataset``."""

    input_len: int = 4
    horizon: Sequence[int] = (1, 2, 4, 8, 12)  # 6h steps: 6h..72h
    target_cols: Sequence[str] = ("lat", "lon")
    feature_cols: Sequence[str] | None = None  # None = auto-build
    include_intensity_target: bool = True
    time_step_hours: int = 6


class TyphoonDataset(torch.utils.data.Dataset):
    """Sliding-window dataset for multi-horizon typhoon track forecasting.

    Each sample consists of:
      - ``x``: tensor of shape ``(input_len, n_features)``
      - ``y_reg``: tensor of shape ``(n_horizons, 2)`` with lat/lon targets
      - ``y_cls``: tensor of shape ``(n_horizons,)`` with intensity class IDs
      - ``mask``: tensor of shape ``(input_len,)`` with valid flags
      - ``meta``: dict with storm_id and issue time for traceability
    """

    def __init__(
        self,
        df: pd.DataFrame,
        config: DatasetConfig | None = None,
        schema: TrackSchema | None = None,
        intensity_order: Sequence[str] | None = None,
        scaler: FeatureScaler | None = None,
    ) -> None:
        self.config = config or DatasetConfig()
        self.schema = schema or DEFAULT_SCHEMA
        self.intensity_order = list(
            intensity_order or ("TD", "TS", "STS", "TY", "STY", "SUPERTY", "UNK")
        )
        self.scaler = scaler
        self.intensity_to_idx = {name: i for i, name in enumerate(self.intensity_order)}

        self.samples: list[dict[str, Any]] = []
        self.feature_cols: list[str] = []
        self.schema.validate_columns(df.columns)
        self._build(df)

    def _build(self, df: pd.DataFrame) -> None:
        df = df.copy()
        df[self.schema.timestamp] = pd.to_datetime(df[self.schema.timestamp], utc=True)
        df = df.sort_values([self.schema.storm_id, self.schema.timestamp]).reset_index(
            drop=True
        )

        # Build derived features before resolving their fixed vocabulary.  This
        # is the same FeatureBuilder path used by serving.
        df = FeatureBuilder().transform(df)

        # Auto feature columns if not provided
        if self.config.feature_cols is None:
            self.feature_cols = list(FEATURE_COLUMNS)
        else:
            self.feature_cols = list(self.config.feature_cols)

        if len(self.feature_cols) != len(set(self.feature_cols)):
            raise ValueError("feature_cols must not contain duplicates")

        # Explicit custom lists are selected from this same transformed frame.

        if self.scaler is not None:
            if not self.scaler.is_fitted:
                raise ValueError("dataset scaler must be fitted on training data")
            scaled = self.scaler.transform(df[self.feature_cols])
            df.loc[:, self.feature_cols] = scaled

        # Ensure all feature columns exist
        missing = [c for c in self.feature_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Feature columns missing from frame: {missing}")

        for storm_id, group in df.groupby(self.schema.storm_id, sort=False):
            group = group.reset_index(drop=True)
            total = len(group)
            if group[self.schema.timestamp].duplicated().any():
                raise ValueError(f"duplicate timestamps for storm {storm_id}")
            time_step = pd.Timedelta(hours=self.config.time_step_hours)
            positions = {
                timestamp: index
                for index, timestamp in enumerate(group[self.schema.timestamp])
            }
            max_offset = max(self.config.horizon)
            # A quick length check avoids scanning storms that cannot hold even
            # a regular input window plus the furthest target.
            # more rows for the furthest target.  Horizon values are 1-based
            # (h=1 means the step immediately after the window), so the target
            # index for horizon h is  start + input_len + h - 1.
            # With start running from 0 to (total - input_len - max_offset),
            # the maximum target index is  (total - input_len - max_offset)
            #   + input_len + max_offset - 1  =  total - 1  ✓ (always in-bounds).
            if total < self.config.input_len + max_offset:
                continue
            for start in range(total - self.config.input_len - max_offset + 1):
                input_rows = group.iloc[start : start + self.config.input_len]
                input_times = input_rows[self.schema.timestamp].tolist()
                expected_input_times = [
                    input_times[-1] - time_step * offset
                    for offset in reversed(range(self.config.input_len))
                ]
                if input_times != expected_input_times:
                    continue
                issue_time = input_times[-1]
                target_positions = [
                    positions.get(issue_time + time_step * h)
                    for h in self.config.horizon
                ]
                if any(position is None for position in target_positions):
                    continue
                y_reg_list: list[list[float]] = []
                y_cls_list: list[int] = []
                for position in target_positions:
                    assert position is not None
                    target_row = group.iloc[position]
                    y_reg_list.append(
                        [float(target_row[col]) for col in self.config.target_cols]
                    )
                    intensity = str(
                        target_row.get(self.schema.intensity, "UNK")
                    ).upper()
                    y_cls_list.append(
                        self.intensity_to_idx.get(
                            intensity, self.intensity_to_idx["UNK"]
                        )
                    )
                self.samples.append(
                    {
                        "x": input_rows[self.feature_cols].to_numpy(dtype=np.float32),
                        "mask": np.ones(self.config.input_len, dtype=np.float32),
                        "y_reg": np.array(y_reg_list, dtype=np.float32),
                        "y_cls": np.array(y_cls_list, dtype=np.int64),
                        "meta": {
                            "storm_id": str(storm_id),
                            "issue_time": pd.Timestamp(issue_time),
                            "horizons": list(self.config.horizon),
                        },
                    }
                )

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> dict[str, Any]:
        return self.samples[idx]

    @property
    def n_features(self) -> int:
        return len(self.feature_cols)

    @property
    def n_horizons(self) -> int:
        return len(self.config.horizon)

    @property
    def n_classes(self) -> int:
        return len(self.intensity_order)


def split_by_storm_or_year(
    df: pd.DataFrame,
    val_ratio: float = 0.1,
    test_ratio: float = 0.1,
    by_year: bool = False,
    schema: TrackSchema | None = None,
    random_seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split a track frame into train/val/test without leaking across storms.

    When ``by_year`` is True, the most recent years become test/validation;
    otherwise storms are randomly shuffled and partitioned.
    """

    schema = schema or DEFAULT_SCHEMA
    if not 0 <= val_ratio < 1 or not 0 <= test_ratio < 1:
        raise ValueError("val_ratio and test_ratio must be in [0, 1)")
    if val_ratio + test_ratio >= 1:
        raise ValueError("val_ratio + test_ratio must be less than 1")
    df = df.copy()
    df[schema.timestamp] = pd.to_datetime(df[schema.timestamp], utc=True)

    if by_year:
        # Assign each whole storm by its final observed UTC year.  Splitting
        # rows by calendar year would leak a storm crossing 31 Dec.
        df["_year"] = (
            df.groupby(schema.storm_id)[schema.timestamp].transform("max").dt.year
        )
        years = sorted(df["_year"].unique())
        n_test = int(round(len(years) * test_ratio))
        n_val = int(round(len(years) * val_ratio))
        test_years = set(years[-n_test:]) if n_test else set()
        test_start = len(years) - n_test
        val_years = set(years[test_start - n_val : test_start]) if n_val else set()
        train = df[~df["_year"].isin(test_years | val_years)].drop(columns="_year")
        val = df[df["_year"].isin(val_years)].drop(columns="_year")
        test = df[df["_year"].isin(test_years)].drop(columns="_year")
        return (
            train.reset_index(drop=True),
            val.reset_index(drop=True),
            test.reset_index(drop=True),
        )

    rng = np.random.default_rng(random_seed)
    storm_ids = list(df[schema.storm_id].unique())
    rng.shuffle(storm_ids)
    n_test = int(round(len(storm_ids) * test_ratio))
    n_val = int(round(len(storm_ids) * val_ratio))
    test_ids = set(storm_ids[:n_test])
    val_ids = set(storm_ids[n_test : n_test + n_val])
    train_ids = set(storm_ids[n_test + n_val :])
    train = df[df[schema.storm_id].isin(train_ids)]
    val = df[df[schema.storm_id].isin(val_ids)]
    test = df[df[schema.storm_id].isin(test_ids)]
    return (
        train.reset_index(drop=True),
        val.reset_index(drop=True),
        test.reset_index(drop=True),
    )


def split_manifest(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    test: pd.DataFrame,
    *,
    schema: TrackSchema | None = None,
    policy: str,
    seed: int | None = None,
) -> dict[str, Any]:
    """Return an auditable, leakage-checked split manifest."""

    schema = schema or DEFAULT_SCHEMA
    ids = {
        "train": sorted(map(str, train[schema.storm_id].unique())),
        "validation": sorted(map(str, validation[schema.storm_id].unique())),
        "test": sorted(map(str, test[schema.storm_id].unique())),
    }
    sets = {name: set(values) for name, values in ids.items()}
    if (
        sets["train"] & sets["validation"]
        or sets["train"] & sets["test"]
        or sets["validation"] & sets["test"]
    ):
        raise ValueError("storm IDs overlap across train/validation/test")
    return {
        "policy": policy,
        "seed": seed,
        "train_ids": ids["train"],
        "validation_ids": ids["validation"],
        "test_ids": ids["test"],
        "row_counts": {
            "train": len(train),
            "validation": len(validation),
            "test": len(test),
        },
    }


def save_split_manifest(manifest: dict[str, Any], path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return path


def collate_fn(batch: Sequence[dict[str, Any]]) -> dict[str, torch.Tensor]:
    """Stack fixed-length samples into a batched dict.

    All samples produced by ``TyphoonDataset._build`` have the same
    ``input_len``, so simple stacking is sufficient.  ``pad_sequence`` is
    not needed here; if you extend the dataset to support variable-length
    windows, replace ``torch.stack`` with ``pad_sequence`` accordingly.
    """
    x = torch.stack([torch.from_numpy(b["x"].copy()) for b in batch], dim=0)
    mask = torch.stack([torch.from_numpy(b["mask"].copy()) for b in batch], dim=0)
    y_reg = torch.stack([torch.from_numpy(b["y_reg"].copy()) for b in batch], dim=0)
    y_cls = torch.stack([torch.from_numpy(b["y_cls"].copy()) for b in batch], dim=0)
    return {
        "x": x,
        "mask": mask,
        "y_reg": y_reg,
        "y_cls": y_cls,
        "meta": [b["meta"] for b in batch],
    }
