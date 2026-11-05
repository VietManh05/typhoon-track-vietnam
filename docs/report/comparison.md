# Model comparison — IBTrACS WP

- Years 1980–2024, whole storms split by final year; test years [2021, 2022, 2023, 2024].
- Storms train/val/test: 895/110/84; test windows 714.
- Vietnam subset: test storms passing within 300 km of Vietnam's coastline: 27 storms, 278 windows.
- Seeds [0, 1, 2] for learned methods (mean ± std); baselines and k-NN are deterministic.
- k-NN analog selected on validation: {'k': 40, 'position': 1.0, 'season': 0.5, 'val_km': 219.37215854058525}.

## Mean track error (km), all test storms

| method | 6h | 12h | 24h | 48h | 72h |
|---|---:|---:|---:|---:|---:|
| Persistence (baseline) | 31 | 68 | 155 | 390 | 676 |
| CLIPER-proxy (baseline) | 30 | 65 | 151 | 388 | 677 |
| k-NN analog (case-based) | 32 | 64 | 133 | 290 | 462 |
| Gradient boosting | 29 ± 0 | 60 ± 0 | 129 ± 0 | 292 ± 0 | 476 ± 0 |
| LSTM | 33 ± 0 | 65 ± 1 | 133 ± 1 | 289 ± 1 | 464 ± 5 |
| Attention-LSTM | 35 ± 3 | 68 ± 4 | 138 ± 5 | 297 ± 10 | 473 ± 9 |
| Transformer | 33 ± 1 | 64 ± 1 | 133 ± 3 | 293 ± 3 | 468 ± 5 |

## Mean track error (km), storms affecting Vietnam

| method | 6h | 12h | 24h | 48h | 72h |
|---|---:|---:|---:|---:|---:|
| Persistence (baseline) | 33 | 70 | 159 | 388 | 642 |
| CLIPER-proxy (baseline) | 32 | 68 | 159 | 414 | 710 |
| k-NN analog (case-based) | 33 | 65 | 134 | 290 | 476 |
| Gradient boosting | 30 ± 0 | 61 ± 0 | 131 ± 0 | 295 ± 0 | 491 ± 0 |
| LSTM | 32 ± 0 | 63 ± 0 | 133 ± 1 | 292 ± 6 | 468 ± 9 |
| Attention-LSTM | 34 ± 3 | 66 ± 4 | 138 ± 4 | 298 ± 6 | 471 ± 3 |
| Transformer | 32 ± 1 | 62 ± 1 | 130 ± 2 | 289 ± 3 | 463 ± 10 |

Research benchmark only; not an operational warning.
