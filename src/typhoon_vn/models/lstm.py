"""LSTM-based track forecasters.

Includes the original single-step LSTM idea (baseline), an encoder-decoder
seq2seq variant for direct multi-horizon output, and an LSTM + attention
variant that can focus on historical fixes.
"""

from __future__ import annotations

import torch
from torch import nn

from typhoon_vn.models.base import TrackForecaster


class LSTMTrackForecaster(TrackForecaster):
    """Baseline LSTM adapted from the sample repo, extended to multi-horizon.

    A single LSTM reads the input window and a fully-connected head emits
    ``n_horizons`` lat/lon pairs plus intensity logits.
    """

    def __init__(
        self,
        n_features: int,
        n_horizons: int,
        n_classes: int,
        hidden_size: int = 128,
        num_layers: int = 2,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self._n_horizons = n_horizons
        self._n_classes = n_classes
        self.lstm = nn.LSTM(
            input_size=n_features,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.reg_head = nn.Linear(hidden_size, n_horizons * 2)
        self.cls_head = nn.Linear(hidden_size, n_horizons * n_classes)

    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> dict[str, torch.Tensor]:
        # x: (B, T, F)
        context = self.encode(x, mask)  # (B, hidden_size)
        reg = self.reg_head(context).view(-1, self.n_horizons, 2)
        cls = self.cls_head(context).view(-1, self.n_horizons, self.n_classes)
        return {"reg": reg, "cls": cls}

    def encode(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        """Run LSTM and return the last hidden state. ``mask`` is unused."""
        lstm_out, _ = self.lstm(x)  # (B, T, hidden_size)
        return lstm_out[:, -1, :]  # (B, hidden_size)

    @property
    def context_size(self) -> int:
        return self.hidden_size


class Seq2SeqLSTMTrackForecaster(TrackForecaster):
    """Encoder-decoder LSTM that generates each horizon step autoregressively.

    The decoder is fed the previous prediction (or teacher-forced target during
    training) so the model learns a sequence of future positions.
    """

    def __init__(
        self,
        n_features: int,
        n_horizons: int,
        n_classes: int,
        hidden_size: int = 128,
        num_layers: int = 2,
        dropout: float = 0.2,
        teacher_forcing_ratio: float = 0.5,
        lat_lon_slice: slice = slice(0, 2),
    ) -> None:
        """Initialise the Seq2Seq forecaster.

        Args:
            lat_lon_slice: slice into the feature dimension that selects the
                lat/lon columns used to seed the decoder.  Defaults to
                ``slice(0, 2)`` which assumes lat/lon are the first two
                features — the same ordering expected by ``TyphoonDataset``
                when ``feature_cols`` is left as ``None`` (auto-build).
                Pass a different slice if you customise ``feature_cols``.
        """
        super().__init__()
        self.n_features = n_features
        self._n_horizons = n_horizons
        self._n_classes = n_classes
        self.hidden_size = hidden_size
        self.teacher_forcing_ratio = teacher_forcing_ratio
        self.lat_lon_slice = lat_lon_slice

        self.encoder = nn.LSTM(
            input_size=n_features,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.decoder = nn.LSTM(
            input_size=2 + n_classes,  # previous lat/lon + previous class one-hot
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.reg_out = nn.Linear(hidden_size, 2)
        self.cls_out = nn.Linear(hidden_size, n_classes)

    def forward(
        self,
        x: torch.Tensor,
        mask: torch.Tensor | None = None,
        y_reg: torch.Tensor | None = None,
        y_cls: torch.Tensor | None = None,
    ) -> dict[str, torch.Tensor]:
        # x: (B, T, F); y_reg/y_cls optional for teacher forcing
        batch_size = x.size(0)
        _, (h, c) = self.encoder(x)

        # Seed decoder with last observed lat/lon position.
        # lat_lon_slice must match the ordering of feature_cols (default: first two = lat/lon).
        last_pos = x[:, -1, self.lat_lon_slice]  # (B, 2)
        # Use a dummy one-hot class vector as initial decoder input
        prev_cls = torch.zeros(batch_size, self.n_classes, device=x.device)
        decoder_input = torch.cat([last_pos, prev_cls], dim=-1).unsqueeze(1)

        reg_outputs: list[torch.Tensor] = []
        cls_outputs: list[torch.Tensor] = []
        for t in range(self.n_horizons):
            dec_out, (h, c) = self.decoder(decoder_input, (h, c))
            step_reg = self.reg_out(dec_out.squeeze(1))
            step_cls = self.cls_out(dec_out.squeeze(1))
            reg_outputs.append(step_reg)
            cls_outputs.append(step_cls)

            # Next decoder input
            if self.training and y_reg is not None and y_cls is not None and torch.rand(1).item() < self.teacher_forcing_ratio:
                next_pos = y_reg[:, t, :]
                next_cls = torch.nn.functional.one_hot(
                    y_cls[:, t].clamp(0, self.n_classes - 1), num_classes=self.n_classes
                ).float()
            else:
                next_pos = step_reg.detach()
                next_cls = torch.nn.functional.softmax(step_cls.detach(), dim=-1)
            decoder_input = torch.cat([next_pos, next_cls], dim=-1).unsqueeze(1)

        return {
            "reg": torch.stack(reg_outputs, dim=1),
            "cls": torch.stack(cls_outputs, dim=1),
        }

    def encode(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        """Not supported: Seq2Seq uses an autoregressive decoder.

        Raises:
            NotImplementedError: always.  Use ``LSTMTrackForecaster`` or
                ``AttentionLSTMTrackForecaster`` with ``QuantileTrackForecaster``.
        """
        raise NotImplementedError(
            "Seq2SeqLSTMTrackForecaster does not support encode(). "
            "Use LSTMTrackForecaster or AttentionLSTMTrackForecaster with QuantileTrackForecaster."
        )

    @property
    def context_size(self) -> int:
        return self.hidden_size


class AttentionLSTMTrackForecaster(TrackForecaster):
    """LSTM encoder with additive attention over the input sequence."""

    def __init__(
        self,
        n_features: int,
        n_horizons: int,
        n_classes: int,
        hidden_size: int = 128,
        num_layers: int = 2,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        self.hidden_size = hidden_size
        self._n_horizons = n_horizons
        self._n_classes = n_classes
        self.encoder = nn.LSTM(
            input_size=n_features,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.attn_query = nn.Linear(hidden_size, hidden_size)
        self.attn_key = nn.Linear(hidden_size, hidden_size)
        self.attn_value = nn.Linear(hidden_size, hidden_size)
        self.reg_head = nn.Linear(hidden_size, n_horizons * 2)
        self.cls_head = nn.Linear(hidden_size, n_horizons * n_classes)

    def forward(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> dict[str, torch.Tensor]:
        context = self.encode(x, mask)  # (B, hidden_size)
        reg = self.reg_head(context).view(-1, self.n_horizons, 2)
        cls = self.cls_head(context).view(-1, self.n_horizons, self.n_classes)
        return {"reg": reg, "cls": cls, "attn": self._last_attn}

    def encode(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        """Run attention-weighted pooling and return the context vector."""
        enc_out, _ = self.encoder(x)  # (B, T, hidden_size)
        last = enc_out[:, -1, :]  # (B, hidden_size)

        # Additive attention: query = last hidden, keys = all encoder outputs
        q = self.attn_query(last).unsqueeze(1)  # (B, 1, H)
        k = self.attn_key(enc_out)  # (B, T, H)
        scores = torch.tanh(q + k).sum(dim=-1)  # (B, T)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float("-inf"))
        attn = torch.softmax(scores, dim=-1)  # (B, T)
        v = self.attn_value(enc_out)  # (B, T, H)
        context = torch.bmm(attn.unsqueeze(1), v).squeeze(1)  # (B, H)
        self._last_attn = attn  # stash for forward() to return
        return context

    @property
    def context_size(self) -> int:
        return self.hidden_size
