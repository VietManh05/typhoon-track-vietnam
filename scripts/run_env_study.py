"""Do steering-flow predictors make the trained model more accurate?

Same protocol as ``run_training_study.py``: Stage A chooses on validation
(2017-2020) only, Stage B evaluates once on test (2021-2024) with three seeds
and a paired storm-level bootstrap against the track-only baseline. All
methods are scored on identical Vietnam-region windows.

Environmental predictors (``typhoon_vn.features.steering``) come from NCEP/NCAR
Reanalysis 1 fields downloaded by ``scripts/download_ncep_steering.py``.

Usage::

    python scripts/run_env_study.py --data-root data --ncep runs/ncep_r1 \
        --output-dir runs/env-study
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from dataclasses import asdict, replace
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_training_study import (  # noqa: E402
    HORIZONS_H,
    Data,
    NeuralConfig,
    predict_neural,
    storm_bootstrap,
    summarise,
    train_neural,
)

from typhoon_vn.evaluation.comparison import errors_km  # noqa: E402
from typhoon_vn.features.build import FEATURE_COLUMNS  # noqa: E402
from typhoon_vn.features.steering import (  # noqa: E402
    ENV_COLUMNS,
    SteeringFields,
    steering_features,
)
from typhoon_vn.models.classical import (  # noqa: E402
    AnalogForecaster,
    GradientBoostingForecaster,
)

CASE = ("WP122024", pd.Timestamp("2024-09-04 06:00", tz="UTC"))  # YAGI


class EnvData(Data):
    feature_cols = tuple(FEATURE_COLUMNS) + tuple(ENV_COLUMNS)
    fields: SteeringFields

    def augment(self, frame: pd.DataFrame) -> pd.DataFrame:
        env = steering_features(frame, self.fields)
        coverage = float(env.notna().all(axis=1).mean())
        print(f"steering coverage {coverage:.1%} of {len(frame)} fixes", flush=True)
        return pd.concat([frame, env], axis=1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--ncep", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--years", type=int, nargs=2, default=(1980, 2024))
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    args = parser.parse_args(argv)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    work = out / "checkpoints"
    started = time.perf_counter()
    log: list[str] = []

    def note(message: str) -> None:
        print(message, flush=True)
        log.append(message)

    years = tuple(args.years)
    plain = Data(args.data_root, years)
    EnvData.fields = SteeringFields(args.ncep)
    env = EnvData(args.data_root, years)
    if plain.keys != env.keys:
        raise RuntimeError("evaluation windows differ between plain and env data")

    # ---------------- Stage A: validation ----------------
    stage_a: dict[str, dict] = {}
    val_pred: dict[str, np.ndarray] = {}
    val_y = plain.windows("box", "val", 4)

    def score(name: str, pred: np.ndarray, config: dict) -> float:
        val_pred[name] = pred
        stage_a[name] = {"config": config, "val": summarise(errors_km(pred, val_y))}
        v = stage_a[name]["val"]
        note(f"[A] {name:34s} val mean={v['mean']:.1f} 72h={v['72']:.1f}")
        return v["mean"]

    def neural(cfg: NeuralConfig, data: Data) -> float:
        model, _, _ = train_neural(cfg, data, 0, work)
        pred = predict_neural(model, data.windows(cfg.domain, "val", cfg.input_len))
        return score(cfg.name, pred, asdict(cfg))

    base = NeuralConfig(name="P0 LSTM track-only (baseline)")
    neural(base, plain)
    best = replace(base, name="E1 LSTM + steering (box)")
    best_score = neural(best, env)
    wide = replace(best, name="E2 LSTM + steering (whole basin)", domain="wide")
    if neural(wide, env) < best_score:
        best, best_score = wide, stage_a[wide.name]["val"]["mean"]
    for cfg in (
        replace(best, name="E3 + haversine loss", loss="haversine"),
        replace(
            best,
            name="E4 + wider/regularised",
            hidden=256,
            dropout=0.3,
            weight_decay=1e-4,
        ),
    ):
        if neural(cfg, env) < best_score:
            best, best_score = cfg, stage_a[cfg.name]["val"]["mean"]
    transformer = replace(
        best,
        name="E5 Transformer + steering",
        model="transformer",
        hidden=128,
        dropout=0.1,
        weight_decay=1e-5,
    )
    neural(transformer, env)

    gbm_domain = best.domain
    gbm = GradientBoostingForecaster(random_state=0).fit(
        env.windows(gbm_domain, "train", 4).x_raw, env.windows(gbm_domain, "train", 4).y
    )
    score(
        "E6 gradient boosting + steering",
        gbm.predict(env.windows(gbm_domain, "val", 4).x_raw),
        {"domain": gbm_domain},
    )

    train4 = env.windows("box", "train", 4)
    best_analog, analog_cfg, analog_score = None, None, np.inf
    for k, steer in itertools.product((20, 40, 80), (0.0, 0.5, 1.0, 2.0)):
        weights = {"track": 1.0, "position": 1.0, "season": 0.5, "steering": steer}
        model = AnalogForecaster(k=k, weights=weights).fit(
            train4.x_raw, train4.y, train4.storm_ids, train4.issue_times
        )
        s = float(
            errors_km(model.predict(env.windows("box", "val", 4).x_raw), val_y).mean()
        )
        if s < analog_score:
            best_analog, analog_cfg, analog_score = model, {"k": k, **weights}, s
    score(
        "E7 k-NN analog + steering",
        best_analog.predict(env.windows("box", "val", 4).x_raw),
        analog_cfg,
    )

    members = {
        "neural": best.name,
        "transformer": transformer.name,
        "gbm": "E6 gradient boosting + steering",
        "analog": "E7 k-NN analog + steering",
    }
    subset, subset_score = None, np.inf
    for r in range(1, len(members) + 1):
        for combo in itertools.combinations(members, r):
            s = float(
                errors_km(
                    np.mean([val_pred[members[m]] for m in combo], 0), val_y
                ).mean()
            )
            if s < subset_score:
                subset, subset_score = combo, s
    note(
        f"[A] best neural: {best.name}; ensemble on val: {subset} "
        f"(val mean {subset_score:.1f})"
    )

    # ---------------- Stage B: test, once ----------------
    test_y = plain.windows("box", "test", 4)
    results: dict[str, list[dict]] = {}
    errs: dict[str, list[np.ndarray]] = {}
    preds: dict[str, list[np.ndarray]] = {}

    def record(name: str, seed, pred: np.ndarray) -> None:
        e = errors_km(pred, test_y)
        results.setdefault(name, []).append({"seed": seed, "test": summarise(e)})
        errs.setdefault(name, []).append(e)
        preds.setdefault(name, []).append(pred)
        note(
            f"[B] {name:34s} seed={seed} test mean={e.mean():.1f} 72h={e[:, -1].mean():.1f}"
        )

    seed_pred: dict[str, dict[int, np.ndarray]] = {}
    for cfg, data in ((base, plain), (best, env), (transformer, env)):
        for seed in args.seeds:
            model, _, _ = train_neural(cfg, data, seed, work)
            p = predict_neural(model, data.windows(cfg.domain, "test", cfg.input_len))
            seed_pred.setdefault(cfg.name, {})[seed] = p
            record(cfg.name, seed, p)
    gbm_test = gbm.predict(env.windows(gbm_domain, "test", 4).x_raw)
    record(members["gbm"], None, gbm_test)
    analog_test = best_analog.predict(env.windows("box", "test", 4).x_raw)
    record(members["analog"], None, analog_test)
    ensemble = "Ensemble (" + "+".join(subset) + ")"
    for seed in args.seeds:
        parts = {
            "neural": seed_pred[best.name][seed],
            "transformer": seed_pred[transformer.name][seed],
            "gbm": gbm_test,
            "analog": analog_test,
        }
        record(ensemble, seed, np.mean([parts[m] for m in subset], 0))

    def mean72(name: str) -> np.ndarray:
        return np.mean([e[:, -1] for e in errs[name]], axis=0)

    bootstrap = {
        f"{name} vs {base.name}": storm_bootstrap(
            mean72(name), mean72(base.name), test_y.storm_ids
        )
        for name in (best.name, ensemble)
    }
    for label, value in bootstrap.items():
        note(f"[B] {label}: {value}")

    # YAGI 2024 case (seed-averaged predictions at the hindcast issue time).
    case_rows = np.flatnonzero(
        (test_y.storm_ids == CASE[0])
        & (
            pd.to_datetime(pd.Series(test_y.issue_times), utc=True) == CASE[1]
        ).to_numpy()
    )
    case = {}
    if len(case_rows):
        i = int(case_rows[0])
        case["actual"] = test_y.y[i].round(2).tolist()
        for name in (base.name, best.name, ensemble, members["analog"]):
            p = np.mean([q[i] for q in preds[name]], axis=0)
            e = errors_km(
                p[None],
                type(test_y)(
                    test_y.x_raw[i : i + 1],
                    None,
                    test_y.y[i : i + 1],
                    test_y.storm_ids[i : i + 1],
                    test_y.issue_times[i : i + 1],
                ),
            )[0]
            case[name] = {
                "track": p.round(2).tolist(),
                "error_km": {str(h): round(float(v), 0) for h, v in zip(HORIZONS_H, e)},
            }
            note(
                f"[YAGI] {name:34s} 72h error {e[-1]:.0f} km, 72h pos "
                f"{p[-1, 0]:.1f}N {p[-1, 1]:.1f}E (actual {test_y.y[i, -1, 0]:.1f}N "
                f"{test_y.y[i, -1, 1]:.1f}E)"
            )

    summary = {
        "eval_windows": {
            "val": len(plain.keys["val"]),
            "test": len(plain.keys["test"]),
        },
        "env_columns": list(ENV_COLUMNS),
        "stage_a": stage_a,
        "best_neural": asdict(best),
        "analog": analog_cfg,
        "ensemble_members": [members[m] for m in subset],
        "stage_b": results,
        "bootstrap_72h": bootstrap,
        "yagi_case": case,
        "log": log,
        "elapsed_seconds": round(time.perf_counter() - started),
    }
    (out / "env_study.json").write_text(
        json.dumps(summary, indent=2, default=str), encoding="utf-8"
    )

    def table(rows, key):
        lines = [
            "| configuration | "
            + " | ".join(f"{h}h" for h in HORIZONS_H)
            + " | mean |",
            "|---|" + "---:|" * (len(HORIZONS_H) + 1),
        ]
        for name, runs in rows.items():
            v = np.array(
                [[r[key][str(h)] for h in HORIZONS_H] + [r[key]["mean"]] for r in runs]
            )
            cells = (
                [f"{m:.0f} ± {s:.0f}" for m, s in zip(v.mean(0), v.std(0, ddof=1))]
                if len(v) > 1
                else [f"{m:.0f}" for m in v[0]]
            )
            lines.append(f"| {name} | " + " | ".join(cells) + " |")
        return lines

    md = [
        "# Steering-flow study — NCEP/NCAR R1 predictors",
        "",
        f"Evaluation windows (Vietnam region, 48 h history): val "
        f"{len(plain.keys['val'])}, test {len(plain.keys['test'])}.",
        f"Environmental predictors: {', '.join(ENV_COLUMNS)}.",
        "",
        "## Stage A — validation 2017–2020 (seed 0)",
        "",
        *table({k: [{"val": v["val"]}] for k, v in stage_a.items()}, "val"),
        "",
        f"Selected: **{best.name}**; ensemble members: {[members[m] for m in subset]}",
        "",
        f"## Stage B — test 2021–2024 (seeds {args.seeds})",
        "",
        *table(results, "test"),
        "",
        "Paired storm-level bootstrap at 72 h (negative = better than track-only):",
        "",
        *[
            f"- {k}: {v['mean_km']:+.0f} km, 95% CI [{v['ci95'][0]:+.0f}, "
            f"{v['ci95'][1]:+.0f}] over {v['storms']} storms"
            for k, v in bootstrap.items()
        ],
        "",
        "## YAGI 2024 (issued 2024-09-04 06Z), 72 h",
        "",
        *[
            f"- {k}: {v['error_km']['72']:.0f} km"
            for k, v in case.items()
            if k != "actual"
        ],
        "",
    ]
    (out / "env_study.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
