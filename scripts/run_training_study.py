"""Training study: make the trained model as accurate as possible, honestly.

Stage A (validation only, seed 0): one change at a time from the current
LSTM baseline — training domain (Vietnam box vs whole WP basin), input history
(24 h vs 48 h), loss (Smooth L1 in degrees vs haversine in km), capacity and
regularisation, Transformer, plus k-NN analog and gradient boosting.

Stage B (test, touched once): the validation-selected configurations with
three seeds, the old baseline, and an ensemble whose members are chosen on
validation. A paired storm-level bootstrap compares the best against the
baseline at 72 h.

All methods are scored on the same windows: Vietnam-box validation/test storms
with a regular 48 h history (so 24 h and 48 h inputs are comparable).

Usage::

    python scripts/run_training_study.py --data-root data --output-dir runs/training-study
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from dataclasses import asdict, dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset

from typhoon_vn.datasets.ibtracs import load_ibtracs_tracks
from typhoon_vn.datasets.typhoon_dataset import DatasetConfig, split_by_storm_or_year
from typhoon_vn.evaluation.comparison import Windows, build_windows, errors_km
from typhoon_vn.features.build import FEATURE_COLUMNS, FeatureBuilder
from typhoon_vn.features.scaling import FeatureScaler
from typhoon_vn.models.classical import AnalogForecaster, GradientBoostingForecaster
from typhoon_vn.models.lstm import LSTMTrackForecaster
from typhoon_vn.models.residual import ResidualTrackForecaster
from typhoon_vn.models.transformer import TransformerTrackForecaster
from typhoon_vn.training.losses import MultiHorizonLoss
from typhoon_vn.training.pipeline import position_stats
from typhoon_vn.training.reproducibility import set_global_determinism
from typhoon_vn.training.trainer import Trainer, TrainingConfig

HORIZON_STEPS = (1, 2, 4, 8, 12)
HORIZONS_H = [6 * s for s in HORIZON_STEPS]
WIDE_BOUNDS = (0.0, 50.0, 95.0, 180.0)  # whole Western Pacific basin
EVAL_HISTORY = 8  # common evaluation set: windows with 48 h of history


@dataclass(frozen=True)
class NeuralConfig:
    name: str
    model: str = "lstm"  # lstm | transformer
    domain: str = "box"  # box | wide
    input_len: int = 4
    loss: str = "smooth_l1"  # smooth_l1 | haversine
    hidden: int = 128
    layers: int = 2
    dropout: float = 0.2
    weight_decay: float = 1e-5
    lr: float = 1e-3


# ----------------------------------------------------------------------------
# data
# ----------------------------------------------------------------------------


class Data:
    feature_cols: tuple[str, ...] = tuple(FEATURE_COLUMNS)

    def augment(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Hook for subclasses to append extra per-fix columns."""

        return frame

    def __init__(self, data_root: Path, years: tuple[int, int]) -> None:
        _, box, _ = load_ibtracs_tracks(data_root, years)
        _, wide, _ = load_ibtracs_tracks(data_root, years, bounds=WIDE_BOUNDS)
        box, wide = self.augment(box), self.augment(wide)
        self.frames = {}
        for domain, frame in (("box", box), ("wide", wide)):
            train, val, test = split_by_storm_or_year(
                frame, val_ratio=0.1, test_ratio=0.1, by_year=True
            )
            self.frames[domain] = {"train": train, "val": val, "test": test}
        years_of = {
            d: sorted(
                f["test"].groupby("storm_id").timestamp.max().dt.year.unique().tolist()
            )
            for d, f in self.frames.items()
        }
        if years_of["box"] != years_of["wide"]:
            raise RuntimeError(f"test years differ between domains: {years_of}")
        self.test_years = years_of["box"]
        self.scalers: dict[str, FeatureScaler] = {}
        self._cache: dict[tuple, Windows] = {}
        # Common evaluation keys: Vietnam-box storms with 48 h of history.
        self.keys = {
            split: self._keys(self.frames["box"][split], EVAL_HISTORY)
            for split in ("val", "test")
        }

    def _config(self, input_len: int) -> DatasetConfig:
        return DatasetConfig(
            input_len=input_len,
            horizon=HORIZON_STEPS,
            feature_cols=self.feature_cols,
        )

    def _keys(self, frame: pd.DataFrame, input_len: int) -> list[tuple]:
        w = build_windows(frame, self._config(input_len))
        return [(s, pd.Timestamp(t)) for s, t in zip(w.storm_ids, w.issue_times)]

    def scaler(self, domain: str) -> FeatureScaler:
        if domain not in self.scalers:
            train = self.frames[domain]["train"]
            self.scalers[domain] = FeatureScaler(list(self.feature_cols)).fit(
                FeatureBuilder().transform(train)[list(self.feature_cols)]
            )
        return self.scalers[domain]

    def windows(self, domain: str, split: str, input_len: int) -> Windows:
        """Train windows from ``domain``; val/test always the common box set."""

        key = (domain, split, input_len)
        if key in self._cache:
            return self._cache[key]
        scaler = self.scaler(domain)
        if split == "train":
            w = build_windows(
                self.frames[domain]["train"], self._config(input_len), scaler
            )
        else:
            w = build_windows(
                self.frames["box"][split], self._config(input_len), scaler
            )
            index = {
                (s, pd.Timestamp(t)): i
                for i, (s, t) in enumerate(zip(w.storm_ids, w.issue_times))
            }
            rows = np.array([index[k] for k in self.keys[split]])
            w = Windows(
                x_raw=w.x_raw[rows],
                x_scaled=w.x_scaled[rows],
                y=w.y[rows],
                storm_ids=w.storm_ids[rows],
                issue_times=w.issue_times[rows],
            )
        self._cache[key] = w
        return w


