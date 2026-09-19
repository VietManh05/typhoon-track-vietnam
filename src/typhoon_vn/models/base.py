"""Base interfaces shared by all track-forecast models."""

from __future__ import annotations

import torch
from torch import nn


class TrackForecaster(nn.Module):
    """Base class exposing a common forward signature.

    All concrete models must return a dict with at least:
      - ``reg``: tensor ``(B, H, 2)`` for lat/lon regression
      - ``cls``: tensor ``(B, H, C)`` for intensity classification logits
      - ``wind`` (optional): tensor ``(B, H, 1)`` in m/s
      - ``pressure`` (optional): tensor ``(B, H, 1)`` in hPa
      - ``attn`` (optional): attention weights for interpretability

    Concrete subclasses should set ``_n_horizons`` and ``_n_classes`` in
    their ``__init__`` so that the base-class properties work correctly.

    Subclasses **must** also implement :meth:`encode` and :attr:`context_size`
    so that wrappers like ``QuantileTrackForecaster`` can reuse the encoder
    without running a second forward pass.
    """

    _n_horizons: int = 1
    _n_classes: int = 7

    def forward(
        self, x: torch.Tensor, mask: torch.Tensor | None = None
    ) -> dict[str, torch.Tensor]:
        raise NotImplementedError

    def encode(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        """Return the context vector for the input sequence.

        Must be implemented by all concrete subclasses.  The returned tensor
        has shape ``(B, context_size)`` and represents the pre-head
        representation that both regression and classification heads consume.
        """
        raise NotImplementedError

    @property
    def context_size(self) -> int:
        """Dimension of the context vector returned by :meth:`encode`."""
        raise NotImplementedError

    @property
    def n_horizons(self) -> int:
        """Number of forecast horizons this model predicts."""
        return getattr(self, "_n_horizons", 1)

    @property
    def n_classes(self) -> int:
        """Number of intensity classes this model predicts."""
        return getattr(self, "_n_classes", 7)
