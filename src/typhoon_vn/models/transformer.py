"""Lightweight Transformer track forecaster.

Implements a Temporal-Fusion-Transformer-inspired encoder using PyTorch's
built-in ``nn.TransformerEncoderLayer`` with:
- Learnable positional encoding for the short input windows (≤ 16 steps).
- Multi-head self-attention over the sequence.
- Two separate output heads (regression + classification), identical to the
  LSTM variants so they are fully interchangeable.

The design is intentionally *small* (default d_model=64, nhead=4, 2 layers)
to be comparable with the LSTM baselines in terms of parameter count and
training time.  Use this to test whether attention helps over LSTM before
committing to a larger model.
"""

from __future__ import annotations

import math

import torch
from torch import nn

from typhoon_vn.models.base import TrackForecaster


class PositionalEncoding(nn.Module):
    """Sinusoidal positional encoding (Vaswani et al., 2017).

    Works for any sequence length up to ``max_len``.
    """

    def __init__(self, d_model: int, max_len: int = 64, dropout: float = 0.1) -> None:
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        if d_model % 2 == 0:
            pe[:, 1::2] = torch.cos(position * div_term)
        else:
            pe[:, 1::2] = torch.cos(position * div_term[: d_model // 2])
        # shape: (1, max_len, d_model) for batch-first usage
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, T, d_model)
        x = x + self.pe[:, : x.size(1), :]
        return self.dropout(x)


class TransformerTrackForecaster(TrackForecaster):
    """Transformer encoder + dual output head for multi-horizon track forecasting.

    Architecture:
    1. Linear projection: ``n_features → d_model``
    2. Sinusoidal positional encoding
    3. ``n_layers`` Transformer encoder layers (self-attention + FFN)
    4. Mean-pooling over the sequence (or use CLS-like last token)
    5. Regression head: ``d_model → n_horizons * 2``
    6. Classification head: ``d_model → n_horizons * n_classes``

    Output format is identical to ``LSTMTrackForecaster`` for drop-in usage.
    """

    def __init__(
        self,
        n_features: int,
        n_horizons: int,
        n_classes: int,
        d_model: int = 64,
        nhead: int = 4,
        n_layers: int = 2,
        dim_feedforward: int = 128,
        dropout: float = 0.1,
    ) -> None:
        super().__init__()
        self._n_horizons = n_horizons
        self._n_classes = n_classes
        self.d_model = d_model

        self.input_proj = nn.Linear(n_features, d_model)
        self.pos_enc = PositionalEncoding(d_model, dropout=dropout)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)

        self.reg_head = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, n_horizons * 2),
        )
        self.cls_head = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, n_horizons * n_classes),
        )

    def forward(
        self, x: torch.Tensor, mask: torch.Tensor | None = None
    ) -> dict[str, torch.Tensor]:
        """Forward pass.

        Args:
            x: ``(B, T, n_features)``
            mask: ``(B, T)`` float mask; 0 = padding, 1 = valid.

        Returns:
            ``{"reg": (B, H, 2), "cls": (B, H, C)}``
        """
        context = self.encode(x, mask)  # (B, d_model)
        reg = self.reg_head(context).view(-1, self._n_horizons, 2)
        cls = self.cls_head(context).view(-1, self._n_horizons, self._n_classes)
        return {"reg": reg, "cls": cls}

    def encode(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        """Project, add positional encoding, run Transformer, return last token.

        Args:
            x: ``(B, T, n_features)``
            mask: ``(B, T)`` float mask; 0 = padding, 1 = valid.

        Returns:
            Context tensor of shape ``(B, d_model)``.
        """
        # Project features → d_model
        h = self.input_proj(x)  # (B, T, d_model)
        h = self.pos_enc(h)

        # Build key-padding mask for Transformer (True = ignore)
        src_key_padding_mask: torch.Tensor | None = None
        if mask is not None:
            src_key_padding_mask = mask == 0  # (B, T), bool

        enc_out = self.encoder(
            h, src_key_padding_mask=src_key_padding_mask
        )  # (B, T, d_model)

        if mask is None:
            return enc_out.mean(dim=1)
        valid = mask.to(enc_out).unsqueeze(-1)
        counts = valid.sum(dim=1).clamp_min(1.0)
        return (enc_out * valid).sum(dim=1) / counts

    @property
    def context_size(self) -> int:
        return self.d_model