# ----------------------------------------------------------------------------
# models
# ----------------------------------------------------------------------------


def _loader(w: Windows, shuffle: bool, seed: int) -> DataLoader:
    ds = TensorDataset(
        torch.tensor(w.x_scaled, dtype=torch.float32),
        torch.tensor(w.y, dtype=torch.float32),
    )

    def collate(rows):
        x, y = map(torch.stack, zip(*rows))
        return {
            "x": x,
            "mask": torch.ones(x.shape[:2]),
            "y_reg": y,
            "y_cls": torch.zeros(y.shape[:2], dtype=torch.long),
        }

    return DataLoader(
        ds,
        batch_size=64,
        shuffle=shuffle,
        generator=torch.Generator().manual_seed(seed),
        collate_fn=collate,
    )


def train_neural(cfg: NeuralConfig, data: Data, seed: int, workdir: Path):
    set_global_determinism(seed)
    train = data.windows(cfg.domain, "train", cfg.input_len)
    val = data.windows(cfg.domain, "val", cfg.input_len)
    n_features, n_h = len(data.feature_cols), len(HORIZON_STEPS)
    if cfg.model == "lstm":
        base = LSTMTrackForecaster(
            n_features,
            n_h,
            2,
            hidden_size=cfg.hidden,
            num_layers=cfg.layers,
            dropout=cfg.dropout,
        )
    else:
        base = TransformerTrackForecaster(
            n_features,
            n_h,
            2,
            d_model=cfg.hidden // 2,
            nhead=4,
            n_layers=cfg.layers,
            dim_feedforward=cfg.hidden,
            dropout=cfg.dropout,
        )
    stats = position_stats(data.scaler(cfg.domain))
    model = ResidualTrackForecaster(
        base, stats["position_mean"], stats["position_scale"]
    )
    loss = MultiHorizonLoss(
        n_h,
        2,
        reg_loss=cfg.loss,
        cls_weight=0.0,
        reg_weight=0.01 if cfg.loss == "haversine" else 1.0,
    )
    ckpt = workdir / f"{cfg.name}-s{seed}"
    trainer = Trainer(
        model,
        TrainingConfig(
            epochs=100,
            batch_size=64,
            learning_rate=cfg.lr,
            weight_decay=cfg.weight_decay,
            patience=10,
            gradient_clip=1.0,
            scheduler="cosine",
            device="cpu",
            checkpoint_dir=ckpt,
            log_every=1000,
        ),
        loss,
    )
    result = trainer.fit(_loader(train, True, seed), _loader(val, False, seed))
    # Checkpoint written by this process just above (holds RNG state).
    best = torch.load(ckpt / "best.pt", map_location="cpu", weights_only=False)
    model.load_state_dict(best["model_state_dict"])
    return model.eval(), int(result["best_epoch"]), len(train)


