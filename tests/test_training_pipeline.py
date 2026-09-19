"""CLI training smoke tests."""

import json
from pathlib import Path

import pytest

from typhoon_vn.cli import main
from typhoon_vn.training.pipeline import load_bundle


def write_config(path: Path, *, extra: str = "") -> None:
    path.write_text(
        f"""
experiment: {{name: smoke-v1, seed: 3, device: cpu}}
dataset: {{input_len: 4, horizon: [1, 2, 4, 8, 12], split_by_year: false, val_ratio: 0.25, test_ratio: 0.0, random_seed: 3}}
model: {{type: LSTMTrackForecaster, hidden_size: 8, num_layers: 1, dropout: 0.0}}
training: {{epochs: 1, batch_size: 32, learning_rate: 0.001, weight_decay: 0.0, patience: 2, gradient_clip: 1.0, scheduler: none, log_every: 99}}
loss: {{reg_loss: smooth_l1, reg_weight: 1.0, cls_weight: 0.3}}
checkpoint: {{dir: ignored, save_last: true, save_best: true}}
mlflow: {{enabled: false, tracking_uri: mlruns, experiment_name: smoke}}
{extra}
""",
        encoding="utf-8",
    )


def test_train_cli_exports_reloadable_bundle(tmp_path, capsys) -> None:
    config = tmp_path / "config.yaml"
    write_config(config)
    output = tmp_path / "run"
    assert main(["train", "--config", str(config), "--output-dir", str(output)]) == 0
    payload = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert payload["data_kind"] == "synthetic-demo"
    bundle = load_bundle(output / "bundle")
    assert bundle["manifest"]["synthetic"] is True
    split = json.loads((output / "bundle" / "split-manifest.json").read_text())
    assert not set(split["train"]) & set(split["val"])


def test_invalid_config_is_nonzero_at_process_boundary(tmp_path) -> None:
    config = tmp_path / "bad.yaml"
    write_config(config, extra="unknown_section: true")
    with pytest.raises(Exception):
        main(["train", "--config", str(config), "--output-dir", str(tmp_path / "out")])
