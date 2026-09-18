"""Deterministic checkpoint/resume contract tests."""

from __future__ import annotations

import random

import numpy as np
import pytest
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset

from typhoon_vn.models.base import TrackForecaster
from typhoon_vn.training.losses import MultiHorizonLoss
from typhoon_vn.training.trainer import Trainer, TrainingConfig


class TinyDataset(Dataset):
    def __init__(self, length: int = 8, nonfinite: bool = False) -> None:
        generator = torch.Generator().manual_seed(7)
        self.x = torch.randn(length, 3, 2, generator=generator)
        self.y_reg = self.x[:, -1:, :].clone()
        if nonfinite:
            self.y_reg[:] = float("nan")
        self.y_cls = torch.zeros(length, 1, dtype=torch.long)

    def __len__(self) -> int:
        return len(self.x)

    def __getitem__(self, index: int) -> dict[str, torch.Tensor]:
        return {
            "x": self.x[index],
            "mask": torch.ones(3),
            "y_reg": self.y_reg[index],
            "y_cls": self.y_cls[index],
        }


class TinyForecaster(TrackForecaster):
    def __init__(self) -> None:
        super().__init__()
        self._n_horizons = 1
        self._n_classes = 2
        self.dropout = nn.Dropout(0.2)
        self.reg = nn.Linear(2, 2)
        self.cls = nn.Linear(2, 2)

    def encode(self, x, mask=None):
        return self.dropout(x[:, -1])

    @property
    def context_size(self):
        return 2

    def forward(self, x, mask=None):
        context = self.encode(x, mask)
        return {"reg": self.reg(context).unsqueeze(1), "cls": self.cls(context).unsqueeze(1)}


def seed_all(seed: int = 11) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def make_trainer(path, model=None) -> Trainer:
    return Trainer(
        model or TinyForecaster(),
        TrainingConfig(
            epochs=2, learning_rate=1e-2, patience=3, scheduler="cosine",
            device="cpu", checkpoint_dir=path, log_every=99,
        ),
        MultiHorizonLoss(n_horizons=1, n_classes=2),
    )


def test_continuous_matches_one_plus_resume(tmp_path) -> None:
    loader = DataLoader(TinyDataset(), batch_size=2, shuffle=False)

    seed_all()
    continuous = make_trainer(tmp_path / "continuous")
    continuous.fit(loader, loader)

    seed_all()
    first = make_trainer(tmp_path / "resumed")
    first.fit(loader, loader, max_epochs=1)
    checkpoint = first.config.checkpoint_dir / "last.pt"
    saved = torch.load(checkpoint, weights_only=False)
    assert saved["history"][-1]["epoch"] == 1
    assert saved["scheduler_state_dict"]["last_epoch"] == 1

    # Deliberately perturb every RNG; load_checkpoint must restore all of them.
    random.random(); np.random.random(); torch.rand(3)
    resumed = make_trainer(tmp_path / "resumed", TinyForecaster())
    resumed.load_checkpoint(checkpoint)
    resumed.fit(loader, loader)

    assert resumed.history == pytest.approx(continuous.history)
    assert resumed.best_epoch == continuous.best_epoch
    assert resumed.patience_counter == continuous.patience_counter
    assert resumed.optimizer.param_groups[0]["lr"] == pytest.approx(
        continuous.optimizer.param_groups[0]["lr"]
    )
    for name, value in continuous.model.state_dict().items():
        torch.testing.assert_close(resumed.model.state_dict()[name], value, rtol=0, atol=1e-7)


def test_empty_and_nonfinite_validation_are_rejected(tmp_path) -> None:
    train = DataLoader(TinyDataset(), batch_size=2)
    empty = DataLoader(TinyDataset(length=0), batch_size=2)
    with pytest.raises(ValueError, match="validation loader"):
        make_trainer(tmp_path / "empty").fit(train, empty)

    bad = DataLoader(TinyDataset(nonfinite=True), batch_size=2)
    trainer = make_trainer(tmp_path / "bad")
    with pytest.raises(ValueError, match="validation metrics must be finite"):
        trainer.fit(train, bad)
    assert not (tmp_path / "bad" / "best.pt").exists()


def test_checkpoint_contract_rejects_scheduler_mismatch(tmp_path) -> None:
    loader = DataLoader(TinyDataset(), batch_size=2)
    source = make_trainer(tmp_path / "source")
    source.fit(loader, loader, max_epochs=1)
    target = Trainer(
        TinyForecaster(),
        TrainingConfig(epochs=2, scheduler="none", device="cpu", checkpoint_dir=tmp_path / "target"),
        MultiHorizonLoss(1, 2),
    )
    with pytest.raises(ValueError, match="scheduler"):
        target.load_checkpoint(tmp_path / "source" / "last.pt")
