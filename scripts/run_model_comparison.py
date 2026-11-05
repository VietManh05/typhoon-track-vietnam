"""Compare track-forecasting methods on real IBTrACS WP storms.

Methods (all scored on the same test windows, displacement formulation):

* baselines: persistence, CLIPER-style damped persistence (no learning)
* classical AI: k-NN analog (case-based reasoning, tuned on validation) and
  gradient-boosted trees
* neural: LSTM, Attention-LSTM, Transformer (residual wrapper)

Data: IBTrACS WP, whole storms split by final year (latest ~10% of years =
test, the ~10% before = validation). Learned methods are run with several
seeds; results are reported as mean ± std over seeds for all test storms and
for the subset of storms passing within ``--vn-km`` of Vietnam's coastline.

Usage::

    python scripts/run_model_comparison.py --data-root data \
        --output-dir runs/model-comparison --seeds 0 1 2
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset

from typhoon_vn.datasets.ibtracs import load_ibtracs_tracks
from typhoon_vn.datasets.typhoon_dataset import DatasetConfig, split_by_storm_or_year
from typhoon_vn.evaluation.comparison import (
    Windows,
    build_windows,
    errors_km,
    vietnam_storms,
)
from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.models.baselines import CLIPERForecaster, PersistenceForecaster
from typhoon_vn.models.classical import AnalogForecaster, GradientBoostingForecaster
from typhoon_vn.models.lstm import AttentionLSTMTrackForecaster, LSTMTrackForecaster
from typhoon_vn.models.residual import ResidualTrackForecaster
from typhoon_vn.models.transformer import TransformerTrackForecaster
from typhoon_vn.training.losses import MultiHorizonLoss
from typhoon_vn.training.pipeline import position_stats
from typhoon_vn.training.reproducibility import set_global_determinism
from typhoon_vn.training.trainer import Trainer, TrainingConfig

HORIZON_STEPS = [1, 2, 4, 8, 12]
HORIZONS_H = [6 * step for step in HORIZON_STEPS]
NEURAL = {
    "lstm": lambda f, h, c: LSTMTrackForecaster(
        f, h, c, hidden_size=128, num_layers=2, dropout=0.2
    ),
    "attention_lstm": lambda f, h, c: AttentionLSTMTrackForecaster(
        f, h, c, hidden_size=128, num_layers=2, dropout=0.2
    ),
    "transformer": lambda f, h, c: TransformerTrackForecaster(
        f, h, c, d_model=64, nhead=4, n_layers=2, dim_feedforward=128, dropout=0.1
    ),
}
LABELS = {
    "persistence": "Persistence (baseline)",
    "cliper": "CLIPER-proxy (baseline)",
    "analog_knn": "k-NN analog (case-based)",
    "gradient_boosting": "Gradient boosting",
    "lstm": "LSTM",
    "attention_lstm": "Attention-LSTM",
    "transformer": "Transformer",
}


def _loader(windows: Windows, shuffle: bool, seed: int, batch_size: int = 64):
    dataset = TensorDataset(
        torch.tensor(windows.x_scaled, dtype=torch.float32),
        torch.ones(windows.x_scaled.shape[:2]),
        torch.tensor(windows.y, dtype=torch.float32),
        torch.zeros(windows.y.shape[:2], dtype=torch.long),
    )
    generator = torch.Generator().manual_seed(seed)

    def collate(rows):
        x, mask, y, cls = map(torch.stack, zip(*rows))
        return {"x": x, "mask": mask, "y_reg": y, "y_cls": cls}

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        generator=generator,
        collate_fn=collate,
    )


def train_neural(name, train, val, scaler, seed, epochs, workdir) -> torch.nn.Module:
    set_global_determinism(seed)
    base = NEURAL[name](len(FEATURE_COLUMNS), len(HORIZON_STEPS), 2)
    stats = position_stats(scaler)
    model = ResidualTrackForecaster(
        base, stats["position_mean"], stats["position_scale"]
    )
    # Track-only comparison: dummy 2-class head with zero classification weight.
    loss = MultiHorizonLoss(len(HORIZON_STEPS), 2, reg_loss="smooth_l1", cls_weight=0.0)
    checkpoints = workdir / f"{name}-seed{seed}"
    trainer = Trainer(
        model,
        TrainingConfig(
            epochs=epochs,
            batch_size=64,
            learning_rate=1e-3,
            weight_decay=1e-5,
            patience=10,
            gradient_clip=1.0,
            scheduler="cosine",
            device="cpu",
            checkpoint_dir=checkpoints,
            log_every=1000,
        ),
        loss,
    )
    trainer.fit(_loader(train, True, seed), _loader(val, False, seed))
    # Checkpoint written by this process just above (holds RNG state).
    best = torch.load(checkpoints / "best.pt", map_location="cpu", weights_only=False)
    model.load_state_dict(best["model_state_dict"])
    return model.eval()


def predict_neural(model, windows: Windows) -> np.ndarray:
    with torch.no_grad():
        x = torch.tensor(windows.x_scaled, dtype=torch.float32)
        return model(x, torch.ones(x.shape[:2]))["reg"].numpy().astype(float)


def predict_baseline(model, windows: Windows) -> np.ndarray:
    with torch.no_grad():
        x = torch.tensor(windows.x_raw, dtype=torch.float32)
        return model(x)["reg"].numpy().astype(float)


def tune_analog(train: Windows, val: Windows) -> tuple[AnalogForecaster, dict]:
    best, best_score, grid = None, np.inf, []
    for k, position, season in itertools.product(
        (5, 10, 20, 40), (0.5, 1.0, 2.0), (0.0, 0.5, 1.0)
    ):
        model = AnalogForecaster(
            k=k, weights={"track": 1.0, "position": position, "season": season}
        ).fit(train.x_raw, train.y, train.storm_ids, train.issue_times)
        score = float(errors_km(model.predict(val.x_raw), val).mean())
        grid.append({"k": k, "position": position, "season": season, "val_km": score})
        if score < best_score:
            best, best_score = model, score
    return best, {"selected": grid[[g["val_km"] for g in grid].index(best_score)]}


def _table(results: dict, subset: str) -> list[str]:
    header = "| method | " + " | ".join(f"{h}h" for h in HORIZONS_H) + " |"
    lines = [header, "|---|" + "---:|" * len(HORIZONS_H)]
    for name, runs in results.items():
        values = np.array([[run[subset][str(h)] for h in HORIZONS_H] for run in runs])
        cells = []
        for column in values.T:
            if len(column) > 1:
                cells.append(f"{column.mean():.0f} ± {column.std(ddof=1):.0f}")
            else:
                cells.append(f"{column.mean():.0f}")
        lines.append(f"| {LABELS[name]} | " + " | ".join(cells) + " |")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--years", type=int, nargs=2, default=(1980, 2024))
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--vn-km", type=float, default=300.0)
    parser.add_argument("--neural", nargs="*", default=list(NEURAL))
    args = parser.parse_args(argv)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()

    _, cleaned, _ = load_ibtracs_tracks(args.data_root, tuple(args.years))
    train_f, val_f, test_f = split_by_storm_or_year(
        cleaned, val_ratio=0.1, test_ratio=0.1, by_year=True
    )
    scaler = FeatureScaler(list(FEATURE_COLUMNS)).fit(
        FeatureBuilder().feature_matrix(train_f)
    )
    config = DatasetConfig(
        input_len=4, horizon=tuple(HORIZON_STEPS), feature_cols=tuple(FEATURE_COLUMNS)
    )
    train, val, test = (
        build_windows(f, config, scaler) for f in (train_f, val_f, test_f)
    )
    vn = vietnam_storms(test_f, within_km=args.vn_km)
    vn_mask = np.isin(test.storm_ids, sorted(vn))
    final_year = cleaned.groupby("storm_id")["timestamp"].max().dt.year
    print(
        f"windows train/val/test={len(train)}/{len(val)}/{len(test)}; "
        f"VN test storms={len(vn)} ({int(vn_mask.sum())} windows)",
        flush=True,
    )

    results: dict[str, list[dict]] = {}
    predictions: dict[str, np.ndarray] = {}

    def record(name: str, seed: int | None, predicted: np.ndarray) -> None:
        error = errors_km(predicted, test)
        run = {
            "seed": seed,
            "all": {
                str(h): float(error[:, i].mean()) for i, h in enumerate(HORIZONS_H)
            },
            "vietnam": {
                str(h): float(error[vn_mask, i].mean())
                for i, h in enumerate(HORIZONS_H)
            },
        }
        results.setdefault(name, []).append(run)
        if name not in predictions:
            predictions[name] = predicted
        print(
            f"{name:18s} seed={seed} 24h={run['all']['24']:.0f} "
            f"72h={run['all']['72']:.0f} km",
            flush=True,
        )

    steps, n = HORIZON_STEPS, len(HORIZON_STEPS)
    record(
        "persistence",
        None,
        predict_baseline(PersistenceForecaster(n, 1, horizon_steps=steps), test),
    )
    record(
        "cliper",
        None,
        predict_baseline(CLIPERForecaster(n, 1, horizon_steps=steps), test),
    )

    analog, analog_info = tune_analog(train, val)
    record("analog_knn", None, analog.predict(test.x_raw))

    for seed in args.seeds:
        boosting = GradientBoostingForecaster(random_state=seed).fit(
            train.x_raw, train.y
        )
        record("gradient_boosting", seed, boosting.predict(test.x_raw))

    for name in args.neural:
        for seed in args.seeds:
            model = train_neural(
                name, train, val, scaler, seed, args.epochs, out / "checkpoints"
            )
            record(name, seed, predict_neural(model, test))

    # Per-window predictions (first seed of each method) for error analysis.
    rows = []
    for name, predicted in predictions.items():
        error = errors_km(predicted, test)
        for i in range(len(test)):
            for j, h in enumerate(HORIZONS_H):
                rows.append(
                    {
                        "method": name,
                        "storm_id": test.storm_ids[i],
                        "issue_time": pd.Timestamp(test.issue_times[i]).isoformat(),
                        "horizon_h": h,
                        "pred_lat": predicted[i, j, 0],
                        "pred_lon": predicted[i, j, 1],
                        "obs_lat": float(test.y[i, j, 0]),
                        "obs_lon": float(test.y[i, j, 1]),
                        "error_km": float(error[i, j]),
                    }
                )
    pd.DataFrame(rows).to_csv(out / "test_predictions.csv", index=False)
    test_f.to_csv(out / "test_tracks.csv", index=False)

    summary = {
        "years": list(args.years),
        "test_years": sorted(set(final_year[sorted(set(test.storm_ids))].tolist())),
        "storms": {
            "train": int(train_f.storm_id.nunique()),
            "val": int(val_f.storm_id.nunique()),
            "test": int(test_f.storm_id.nunique()),
            "test_vietnam": len(vn),
        },
        "windows": {
            "train": len(train),
            "val": len(val),
            "test": len(test),
            "test_vietnam": int(vn_mask.sum()),
        },
        "vietnam_definition_km": args.vn_km,
        "seeds": args.seeds,
        "analog": analog_info,
        "results": results,
        "elapsed_seconds": time.perf_counter() - started,
    }
    (out / "comparison.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    lines = [
        "# Model comparison — IBTrACS WP",
        "",
        f"- Years {args.years[0]}–{args.years[1]}, whole storms split by final year; "
        f"test years {summary['test_years']}.",
        f"- Storms train/val/test: {summary['storms']['train']}/"
        f"{summary['storms']['val']}/{summary['storms']['test']}; test windows "
        f"{len(test)}.",
        f"- Vietnam subset: test storms passing within {args.vn_km:.0f} km of "
        f"Vietnam's coastline: {len(vn)} storms, {int(vn_mask.sum())} windows.",
        f"- Seeds {args.seeds} for learned methods (mean ± std); baselines and "
        "k-NN are deterministic.",
        f"- k-NN analog selected on validation: {analog_info['selected']}.",
        "",
        "## Mean track error (km), all test storms",
        "",
        *_table(results, "all"),
        "",
        "## Mean track error (km), storms affecting Vietnam",
        "",
        *_table(results, "vietnam"),
        "",
        "Research benchmark only; not an operational warning.",
    ]
    (out / "comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