def predict_neural(model, w: Windows) -> np.ndarray:
    with torch.no_grad():
        x = torch.tensor(w.x_scaled, dtype=torch.float32)
        return model(x, torch.ones(x.shape[:2]))["reg"].numpy().astype(float)


def fit_analog(data: Data, domain: str, input_len: int):
    train = data.windows(domain, "train", input_len)
    val = data.windows(domain, "val", input_len)
    best, best_score, chosen = None, np.inf, None
    for k, position in itertools.product((10, 20, 40, 80), (0.5, 1.0, 2.0)):
        weights = {"track": 1.0, "position": position, "season": 0.5}
        model = AnalogForecaster(k=k, weights=weights).fit(
            train.x_raw, train.y, train.storm_ids, train.issue_times
        )
        score = float(errors_km(model.predict(val.x_raw), val).mean())
        if score < best_score:
            best, best_score, chosen = model, score, {"k": k, **weights}
    return best, chosen


def summarise(err: np.ndarray) -> dict[str, float]:
    out = {str(h): round(float(err[:, i].mean()), 1) for i, h in enumerate(HORIZONS_H)}
    out["mean"] = round(float(err.mean()), 1)
    return out


def storm_bootstrap(a: np.ndarray, b: np.ndarray, storms: np.ndarray, n=5000):
    """Mean (a - b) at 72 h with a paired storm-level 95% bootstrap CI."""

    frame = pd.DataFrame({"storm": storms, "d": a - b}).groupby("storm")["d"].mean()
    diffs = frame.to_numpy()
    rng = np.random.default_rng(0)
    boot = diffs[rng.integers(0, len(diffs), size=(n, len(diffs)))].mean(axis=1)
    low, high = np.percentile(boot, [2.5, 97.5])
    return {
        "mean_km": round(float(diffs.mean()), 1),
        "ci95": [round(low, 1), round(high, 1)],
        "storms": len(diffs),
    }


