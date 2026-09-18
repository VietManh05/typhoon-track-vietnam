"""Reusable training loop with deterministic checkpoint/resume support."""

from __future__ import annotations

import dataclasses
import math
import os
import random
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import optim
from torch.utils.data import DataLoader

from typhoon_vn.models.base import TrackForecaster
from typhoon_vn.training.losses import MultiHorizonLoss


@dataclasses.dataclass(frozen=True)
class TrainingConfig:
    """Hyperparameters for the trainer."""

    epochs: int = 100
    batch_size: int = 32
    learning_rate: float = 1e-3
    weight_decay: float = 1e-5
    patience: int = 10
    gradient_clip: float = 1.0
    scheduler: str = "cosine"  # "cosine", "plateau", "none"
    device: str = "auto"
    checkpoint_dir: Path | None = None
    log_every: int = 10


class Trainer:
    """Train a ``TrackForecaster`` with early stopping and resumable state."""

    CHECKPOINT_VERSION = 2

    def __init__(
        self,
        model: TrackForecaster,
        config: TrainingConfig,
        loss_fn: MultiHorizonLoss,
        optimizer: optim.Optimizer | None = None,
    ) -> None:
        if config.epochs < 1:
            raise ValueError("epochs must be positive")
        if config.patience < 1:
            raise ValueError("patience must be positive")
        if config.scheduler not in {"cosine", "plateau", "none"}:
            raise ValueError(f"unsupported scheduler: {config.scheduler}")
        self.model = model
        self.config = config
        self.loss_fn = loss_fn
        self.optimizer = optimizer or optim.AdamW(
            model.parameters(),
            lr=config.learning_rate,
            weight_decay=config.weight_decay,
        )
        self.device = self._resolve_device(config.device)
        self.model.to(self.device)
        self.history: list[dict[str, float]] = []
        self.best_val_loss = float("inf")
        self.best_epoch = 0
        self.patience_counter = 0
        self.start_epoch = 1

        if config.scheduler == "cosine":
            self.scheduler: Any = optim.lr_scheduler.CosineAnnealingLR(
                self.optimizer, T_max=config.epochs
            )
        elif config.scheduler == "plateau":
            self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
                self.optimizer, mode="min", factor=0.5, patience=3
            )
        else:
            self.scheduler = None

    @staticmethod
    def _resolve_device(device: str) -> torch.device:
        if device == "auto":
            return torch.device("cuda" if torch.cuda.is_available() else "cpu")
        return torch.device(device)

    def _run_epoch(self, loader: DataLoader, training: bool = True) -> dict[str, float]:
        self.model.train(training)
        totals = {"loss": 0.0, "reg_loss": 0.0, "cls_loss": 0.0}
        n_batches = 0

        with torch.set_grad_enabled(training):
            for batch in loader:
                x = batch["x"].to(self.device)
                mask = batch["mask"].to(self.device)
                y_reg = batch["y_reg"].to(self.device)
                y_cls = batch["y_cls"].to(self.device)
                if training:
                    self.optimizer.zero_grad()
                out = self.model(x, mask)
                loss, metrics = self.loss_fn(
                    out["reg"], out["cls"], y_reg, y_cls
                )
                metric_values = {
                    name: float(metrics[name].detach().item()) for name in totals
                }
                if not all(math.isfinite(value) for value in metric_values.values()):
                    kind = "training" if training else "validation"
                    raise ValueError(f"{kind} metrics must be finite")
                if training:
                    loss.backward()
                    if self.config.gradient_clip > 0:
                        torch.nn.utils.clip_grad_norm_(
                            self.model.parameters(), self.config.gradient_clip
                        )
                    self.optimizer.step()
                for name, value in metric_values.items():
                    totals[name] += value
                n_batches += 1

        if n_batches == 0:
            kind = "training" if training else "validation"
            raise ValueError(f"{kind} loader must contain at least one batch")
        return {name: value / n_batches for name, value in totals.items()}

    def fit(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader | None = None,
        epoch_callback: Callable[
            [int, dict[str, float], dict[str, float] | None], None
        ]
        | None = None,
        max_epochs: int | None = None,
    ) -> dict[str, Any]:
        """Train through the configured epoch, or pause at ``max_epochs``.

        ``max_epochs`` is an absolute epoch number and enables a deterministic
        pause/resume test without changing the scheduler's configured horizon.
        """

        final_epoch = self.config.epochs
        if max_epochs is not None:
            if max_epochs < self.start_epoch:
                raise ValueError("max_epochs precedes the next resume epoch")
            final_epoch = min(final_epoch, max_epochs)

        for epoch in range(self.start_epoch, final_epoch + 1):
            train_metrics = self._run_epoch(train_loader, training=True)
            val_metrics = None
            improved = False
            if val_loader is not None:
                val_metrics = self._run_epoch(val_loader, training=False)
                val_loss = val_metrics["loss"]
                improved = val_loss < self.best_val_loss
                if improved:
                    self.best_val_loss = val_loss
                    self.best_epoch = epoch
                    self.patience_counter = 0
                else:
                    self.patience_counter += 1

            if self.scheduler is not None:
                if self.config.scheduler == "plateau":
                    if val_metrics is None:
                        raise ValueError("plateau scheduler requires a validation loader")
                    self.scheduler.step(val_metrics["loss"])
                else:
                    self.scheduler.step()

            record = {"epoch": epoch, **train_metrics}
            if val_metrics is not None:
                record.update({f"val_{k}": v for k, v in val_metrics.items()})
            record["learning_rate"] = float(self.optimizer.param_groups[0]["lr"])
            self.history.append(record)
            self.start_epoch = epoch + 1

            if epoch_callback is not None:
                epoch_callback(epoch, train_metrics, val_metrics)
            elif epoch % self.config.log_every == 0 or epoch == 1:
                message = (
                    f"Epoch {epoch}/{self.config.epochs}  "
                    f"train_loss={train_metrics['loss']:.4f}"
                )
                if val_metrics is not None:
                    message += f"  val_loss={val_metrics['loss']:.4f}"
                print(message)

            # Save only after scheduler/history/early-stop state is complete.
            if improved:
                self.save_checkpoint("best", current_epoch=epoch)
            self.save_checkpoint("last", current_epoch=epoch)

            if val_loader is not None and self.patience_counter >= self.config.patience:
                print(f"Early stopping at epoch {epoch} (best={self.best_epoch})")
                break

        return {
            "history": self.history,
            "best_epoch": self.best_epoch,
            "best_val_loss": self.best_val_loss,
        }

    @staticmethod
    def _rng_state() -> dict[str, Any]:
        state: dict[str, Any] = {
            "python": random.getstate(),
            "numpy": np.random.get_state(),
            "torch": torch.get_rng_state(),
        }
        if torch.cuda.is_available():
            state["cuda"] = torch.cuda.get_rng_state_all()
        return state

    @staticmethod
    def _restore_rng_state(state: dict[str, Any]) -> None:
        random.setstate(state["python"])
        np.random.set_state(state["numpy"])
        torch.set_rng_state(state["torch"])
        if "cuda" in state and torch.cuda.is_available():
            torch.cuda.set_rng_state_all(state["cuda"])

    def save_checkpoint(self, tag: str, current_epoch: int | None = None) -> Path:
        """Atomically persist all state required for an exact local resume."""

        directory = self.config.checkpoint_dir or Path("checkpoints")
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{tag}.pt"
        temporary = path.with_suffix(path.suffix + ".tmp")
        epoch = current_epoch if current_epoch is not None else self.start_epoch - 1
        payload = {
            "checkpoint_version": self.CHECKPOINT_VERSION,
            "epoch": epoch,
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "scheduler_state_dict": (
                self.scheduler.state_dict() if self.scheduler is not None else None
            ),
            "scheduler_kind": self.config.scheduler,
            "best_val_loss": self.best_val_loss,
            "best_epoch": self.best_epoch,
            "patience_counter": self.patience_counter,
            "history": self.history,
            "rng_state": self._rng_state(),
        }
        torch.save(payload, temporary)
        os.replace(temporary, path)
        return path

    def load_checkpoint(self, path: Path) -> None:
        """Load a trusted, locally generated checkpoint and restore RNG state."""

        checkpoint = torch.load(path, map_location=self.device, weights_only=False)
        required = {
            "checkpoint_version",
            "epoch",
            "model_state_dict",
            "optimizer_state_dict",
            "scheduler_state_dict",
            "scheduler_kind",
            "best_val_loss",
            "best_epoch",
            "patience_counter",
            "history",
            "rng_state",
        }
        missing = sorted(required.difference(checkpoint))
        if missing:
            raise ValueError(f"checkpoint is missing required state: {missing}")
        if checkpoint["checkpoint_version"] != self.CHECKPOINT_VERSION:
            raise ValueError("unsupported checkpoint version")
        if checkpoint["scheduler_kind"] != self.config.scheduler:
            raise ValueError("checkpoint scheduler does not match TrainingConfig")

        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        scheduler_state = checkpoint["scheduler_state_dict"]
        if self.scheduler is not None:
            if scheduler_state is None:
                raise ValueError("checkpoint has no scheduler state")
            self.scheduler.load_state_dict(scheduler_state)
        elif scheduler_state is not None:
            raise ValueError("checkpoint unexpectedly contains scheduler state")
        self.best_val_loss = float(checkpoint["best_val_loss"])
        self.best_epoch = int(checkpoint["best_epoch"])
        self.patience_counter = int(checkpoint["patience_counter"])
        self.history = list(checkpoint["history"])
        self.start_epoch = int(checkpoint["epoch"]) + 1
        self._restore_rng_state(checkpoint["rng_state"])
