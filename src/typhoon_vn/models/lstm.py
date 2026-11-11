"""LSTM-based track forecasters.

Includes the original single-step LSTM idea (baseline), an encoder-decoder
seq2seq variant for direct multi-horizon output, and an LSTM + attention
variant that can focus on historical fixes.
"""

from __future__ import annotations

import math

import torch
from torch import nn

from typhoon_vn.models.base import TrackForecaster


def _validate_sequence(
    x: torch.Tensor, mask: torch.Tensor | None
) -> tuple[torch.Tensor | None, torch.Tensor]:
    if x.ndim != 3 or x.shape[1] < 1 or x.shape[2] < 1:
        raise ValueError("x must have shape (B, T, F) with non-empty dimensions")
    if not torch.isfinite(x).all():
        raise ValueError("model input must contain only finite values")
    if mask is None:
        lengths = torch.full(
            (x.shape[0],), x.shape[1], dtype=torch.long, device=x.device
        )
        return None, lengths
    if mask.shape != x.shape[:2]:
        raise ValueError("mask must have shape (B, T)")
    valid = mask.to(dtype=torch.bool)
    lengths = valid.sum(dim=1)
    if (lengths < 1).any():
        raise ValueError("each sequence must contain at least one valid timestep")
    expected = torch.arange(x.shape[1], device=x.device).unsqueeze(
        0
    ) < lengths.unsqueeze(1)
    if not torch.equal(valid, expected):
        raise ValueError("mask must describe right-padded contiguous sequences")
    return valid, lengths


def _last_valid(sequence: torch.Tensor, lengths: torch.Tensor) -> torch.Tensor:
    batch = torch.arange(sequence.shape[0], device=sequence.device)
    return sequence[batch, lengths - 1]


def _validate_model_config(
    *,
    n_features: int,
    n_horizons: int,
    n_classes: int,
    hidden_size: int,
    num_layers: int,
    dropout: float,
) -> None:
    if min(n_features, n_horizons, n_classes, hidden_size, num_layers) < 1:
        raise ValueError("model dimensions and num_layers must be positive")
    if not 0 <= dropout < 1:
        raise ValueError("dropout must lie inside [0, 1)")


