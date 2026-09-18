"""End-to-end Phase 3 demo: dataset, model, training, evaluation.

This script:
  1. Generates a synthetic storm catalogue.
  2. Splits it by storm ID (no leakage).
  3. Builds multi-horizon datasets.
  4. Trains three Phase-3 models (baseline LSTM, Seq2Seq, Attention LSTM).
  5. Evaluates track error per horizon and prints a cone sample.

Run from the repo root:
    python scripts/run_phase3_demo.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow running the demo before the package is installed.
SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import numpy as np
import torch
from torch.utils.data import DataLoader

from typhoon_vn.datasets.synthetic import generate_synthetic_catalogue
from typhoon_vn.datasets.typhoon_dataset import (
    DatasetConfig,
    TyphoonDataset,
    collate_fn,
    split_by_storm_or_year,
)
from typhoon_vn.evaluation.metrics import intensity_accuracy, track_error_km
from typhoon_vn.models.lstm import (
    AttentionLSTMTrackForecaster,
    LSTMTrackForecaster,
    Seq2SeqLSTMTrackForecaster,
)
from typhoon_vn.models.uncertainty import build_cone, cone_radius_km, mc_dropout_predict
from typhoon_vn.training.losses import MultiHorizonLoss
from typhoon_vn.training.trainer import Trainer, TrainingConfig


def run() -> None:
    print("=" * 60)
    print("Typhoon VN Forecast System — Phase 3 Demo")
    print("=" * 60)

    # 1. Synthetic catalogue
    df = generate_synthetic_catalogue(n_storms=40, n_fixes=45, seed=42)
    print(f"Generated synthetic catalogue: {len(df)} fixes across {df['storm_id'].nunique()} storms")

    # 2. Split by storm ID
    train_df, val_df, test_df = split_by_storm_or_year(
        df, val_ratio=0.15, test_ratio=0.15, by_year=False, random_seed=7
    )
    print(f"Train storms: {train_df['storm_id'].nunique()}, val: {val_df['storm_id'].nunique()}, test: {test_df['storm_id'].nunique()}")

    # 3. Multi-horizon dataset
    config = DatasetConfig(input_len=6, horizon=(1, 2, 4, 8, 12))  # 6h, 12h, 24h, 48h, 72h
    train_ds = TyphoonDataset(train_df, config=config)
    val_ds = TyphoonDataset(val_df, config=config)
    test_ds = TyphoonDataset(test_df, config=config)
    print(f"Train samples: {len(train_ds)}, val: {len(val_ds)}, test: {len(test_ds)}")
    print(f"Features: {train_ds.n_features}, horizons: {train_ds.n_horizons}, classes: {train_ds.n_classes}")

    train_loader = DataLoader(train_ds, batch_size=16, shuffle=True, collate_fn=collate_fn)
    val_loader = DataLoader(val_ds, batch_size=16, shuffle=False, collate_fn=collate_fn)
    test_loader = DataLoader(test_ds, batch_size=16, shuffle=False, collate_fn=collate_fn)

    loss_fn = MultiHorizonLoss(
        n_horizons=train_ds.n_horizons,
        n_classes=train_ds.n_classes,
        reg_loss="smooth_l1",
        reg_weight=1.0,
        cls_weight=0.2,
    )

    models = {
        "Baseline LSTM": LSTMTrackForecaster(
            n_features=train_ds.n_features,
            n_horizons=train_ds.n_horizons,
            n_classes=train_ds.n_classes,
            hidden_size=64,
            num_layers=2,
            dropout=0.2,
        ),
        "Seq2Seq LSTM": Seq2SeqLSTMTrackForecaster(
            n_features=train_ds.n_features,
            n_horizons=train_ds.n_horizons,
            n_classes=train_ds.n_classes,
            hidden_size=64,
            num_layers=2,
            dropout=0.2,
            teacher_forcing_ratio=0.5,
        ),
        "Attention LSTM": AttentionLSTMTrackForecaster(
            n_features=train_ds.n_features,
            n_horizons=train_ds.n_horizons,
            n_classes=train_ds.n_classes,
            hidden_size=64,
            num_layers=2,
            dropout=0.2,
        ),
    }

    results: dict[str, dict[str, object]] = {}
    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        trainer_config = TrainingConfig(
            epochs=30,
            batch_size=16,
            learning_rate=1e-3,
            patience=7,
            gradient_clip=1.0,
            scheduler="cosine",
            device="auto",
            checkpoint_dir=Path("checkpoints") / name.replace(" ", "_").lower(),
            log_every=5,
        )
        trainer = Trainer(model, trainer_config, loss_fn)
        fit_result = trainer.fit(train_loader, val_loader)
        print(f"Best val loss: {fit_result['best_val_loss']:.4f} at epoch {fit_result['best_epoch']}")

        # Evaluate on test set
        model.eval()
        all_pred_reg: list[torch.Tensor] = []
        all_actual_reg: list[torch.Tensor] = []
        all_pred_cls: list[torch.Tensor] = []
        all_actual_cls: list[torch.Tensor] = []
        with torch.no_grad():
            for batch in test_loader:
                out = model(batch["x"].to(trainer.device), batch["mask"].to(trainer.device))
                all_pred_reg.append(out["reg"].cpu())
                all_actual_reg.append(batch["y_reg"])
                all_pred_cls.append(out["cls"].cpu())
                all_actual_cls.append(batch["y_cls"])

        pred_reg = torch.cat(all_pred_reg, dim=0).numpy()
        actual_reg = torch.cat(all_actual_reg, dim=0).numpy()
        pred_cls = torch.cat(all_pred_cls, dim=0).numpy()
        actual_cls = torch.cat(all_actual_cls, dim=0).numpy()

        errors = track_error_km(pred_reg, actual_reg)
        mean_errors = errors.mean(axis=0)
        acc = intensity_accuracy(pred_cls, actual_cls)

        horizon_hours = [6 * h for h in config.horizon]
        print(f"Mean track error (km) by horizon: {dict(zip(horizon_hours, [round(float(e), 1) for e in mean_errors]))}")
        print(f"Intensity accuracy by horizon: {dict(zip(horizon_hours, [round(float(a), 3) for a in acc]))}")

        results[name] = {
            "best_val_loss": float(fit_result["best_val_loss"]),
            "best_epoch": int(fit_result["best_epoch"]),
            "mean_track_error_km": [float(e) for e in mean_errors],
            "intensity_accuracy": [float(a) for a in acc],
        }

    # 4. Uncertainty / cone demo on the first test sample
    print("\n--- Uncertainty cone demo (Attention LSTM + MC Dropout) ---")
    test_sample = test_ds[0]
    x = torch.from_numpy(test_sample["x"]).unsqueeze(0).to(trainer.device)
    mask = torch.from_numpy(test_sample["mask"]).unsqueeze(0).to(trainer.device)
    attn_model = models["Attention LSTM"]
    attn_model.to(trainer.device)
    mc_result = mc_dropout_predict(attn_model, x, mask, n_samples=30)
    means = mc_result["reg_mean"].squeeze(0).cpu().numpy()
    stds = mc_result["reg_std"].squeeze(0).cpu().numpy()
    for i, h in enumerate(config.horizon):
        hours = 6 * h
        lat, lon = float(means[i, 0]), float(means[i, 1])
        radius = cone_radius_km(hours)
        cone = build_cone(lat, lon, radius, n_points=16)
        print(
            f"  {hours}h: center=({lat:.2f}, {lon:.2f}), "
            f"std=({stds[i, 0]:.3f}, {stds[i, 1]:.3f}), cone_radius={radius:.1f} km"
        )

    # Save results
    out_path = Path("checkpoints") / "phase3_demo_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nSaved results to {out_path}")


if __name__ == "__main__":
    run()
