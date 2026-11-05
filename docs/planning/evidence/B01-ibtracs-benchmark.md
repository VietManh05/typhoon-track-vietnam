# IBTrACS WP benchmark — IBTrACS-WP-1980-2024-sha256:08544ff3530d

- Years: [1980, 2024]; clean rows: 24024; storms: 1089
- Split (whole storms by final year): {'train': 895, 'val': 110, 'test': 84}
- Test years: [2021, 2022, 2023, 2024]; test storms: 84
- Epochs run: 15; train seconds: 58

Mean great-circle track error (km) on the test split:

| model | 6h | 12h | 24h | 48h | 72h |
|---|---:|---:|---:|---:|---:|
| lstm | 34 | 66 | 135 | 294 | 470 |
| persistence | 31 | 68 | 155 | 390 | 676 |
| cliper | 30 | 65 | 151 | 388 | 677 |
| n forecasts | 714 | 714 | 714 | 714 | 714 |

Research benchmark only; not an operational warning. CLIPER is a damped-persistence proxy, not operational CLIPER5.

## Reproduce

```powershell
python scripts/run_ibtracs_benchmark.py --data-root data --output-dir runs/ibtracs-benchmark
```

Config: `configs/ibtracs_benchmark.yaml` (seed 42, LSTM 2x128, residual displacement head, best-validation weights). Run date 2026-11-05, CPU.

## Caveats

- Single seed, single split; no confidence intervals yet.
- Domain box lat 0–30, lon 100–140 (`features/constants.py`); fixes outside it are dropped (reported as `n_dropped_invalid_coords`).
- Raw partitions contain every IBTrACS row twice; deduplication removes them.
- Early stopping at epoch 15 with best epoch 5: the model overfits quickly; regularisation/feature work is the next lever.
- Cone radii in the bundle are still illustrative (G11 not done).