class LSTMTrackForecaster(TrackForecaster):
    """Baseline LSTM adapted from the sample repo, extended to multi-horizon.

    A single LSTM reads the input window and a fully-connected head emits
    ``n_horizons`` lat/lon pairs plus intensity logits. Real-data bundles may
    anchor positions to the latest fix and a bounded recent-motion estimate;
    the head then learns a correction in WGS84 degrees.
    """

    def __init__(
        self,
        n_features: int,
        n_horizons: int,
        n_classes: int,
        hidden_size: int = 128,
        num_layers: int = 2,
        dropout: float = 0.2,
        anchor_indices: tuple[int, int] | None = None,
        anchor_mean: tuple[float, float] | None = None,
        anchor_scale: tuple[float, float] | None = None,
        anchor_horizon_steps: tuple[int, ...] | None = None,
    ) -> None:
        super().__init__()
        _validate_model_config(
            n_features=n_features,
            n_horizons=n_horizons,
            n_classes=n_classes,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout,
        )
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self._n_horizons = n_horizons
        self._n_classes = n_classes
        anchored = (anchor_indices, anchor_mean, anchor_scale)
        if any(value is not None for value in anchored):
            if any(value is None or len(value) != 2 for value in anchored):
                raise ValueError("anchor indices, mean and scale must be paired")
            if any(
                not isinstance(index, int) or not 0 <= index < n_features
                for index in anchor_indices
            ):
                raise ValueError("anchor indices must identify input features")
            if (
                len(set(anchor_indices)) != 2
                or any(
                    not math.isfinite(value) for value in (*anchor_mean, *anchor_scale)
                )
                or any(value <= 0 for value in anchor_scale)
            ):
                raise ValueError("anchor statistics must be finite and scales positive")
        self.anchor_indices = (
            tuple(anchor_indices) if anchor_indices is not None else None
        )
        if anchor_horizon_steps is not None and (
            self.anchor_indices is None
            or len(anchor_horizon_steps) != n_horizons
            or any(
                not isinstance(step, int) or step < 1 for step in anchor_horizon_steps
            )
        ):
            raise ValueError("anchor horizon steps must match the model horizons")
        self.anchor_horizon_steps = (
            tuple(anchor_horizon_steps) if anchor_horizon_steps is not None else None
        )
        self.register_buffer(
            "anchor_mean",
            torch.tensor(anchor_mean or (0.0, 0.0), dtype=torch.float32),
            persistent=False,
        )
        self.register_buffer(
            "anchor_scale",
            torch.tensor(anchor_scale or (1.0, 1.0), dtype=torch.float32),
            persistent=False,
        )
        self.register_buffer(
            "motion_factors",
            torch.tensor(
                (
                    [
                        3.0 * (1.0 - math.exp(-step / 3.0))
                        for step in anchor_horizon_steps
                    ]
                    if anchor_horizon_steps is not None
                    else []
                ),
                dtype=torch.float32,
            ),
            persistent=False,
        )
        self.lstm = nn.LSTM(
            input_size=n_features,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.reg_head = nn.Linear(hidden_size, n_horizons * 2)
        self.cls_head = nn.Linear(hidden_size, n_horizons * n_classes)
        self.wind_head = nn.Linear(hidden_size, n_horizons)
        self.pressure_head = nn.Linear(hidden_size, n_horizons)

    def forward(
        self, x: torch.Tensor, mask: torch.Tensor | None = None
    ) -> dict[str, torch.Tensor]:
        # x: (B, T, F)
        context = self.encode(x, mask)  # (B, hidden_size)
        reg = self.reg_head(context).view(-1, self.n_horizons, 2)
        if self.anchor_indices is not None:
            _, lengths = _validate_sequence(x, mask)
            last = _last_valid(x, lengths)[:, list(self.anchor_indices)]
            origin = last * self.anchor_scale + self.anchor_mean
            reg = reg + origin.unsqueeze(1)
            if self.anchor_horizon_steps is not None:
                if (lengths < 2).any():
                    raise ValueError("motion anchor requires two valid timesteps")
                previous = x[torch.arange(x.shape[0], device=x.device), lengths - 2]
                velocity = (
                    last - previous[:, list(self.anchor_indices)]
                ) * self.anchor_scale
                reg = reg + velocity.unsqueeze(1) * self.motion_factors.view(1, -1, 1)
        cls = self.cls_head(context).view(-1, self.n_horizons, self.n_classes)
        wind = self.wind_head(context).view(-1, self.n_horizons, 1)
        pressure = self.pressure_head(context).view(-1, self.n_horizons, 1)
        return {"reg": reg, "cls": cls, "wind": wind, "pressure": pressure}

    def encode(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        """Run LSTM and return the last hidden state. ``mask`` is unused."""
        _, lengths = _validate_sequence(x, mask)
        lstm_out, _ = self.lstm(x)  # (B, T, hidden_size)
        return _last_valid(lstm_out, lengths)  # (B, hidden_size)

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
        _validate_model_config(
            n_features=n_features,
            n_horizons=n_horizons,
            n_classes=n_classes,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout,
        )
        if not 0 <= teacher_forcing_ratio <= 1:
            raise ValueError("teacher_forcing_ratio must lie inside [0, 1]")
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
        _, lengths = _validate_sequence(x, mask)
        packed = nn.utils.rnn.pack_padded_sequence(
            x, lengths.cpu(), batch_first=True, enforce_sorted=False
        )
        _, (h, c) = self.encoder(packed)

        # Seed decoder with last observed lat/lon position.
        # lat_lon_slice must match the ordering of feature_cols (default: first two = lat/lon).
        last_pos = _last_valid(x, lengths)[:, self.lat_lon_slice]  # (B, 2)
        if last_pos.shape[-1] != 2:
            raise ValueError("lat_lon_slice must select exactly two features")
        if self.training and ((y_reg is None) != (y_cls is None)):
            raise ValueError("teacher forcing requires both y_reg and y_cls")
        if y_reg is not None and y_reg.shape != (batch_size, self.n_horizons, 2):
            raise ValueError("y_reg has an invalid teacher-forcing shape")
        if y_cls is not None and y_cls.shape != (batch_size, self.n_horizons):
            raise ValueError("y_cls has an invalid teacher-forcing shape")
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
            if (
                self.training
                and y_reg is not None
                and y_cls is not None
                and torch.rand(1).item() < self.teacher_forcing_ratio
            ):
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
        _validate_model_config(
            n_features=n_features,
            n_horizons=n_horizons,
            n_classes=n_classes,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout,
        )
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

    def forward(
        self, x: torch.Tensor, mask: torch.Tensor | None = None
    ) -> dict[str, torch.Tensor]:
        context = self.encode(x, mask)  # (B, hidden_size)
        reg = self.reg_head(context).view(-1, self.n_horizons, 2)
        cls = self.cls_head(context).view(-1, self.n_horizons, self.n_classes)
        return {"reg": reg, "cls": cls, "attn": self._last_attn}

    def encode(self, x: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        """Run attention-weighted pooling and return the context vector."""
        valid, lengths = _validate_sequence(x, mask)
        enc_out, _ = self.encoder(x)  # (B, T, hidden_size)
        last = _last_valid(enc_out, lengths)  # (B, hidden_size)

        # Additive attention: query = last hidden, keys = all encoder outputs
        q = self.attn_query(last).unsqueeze(1)  # (B, 1, H)
        k = self.attn_key(enc_out)  # (B, T, H)
        scores = torch.tanh(q + k).sum(dim=-1)  # (B, T)
        if valid is not None:
            scores = scores.masked_fill(~valid, float("-inf"))
        attn = torch.softmax(scores, dim=-1)  # (B, T)
        v = self.attn_value(enc_out)  # (B, T, H)
        context = torch.bmm(attn.unsqueeze(1), v).squeeze(1)  # (B, H)
        self._last_attn = attn  # stash for forward() to return
        return context

    @property
    def context_size(self) -> int:
        return self.hidden_size
