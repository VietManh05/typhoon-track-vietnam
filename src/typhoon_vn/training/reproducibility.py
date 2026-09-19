"""Reproducibility controls shared by training, tuning and validation."""

from __future__ import annotations

import os
import random

import numpy as np
import torch


def set_global_determinism(seed: int, deterministic: bool = True) -> None:
    """Seed supported RNGs and configure deterministic PyTorch execution."""

    if seed < 0:
        raise ValueError("seed must be non-negative")
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if deterministic:
        os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
    torch.use_deterministic_algorithms(deterministic, warn_only=True)
    torch.backends.cudnn.benchmark = not deterministic
    torch.backends.cudnn.deterministic = deterministic


def seed_worker(worker_id: int) -> None:
    """Seed NumPy/Python in a DataLoader worker from PyTorch's worker seed."""

    del worker_id
    worker_seed = torch.initial_seed() % (2**32)
    np.random.seed(worker_seed)
    random.seed(worker_seed)
