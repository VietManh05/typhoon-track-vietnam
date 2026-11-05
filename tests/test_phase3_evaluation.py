"""Phase-3 evaluation: scaled backtest and test-split baseline comparison."""

import json
import math

import torch

from typhoon_vn.datasets.synthetic import generate_synthetic_catalogue
from typhoon_vn.datasets.typhoon_dataset import DatasetConfig, TyphoonDataset
from typhoon_vn.evaluation.backtest import backtest_catalogue
from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.models.base import TrackForecaster
from typhoon_vn.models.lstm import LSTMTrackForecaster
from typhoon_vn.training.config_loader import PipelineConfig
from typhoon_vn.training.run import run_training

HORIZONS_H = [6, 12, 24, 48, 72]


class _RecordingModel(TrackForecaster):
    def __init__(self) -> None:
        super().__init__()
        self.seen: list[torch.Tensor] = []
        self._n_horizons = 5
        self._n_classes = 2

    def forward(self, x, mask=None):
        self.seen.append(x.clone())
        batch = x.shape[0]
        return {
            "reg": torch.zeros(batch, 5, 2),
            "cls": torch.zeros(batch, 5, 2),
        }


def test_backtest_feeds_scaled_features_when_scaler_given() -> None:
    frame = generate_synthetic_catalogue(n_storms=3, n_fixes=20, seed=1)
    scaler = FeatureScaler(list(FEATURE_COLUMNS)).fit(
        FeatureBuilder().feature_matrix(frame)
    )
    config = DatasetConfig(feature_cols=tuple(FEATURE_COLUMNS))
    model = _RecordingModel()

    detail, summary = backtest_catalogue(model, frame, config=config, scaler=scaler)

    assert not detail.empty and len(summary) == 5
    x = torch.cat(model.seen)
    # Raw latitudes are ~5-40 degrees; scaled features are roughly standardised.
    assert x[..., 0].abs().max() < 5
    # Targets stay in physical degrees, so errors remain physical kilometres.
    assert detail["actual_lat"].between(-90, 90).all()
    assert detail["actual_lat"].abs().max() > 5


def test_scaled_dataset_keeps_targets_in_physical_degrees() -> None:
    frame = generate_synthetic_catalogue(n_storms=3, n_fixes=20, seed=1)
    scaler = FeatureScaler(list(FEATURE_COLUMNS)).fit(
        FeatureBuilder().feature_matrix(frame)
    )
    config = DatasetConfig(feature_cols=tuple(FEATURE_COLUMNS))
    raw = TyphoonDataset(frame, config)
    scaled = TyphoonDataset(frame, config, scaler=scaler)

    assert len(raw) == len(scaled) > 0
    for a, b in zip(raw.samples, scaled.samples):
        assert (a["y_reg"] == b["y_reg"]).all()
    assert not (raw.samples[0]["x"] == scaled.samples[0]["x"]).all()


def test_residual_lstm_anchors_on_last_physical_position() -> None:
    model = LSTMTrackForecaster(
        n_features=3,
        n_horizons=2,
        n_classes=2,
        hidden_size=4,
        num_layers=1,
        position_mean=[15.0, 120.0],
        position_scale=[5.0, 10.0],
    )
    torch.nn.init.zeros_(model.reg_head.weight)
    torch.nn.init.zeros_(model.reg_head.bias)
    x = torch.zeros(1, 3, 3)
    x[0, 1, :2] = torch.tensor([1.0, 1.0])  # last valid step under the mask
    mask = torch.tensor([[1.0, 1.0, 0.0]])
    reg = model(x, mask)["reg"]
    assert torch.allclose(reg, torch.tensor([[[20.0, 130.0], [20.0, 130.0]]]))


