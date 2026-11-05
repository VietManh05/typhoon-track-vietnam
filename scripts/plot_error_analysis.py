"""Error analysis figures and tables for the model comparison.

Reads ``run_model_comparison.py`` outputs and writes to ``<run>/analysis``:

* ``error_by_horizon.png`` — mean error vs lead time, all vs Vietnam storms
* ``error_by_intensity.md`` — 72 h error by intensity class at issue time
* ``case_<storm>.png`` — observed track vs forecasts for storms affecting
  Vietnam, with the analog storms the k-NN method relied on
* ``cases.md`` — the case-study numbers and analog explanations

Usage::

    python scripts/plot_error_analysis.py --run runs/model-comparison \
        --data-root data
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from typhoon_vn.datasets.ibtracs import load_ibtracs_tracks  # noqa: E402
from typhoon_vn.datasets.typhoon_dataset import (  # noqa: E402
    DatasetConfig,
    split_by_storm_or_year,
)
from typhoon_vn.evaluation.comparison import build_windows  # noqa: E402
from typhoon_vn.features import constants as C  # noqa: E402
from typhoon_vn.features.build import FEATURE_COLUMNS  # noqa: E402
from typhoon_vn.models.classical import AnalogForecaster  # noqa: E402

HORIZONS = [6, 12, 24, 48, 72]
LABELS = {
    "persistence": "Persistence",
    "cliper": "CLIPER-proxy",
    "analog_knn": "k-NN analog",
    "gradient_boosting": "Gradient boosting",
    "lstm": "LSTM",
    "attention_lstm": "Attention-LSTM",
    "transformer": "Transformer",
}
# Vietnamese storm classes from 10-min sustained wind (m/s); IBTrACS USA_WIND
# is 1-min, so bins are indicative for analysis only.
INTENSITY_BINS = [0, 17.2, 24.5, 32.7, 41.5, np.inf]
INTENSITY_NAMES = [
    "ATNĐ (<17.2 m/s)",
    "Bão cấp 8–9",
    "Bão mạnh cấp 10–11",
    "Bão rất mạnh cấp 12–13",
    "Cuồng phong ≥ cấp 14",
]


def horizon_figure(summary: dict, path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    for axis, subset, title in zip(
        axes, ("all", "vietnam"), ("All test storms", "Storms affecting Vietnam")
    ):
        for name, runs in summary["results"].items():
            values = np.array([[run[subset][str(h)] for h in HORIZONS] for run in runs])
            mean = values.mean(axis=0)
            style = "--" if name in ("persistence", "cliper") else "-"
            axis.plot(HORIZONS, mean, style, marker="o", label=LABELS[name])
            if len(values) > 1:
                std = values.std(axis=0, ddof=1)
                axis.fill_between(HORIZONS, mean - std, mean + std, alpha=0.15)
        axis.set_title(title)
        axis.set_xlabel("Lead time (h)")
        axis.set_xticks(HORIZONS)
        axis.grid(alpha=0.3)
    axes[0].set_ylabel("Mean track error (km)")
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def intensity_table(pred: pd.DataFrame, tracks: pd.DataFrame, methods) -> str:
    issue = tracks[["storm_id", "timestamp", "wind_ms"]].copy()
    issue["issue_time"] = pd.to_datetime(issue["timestamp"], utc=True)
    at72 = pred[pred.horizon_h == 72].copy()
    at72["issue_time"] = pd.to_datetime(at72["issue_time"], utc=True)
    merged = at72.merge(issue, on=["storm_id", "issue_time"], how="left")
    merged["class"] = pd.cut(
        merged["wind_ms"], INTENSITY_BINS, labels=INTENSITY_NAMES, right=False
    )
    merged["class"] = merged["class"].cat.add_categories("Không rõ").fillna("Không rõ")
    table = merged.pivot_table(
        index="class",
        columns="method",
        values="error_km",
        aggfunc="mean",
        observed=True,
    )[methods]
    counts = merged[merged.method == methods[0]].groupby("class", observed=True).size()
    lines = [
        "| Cường độ lúc phát dự báo | n | "
        + " | ".join(LABELS[m] for m in methods)
        + " |",
        "|---|---:|" + "---:|" * len(methods),
    ]
    for cls, row in table.iterrows():
        cells = " | ".join(f"{row[m]:.0f}" for m in methods)
        lines.append(f"| {cls} | {counts.get(cls, 0)} | {cells} |")
    return "\n".join(lines)


def storm_bootstrap(
    pred: pd.DataFrame,
    methods,
    reference: str,
    horizon: int = 72,
    n_boot: int = 5000,
    seed: int = 0,
) -> str:
    """Paired storm-level bootstrap of mean error difference vs ``reference``.

    Forecasts from one storm are correlated, so storms (not windows) are
    resampled; each storm contributes its mean error at ``horizon``.
    """

    per_storm = (
        pred[pred.horizon_h == horizon]
        .groupby(["storm_id", "method"])["error_km"]
        .mean()
        .unstack()
    )
    rng = np.random.default_rng(seed)
    draws = rng.integers(0, len(per_storm), size=(n_boot, len(per_storm)))
    lines = [
        f"Reference: {LABELS[reference]}, {horizon} h, {len(per_storm)} test "
        f"storms, {n_boot} storm-level bootstrap resamples (negative = better "
        "than the reference).",
        "",
        "| method | mean diff (km) | 95% CI | better in % of resamples |",
        "|---|---:|---:|---:|",
    ]
    for method in methods:
        if method == reference:
            continue
        diff = (per_storm[method] - per_storm[reference]).to_numpy()
        boot = diff[draws].mean(axis=1)
        low, high = np.percentile(boot, [2.5, 97.5])
        lines.append(
            f"| {LABELS[method]} | {diff.mean():+.0f} | [{low:+.0f}, {high:+.0f}] "
            f"| {np.mean(boot < 0):.0%} |"
        )
    return "\n".join(lines)


def pick_case_issue(storm_pred: pd.DataFrame) -> str:
    """Issue time whose 72 h verifying position is closest to Vietnam."""

    at72 = storm_pred[storm_pred.horizon_h == 72].drop_duplicates("issue_time")
    coast = np.array(C.VN_COASTLINE)
    distance = [
        np.min(np.hypot(coast[:, 0] - lat, coast[:, 1] - lon))
        for lat, lon in zip(at72.obs_lat, at72.obs_lon)
    ]
    return at72.iloc[int(np.argmin(distance))]["issue_time"]


def case_figure(storm, name, track, storm_pred, issue, methods, analogs, path):
    fig, axis = plt.subplots(figsize=(6.5, 6))
    coast = np.array(C.VN_COASTLINE)
    axis.plot(coast[:, 1], coast[:, 0], color="0.4", lw=1.5, label="Vietnam coast")
    axis.plot(track.lon, track.lat, "k.-", lw=1, ms=3, label="Observed track")
    issued = storm_pred[storm_pred.issue_time == issue]
    first = issued[issued.method == methods[0]].sort_values("horizon_h")
    anchor_time = pd.Timestamp(issue)
    anchor = track[pd.to_datetime(track.timestamp, utc=True) == anchor_time]
    for method in methods:
        rows = issued[issued.method == method].sort_values("horizon_h")
        lon = np.r_[anchor.lon.values, rows.pred_lon.values]
        lat = np.r_[anchor.lat.values, rows.pred_lat.values]
        axis.plot(
            lon,
            lat,
            "o-",
            ms=4,
            label=f"{LABELS[method]} (72h err " f"{rows.error_km.values[-1]:.0f} km)",
        )
    axis.plot(first.obs_lon, first.obs_lat, "kx", ms=8, label="Verifying positions")
    axis.plot(
        anchor.lon, anchor.lat, "r*", ms=14, label=f"Issue {anchor_time:%d/%m %HZ}"
    )
    axis.set_title(f"{name} ({storm})")
    axis.set_xlabel("Longitude (°E)")
    axis.set_ylabel("Latitude (°N)")
    axis.grid(alpha=0.3)
    axis.legend(fontsize=7, loc="best")
    if analogs:
        text = "k-NN analogs: " + ", ".join(analogs)
        fig.text(0.01, 0.01, text, fontsize=7, wrap=True)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--cases", type=int, default=4)
    args = parser.parse_args(argv)
    out = args.run / "analysis"
    out.mkdir(parents=True, exist_ok=True)

    summary = json.loads((args.run / "comparison.json").read_text(encoding="utf-8"))
    pred = pd.read_csv(args.run / "test_predictions.csv")
    methods = [m for m in LABELS if m in set(pred.method)]
    horizon_figure(summary, out / "error_by_horizon.png")

    raw, cleaned, _ = load_ibtracs_tracks(args.data_root, tuple(summary["years"]))
    names = (
        raw.dropna(subset=["storm_name"])
        .drop_duplicates("storm_id")
        .set_index("storm_id")["storm_name"]
        .astype(str)
    )
    train_f, _, test_f = split_by_storm_or_year(
        cleaned, val_ratio=0.1, test_ratio=0.1, by_year=True
    )
    (out / "error_by_intensity.md").write_text(
        "# Sai số 72h theo cường độ lúc phát dự báo (km)\n\n"
        + intensity_table(pred, test_f, methods)
        + "\n",
        encoding="utf-8",
    )

    (out / "significance.md").write_text(
        "# Paired storm-level bootstrap at 72 h\n\n## vs persistence\n\n"
        + storm_bootstrap(pred, methods, "persistence")
        + "\n\n## vs LSTM\n\n"
        + storm_bootstrap(pred, methods, "lstm")
        + "\n",
        encoding="utf-8",
    )

    # Refit the validation-selected analog model to explain its suggestions.
    config = DatasetConfig(
        input_len=4, horizon=(1, 2, 4, 8, 12), feature_cols=tuple(FEATURE_COLUMNS)
    )
    train, test = build_windows(train_f, config), build_windows(test_f, config)
    chosen = summary["analog"]["selected"]
    analog = AnalogForecaster(
        k=chosen["k"],
        weights={
            "track": 1.0,
            "position": chosen["position"],
            "season": chosen["season"],
        },
    ).fit(train.x_raw, train.y, train.storm_ids, train.issue_times)

    from typhoon_vn.evaluation.comparison import vietnam_storms

    vn = vietnam_storms(test_f)
    counts = pred[pred.storm_id.isin(vn)].groupby("storm_id").size()
    case_lines = ["# Case studies: storms affecting Vietnam", ""]
    shown = [
        m
        for m in (
            "persistence",
            "analog_knn",
            "gradient_boosting",
            "transformer",
            "lstm",
        )
        if m in methods
    ]
    for storm in counts.sort_values(ascending=False).index[: args.cases]:
        storm_pred = pred[pred.storm_id == storm]
        issue = pick_case_issue(storm_pred)
        window = np.flatnonzero(
            (test.storm_ids == storm)
            & (
                pd.to_datetime(pd.Series(test.issue_times), utc=True)
                == pd.Timestamp(issue)
            ).to_numpy()
        )
        explained = analog.explain(test.x_raw[window], top=5)[0] if len(window) else []
        analogs = [
            f"{names.get(item['storm_id'], item['storm_id'])} "
            f"{pd.Timestamp(item['issue_time']).year}"
            for item in explained
        ]
        name = names.get(storm, storm)
        track = test_f[test_f.storm_id == storm].sort_values("timestamp")
        case_figure(
            storm,
            name,
            track,
            storm_pred,
            issue,
            shown,
            analogs,
            out / f"case_{storm}.png",
        )
        at72 = storm_pred[
            (storm_pred.issue_time == issue) & (storm_pred.horizon_h == 72)
        ]
        case_lines += [
            f"## {name} ({storm}) — issued {pd.Timestamp(issue):%Y-%m-%d %H}Z",
            "",
            "| method | 72h error (km) |",
            "|---|---:|",
            *[
                f"| {LABELS[row.method]} | {row.error_km:.0f} |"
                for row in at72.sort_values("error_km").itertuples()
            ],
            "",
            f"k-NN analog storms: {', '.join(analogs) or 'n/a'}",
            "",
            f"![{name}](case_{storm}.png)",
            "",
        ]
    (out / "cases.md").write_text("\n".join(case_lines), encoding="utf-8")
    print(f"wrote analysis to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
