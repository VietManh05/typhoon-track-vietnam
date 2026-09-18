"""Leak-free scaling: fit on train only, reuse everywhere else (WBS 5.x).

Fixes the sample repo's leak (min-max computed over the *whole* dataset) by
encapsulating fitted statistics in ``FeatureScaler`` and persisting them to
disk so inference uses exactly the training-time parameters.
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def _fill_non_finite(values: np.ndarray, fill: np.ndarray) -> np.ndarray:
    """Replace NaN/±inf entries with the per-column fill value.

    Lag/delta columns legitimately hold NaN at series starts and a corrupted
    source column can carry inf; both would otherwise poison the standard score.
    """

    return np.where(np.isfinite(values), values, fill)


class FeatureScaler:
    """Standard-score scaler with save/load and inverse transform support."""

    def __init__(self, feature_columns: list[str] | None = None) -> None:
        self.feature_columns: list[str] = list(feature_columns or [])
        self._scaler = StandardScaler()
        self._fitted = False

    @property
    def is_fitted(self) -> bool:
        return self._fitted

    def fit(self, df: pd.DataFrame) -> FeatureScaler:
        """Fit statistics on the *training* frame only."""

        if not self.feature_columns:
            self.feature_columns = [c for c in df.columns if c != "storm_id"]
        values = df[self.feature_columns].to_numpy(dtype=float)
        # Lag/delta columns legitimately contain NaN at series starts; use the
        # column mean as a neutral fill *computed from train only*. ±inf is
        # masked out first so a single corrupted reading cannot bias the mean.
        finite = np.where(np.isfinite(values), values, np.nan)
        with warnings.catch_warnings():
            # numpy warns "Mean of empty slice" for all-NaN columns; the
            # degenerate-column branch below reports that case explicitly.
            warnings.simplefilter("ignore", RuntimeWarning)
            fill = np.nanmean(finite, axis=0)
        # ``nanmean`` returns NaN when a column has no finite training value
        # (e.g. a lag column whose lag exceeds every storm's length, or an
        # all-missing SST/wind-shear channel). Left as-is it would poison every
        # transformed row, so fall back to a neutral 0.0 and warn instead of
        # corrupting the scaler silently.
        degenerate = ~np.isfinite(fill)
        if degenerate.any():
            names = [self.feature_columns[j] for j in np.flatnonzero(degenerate)]
            warnings.warn(
                "FeatureScaler: no finite training values for "
                f"{names}; using a neutral 0.0 fill (column stays constant 0 "
                "after scaling).",
                RuntimeWarning,
                stacklevel=2,
            )
            fill = np.where(degenerate, 0.0, fill)
        self._fill_values = fill
        self._scaler.fit(_fill_non_finite(values, fill))
        self._fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Scale a frame with frozen training statistics and column order."""

        self._validate_columns(df)

        self._require_fitted()
        out = df.copy()
        values = out[self.feature_columns].to_numpy(dtype=float)
        filled = _fill_non_finite(values, self._fill_values)
        out[self.feature_columns] = self._scaler.transform(filled)
        return out

    def inverse_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Restore original units (round-trip check + inference denormalise)."""

        self._require_fitted()
        out = df.copy()
        values = out[self.feature_columns].to_numpy(dtype=float)
        out[self.feature_columns] = self._scaler.inverse_transform(values)
        return out

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.fit(df).transform(df)

    def save(self, path: str | Path) -> Path:
        """Persist scaler + column order + fill values for serving."""

        self._require_fitted()
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(
            {
                "scaler": self._scaler,
                "feature_columns": self.feature_columns,
                "fill_values": self._fill_values,
            },
            path,
        )
        # Human-readable sidecar for audits.
        path.with_suffix(".json").write_text(
            json.dumps(
                {
                    "feature_columns": self.feature_columns,
                    "mean": self._scaler.mean_.tolist(),
                    "scale": self._scaler.scale_.tolist(),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return path

    @classmethod
    def load(cls, path: str | Path) -> FeatureScaler:
        """Reload a scaler fitted during training (inference path)."""

        payload = joblib.load(path)
        obj = cls(feature_columns=list(payload["feature_columns"]))
        obj._scaler = payload["scaler"]
        obj._fill_values = np.asarray(payload["fill_values"], dtype=float)
        obj._fitted = True
        return obj

    def _validate_columns(self, df: pd.DataFrame) -> None:
        actual = list(df.columns)
        missing = [name for name in self.feature_columns if name not in actual]
        if missing:
            raise ValueError(f"missing feature columns: {missing}")
        extra = [name for name in actual if name not in self.feature_columns]
        if extra:
            raise ValueError(f"unexpected feature columns: {extra}")
        if actual != self.feature_columns:
            raise ValueError(
                "feature columns are reordered; expected "
                f"{self.feature_columns} in training order"
            )

    def _require_fitted(self) -> None:
        if not self._fitted:
            raise RuntimeError("FeatureScaler must be fitted before transform().")


__all__ = ["FeatureScaler"]