def _config(tmp_path) -> PipelineConfig:
    return PipelineConfig.model_validate(
        {
            "experiment": {"name": "eval-smoke", "seed": 3, "device": "cpu"},
            "dataset": {
                "input_len": 4,
                "horizon": [1, 2, 4, 8, 12],
                "split_by_year": False,
                "val_ratio": 0.25,
                "test_ratio": 0.25,
                "random_seed": 3,
            },
            "model": {
                "type": "LSTMTrackForecaster",
                "hidden_size": 8,
                "num_layers": 1,
                "dropout": 0.0,
            },
            "training": {
                "epochs": 1,
                "batch_size": 32,
                "learning_rate": 0.001,
                "weight_decay": 0.0,
                "patience": 2,
                "gradient_clip": 1.0,
                "scheduler": "none",
                "log_every": 99,
            },
            "loss": {"reg_loss": "smooth_l1", "reg_weight": 1.0, "cls_weight": 0.3},
            "checkpoint": {"dir": str(tmp_path), "save_last": True, "save_best": True},
            "mlflow": {
                "enabled": False,
                "tracking_uri": "mlruns",
                "experiment_name": "x",
            },
        }
    )


def test_run_training_compares_lstm_with_baselines_on_test_split(tmp_path) -> None:
    frame = generate_synthetic_catalogue(n_storms=12, n_fixes=24, seed=3)
    result = run_training(_config(tmp_path), output_dir=tmp_path / "run", frame=frame)

    evaluation = result["evaluation"]
    assert evaluation["split"] == "test"
    assert evaluation["n_storms"] == len(result["split"]["test"]) > 0
    assert set(evaluation["models"]) == {"lstm", "persistence", "cliper"}
    for rows in evaluation["models"].values():
        assert [row["horizon_h"] for row in rows] == HORIZONS_H
        for row in rows:
            assert math.isfinite(row["mean_error_km"]) and row["mean_error_km"] >= 0
            assert row["n_forecasts"] > 0

    on_disk = json.loads((tmp_path / "run" / "evaluation.json").read_text())
    assert on_disk == json.loads(json.dumps(evaluation))


def test_run_training_without_test_split_skips_evaluation(tmp_path) -> None:
    config = _config(tmp_path)
    config.dataset.test_ratio = 0.0
    frame = generate_synthetic_catalogue(n_storms=8, n_fixes=20, seed=3)
    result = run_training(config, output_dir=tmp_path / "run", frame=frame)
    assert result["evaluation"] is None
    assert not (tmp_path / "run" / "evaluation.json").exists()


def test_run_training_exports_best_epoch_weights_not_last(tmp_path) -> None:
    config = _config(tmp_path)
    config.training.epochs = 6
    config.training.patience = 100
    config.training.learning_rate = 0.05  # val loss peaks at epoch 1
    frame = generate_synthetic_catalogue(n_storms=12, n_fixes=24, seed=3)
    result = run_training(config, output_dir=tmp_path / "run", frame=frame)

    checkpoints = tmp_path / "run" / "checkpoints"
    best = torch.load(checkpoints / "best.pt", weights_only=False)
    last = torch.load(checkpoints / "last.pt", weights_only=False)
    exported = torch.load(result["manifest"].parent / "weights.pt", weights_only=True)
    assert best["epoch"] != last["epoch"], "fixture must overfit after best epoch"
    for key, value in best["model_state_dict"].items():
        assert torch.equal(exported[key], value), key
    assert result["best_epoch"] == best["epoch"]


def test_run_training_calibrates_cone_on_validation_and_reports_test_coverage(
    tmp_path,
) -> None:
    config = _config(tmp_path)
    config.uncertainty.coverage = 0.7
    frame = generate_synthetic_catalogue(n_storms=12, n_fixes=24, seed=3)
    result = run_training(config, output_dir=tmp_path / "run", frame=frame)

    manifest = json.loads(result["manifest"].read_text())
    radii = [manifest["validation_radius_km"][str(h)] for h in HORIZONS_H]
    assert all(r > 0 for r in radii) and radii == sorted(radii)
    assert "validation" in manifest["uncertainty_method"]
    assert "70%" in manifest["uncertainty_method"]

    cone = result["evaluation"]["cone"]
    assert cone["coverage_target"] == 0.7
    assert cone["calibration_split"] == "val"
    assert [float(cone["radius_km"][str(h)]) for h in HORIZONS_H] == radii
    assert set(map(int, cone["test_coverage"])) == set(HORIZONS_H)
    assert all(0.0 <= v <= 1.0 for v in cone["test_coverage"].values())