# ----------------------------------------------------------------------------
# study
# ----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--years", type=int, nargs=2, default=(1980, 2024))
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    args = parser.parse_args(argv)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    work = out / "checkpoints"
    started = time.perf_counter()
    log = []

    def note(message: str) -> None:
        print(message, flush=True)
        log.append(message)

    data = Data(args.data_root, tuple(args.years))
    note(
        "train windows box/wide (24h): "
        f"{len(data.windows('box', 'train', 4))}/{len(data.windows('wide', 'train', 4))}; "
        f"eval windows val/test: {len(data.keys['val'])}/{len(data.keys['test'])}"
    )

    # ---------------- Stage A: validation only ----------------
    stage_a: dict[str, dict] = {}
    val_pred: dict[str, np.ndarray] = {}

    def run_a(cfg: NeuralConfig) -> float:
        model, best_epoch, n_train = train_neural(cfg, data, 0, work)
        val = data.windows(cfg.domain, "val", cfg.input_len)
        pred = predict_neural(model, val)
        val_pred[cfg.name] = pred
        stage_a[cfg.name] = {
            "config": asdict(cfg),
            "val": summarise(errors_km(pred, val)),
            "best_epoch": best_epoch,
            "train_windows": n_train,
        }
        note(
            f"[A] {cfg.name:28s} val mean={stage_a[cfg.name]['val']['mean']:.1f} "
            f"72h={stage_a[cfg.name]['val']['72']:.1f} best_epoch={best_epoch}"
        )
        return stage_a[cfg.name]["val"]["mean"]

    baseline = NeuralConfig(name="A0 baseline (box, 24h, L1)")
    run_a(baseline)
    wide = replace(baseline, name="A1 + whole-basin data", domain="wide")
    best = wide if run_a(wide) < stage_a[baseline.name]["val"]["mean"] else baseline
    longer = replace(best, name="A2 + 48h history", input_len=8)
    if run_a(longer) < stage_a[best.name]["val"]["mean"]:
        best = longer
    km = replace(best, name="A3 + haversine loss (km)", loss="haversine")
    if run_a(km) < stage_a[best.name]["val"]["mean"]:
        best = km
    for cfg in (
        replace(
            best,
            name="A4 + wider/regularised",
            hidden=256,
            dropout=0.3,
            weight_decay=1e-4,
        ),
        replace(best, name="A5 + smaller/lr 5e-4", hidden=64, lr=5e-4),
    ):
        if run_a(cfg) < stage_a[best.name]["val"]["mean"]:
            best = cfg
    transformer = replace(
        best,
        name="A6 Transformer (same data/loss)",
        model="transformer",
        hidden=128,
        layers=2,
        dropout=0.1,
        weight_decay=1e-5,
        lr=1e-3,
    )
    run_a(transformer)

    analog_choice = {}
    for domain in ("box", "wide"):
        model, chosen = fit_analog(data, domain, 4)
        val = data.windows(domain, "val", 4)
        name = f"A7 k-NN analog ({domain})"
        val_pred[name] = model.predict(val.x_raw)
        stage_a[name] = {
            "config": chosen,
            "val": summarise(errors_km(val_pred[name], val)),
        }
        analog_choice[domain] = (model, chosen)
        note(
            f"[A] {name:28s} val mean={stage_a[name]['val']['mean']:.1f} "
            f"72h={stage_a[name]['val']['72']:.1f} {chosen}"
        )
    analog_domain = min(
        ("box", "wide"), key=lambda d: stage_a[f"A7 k-NN analog ({d})"]["val"]["mean"]
    )

    gbm_domain = best.domain
    gbm = GradientBoostingForecaster(random_state=0).fit(
        data.windows(gbm_domain, "train", 4).x_raw,
        data.windows(gbm_domain, "train", 4).y,
    )
    val4 = data.windows(gbm_domain, "val", 4)
    val_pred["A8 gradient boosting"] = gbm.predict(val4.x_raw)
    stage_a["A8 gradient boosting"] = {
        "config": {"domain": gbm_domain},
        "val": summarise(errors_km(val_pred["A8 gradient boosting"], val4)),
    }
    note(
        f"[A] A8 gradient boosting ({gbm_domain}) val mean="
        f"{stage_a['A8 gradient boosting']['val']['mean']:.1f}"
    )

    # Ensemble members chosen on validation (seed-0 predictions).
    members = {
        "best_neural": best.name,
        "transformer": transformer.name,
        "analog": f"A7 k-NN analog ({analog_domain})",
        "gbm": "A8 gradient boosting",
    }
    val_y = data.windows("box", "val", 4)
    best_subset, best_score = None, np.inf
    for r in range(1, len(members) + 1):
        for subset in itertools.combinations(members, r):
            pred = np.mean([val_pred[members[m]] for m in subset], axis=0)
            score = float(errors_km(pred, val_y).mean())
            if score < best_score:
                best_subset, best_score = subset, score
    note(f"[A] ensemble selected on val: {best_subset} val mean={best_score:.1f}")
    note(f"[A] best single neural config: {best.name}")

    # ---------------- Stage B: test, once ----------------
    test_y = data.windows("box", "test", 4)
    results: dict[str, list[dict]] = {}
    test_err: dict[str, list[np.ndarray]] = {}

    def record(name: str, seed, pred: np.ndarray) -> None:
        err = errors_km(pred, test_y)
        results.setdefault(name, []).append({"seed": seed, "test": summarise(err)})
        test_err.setdefault(name, []).append(err)
        note(
            f"[B] {name:28s} seed={seed} test mean={err.mean():.1f} "
            f"72h={err[:, -1].mean():.1f}"
        )

    seed_preds: dict[str, dict[int, np.ndarray]] = {}
    for cfg in {
        baseline.name: baseline,
        best.name: best,
        transformer.name: transformer,
    }.values():
        for seed in args.seeds:
            model, _, _ = train_neural(cfg, data, seed, work)
            pred = predict_neural(
                model, data.windows(cfg.domain, "test", cfg.input_len)
            )
            seed_preds.setdefault(cfg.name, {})[seed] = pred
            record(cfg.name, seed, pred)
    analog_model, _ = analog_choice[analog_domain]
    analog_test = analog_model.predict(data.windows(analog_domain, "test", 4).x_raw)
    record(members["analog"], None, analog_test)
    gbm_test = gbm.predict(data.windows(gbm_domain, "test", 4).x_raw)
    record(members["gbm"], None, gbm_test)

    for seed in args.seeds:
        parts = {
            "best_neural": seed_preds[best.name][seed],
            "transformer": seed_preds[transformer.name][seed],
            "analog": analog_test,
            "gbm": gbm_test,
        }
        pred = np.mean([parts[m] for m in best_subset], axis=0)
        record("Ensemble (" + "+".join(best_subset) + ")", seed, pred)

    def mean72(name):
        return np.mean([e[:, -1] for e in test_err[name]], axis=0)

    ensemble_name = "Ensemble (" + "+".join(best_subset) + ")"
    comparisons = {
        f"{name} vs baseline": storm_bootstrap(
            mean72(name), mean72(baseline.name), test_y.storm_ids
        )
        for name in (best.name, ensemble_name)
    }
    for label, value in comparisons.items():
        note(f"[B] {label}: {value}")

    summary = {
        "test_years": data.test_years,
        "eval_windows": {"val": len(data.keys["val"]), "test": len(data.keys["test"])},
        "stage_a": stage_a,
        "best_neural": asdict(best),
        "ensemble_members": [members[m] for m in best_subset],
        "stage_b": results,
        "bootstrap_72h": comparisons,
        "log": log,
        "elapsed_seconds": round(time.perf_counter() - started),
    }
    (out / "study.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    def table(rows: dict[str, list[dict]], key: str) -> list[str]:
        lines = [
            "| configuration | "
            + " | ".join(f"{h}h" for h in HORIZONS_H)
            + " | mean |",
            "|---|" + "---:|" * (len(HORIZONS_H) + 1),
        ]
        for name, runs in rows.items():
            vals = np.array(
                [[r[key][str(h)] for h in HORIZONS_H] + [r[key]["mean"]] for r in runs]
            )
            if len(vals) > 1:
                cells = [
                    f"{m:.0f} ± {s:.0f}"
                    for m, s in zip(vals.mean(0), vals.std(0, ddof=1))
                ]
            else:
                cells = [f"{m:.0f}" for m in vals[0]]
            lines.append(f"| {name} | " + " | ".join(cells) + " |")
        return lines

    stage_a_rows = {k: [{"val": v["val"]}] for k, v in stage_a.items()}
    md = [
        "# Training study — IBTrACS WP, evaluated on Vietnam-region storms",
        "",
        f"Common evaluation windows (48 h history available): val {len(data.keys['val'])},"
        f" test {len(data.keys['test'])} (test years {data.test_years}).",
        "",
        "## Stage A — validation (2017–2020), seed 0; each step kept only if it helped",
        "",
        *table(stage_a_rows, "val"),
        "",
        f"Selected neural config: **{best.name}** — {asdict(best)}",
        f"Ensemble members (chosen on validation): {[members[m] for m in best_subset]}",
        "",
        f"## Stage B — test (2021–2024), seeds {args.seeds}",
        "",
        *table(results, "test"),
        "",
        "Paired storm-level bootstrap at 72 h (negative = better than baseline):",
        "",
        *[
            f"- {k}: {v['mean_km']:+.0f} km, 95% CI [{v['ci95'][0]:+.0f}, "
            f"{v['ci95'][1]:+.0f}] over {v['storms']} storms"
            for k, v in comparisons.items()
        ],
        "",
    ]
    (out / "study.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
