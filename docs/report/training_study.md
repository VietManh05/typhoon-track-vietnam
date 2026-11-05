# Training study — IBTrACS WP, evaluated on Vietnam-region storms

Common evaluation windows (48 h history available): val 435, test 526 (test years [2021, 2022, 2023, 2024]).

## Stage A — validation (2017–2020), seed 0; each step kept only if it helped

| configuration | 6h | 12h | 24h | 48h | 72h | mean |
|---|---:|---:|---:|---:|---:|---:|
| A0 baseline (box, 24h, L1) | 33 | 67 | 140 | 298 | 466 | 201 |
| A1 + whole-basin data | 32 | 68 | 148 | 319 | 494 | 212 |
| A2 + 48h history | 36 | 71 | 146 | 315 | 489 | 212 |
| A3 + haversine loss (km) | 32 | 66 | 140 | 303 | 475 | 203 |
| A4 + wider/regularised | 34 | 67 | 140 | 305 | 484 | 206 |
| A5 + smaller/lr 5e-4 | 36 | 69 | 145 | 307 | 476 | 207 |
| A6 Transformer (same data/loss) | 34 | 69 | 144 | 309 | 480 | 207 |
| A7 k-NN analog (box) | 34 | 70 | 149 | 328 | 515 | 219 |
| A7 k-NN analog (wide) | 35 | 71 | 151 | 335 | 530 | 224 |
| A8 gradient boosting | 30 | 64 | 142 | 325 | 514 | 215 |

Selected neural config: **A0 baseline (box, 24h, L1)** — {'name': 'A0 baseline (box, 24h, L1)', 'model': 'lstm', 'domain': 'box', 'input_len': 4, 'loss': 'smooth_l1', 'hidden': 128, 'layers': 2, 'dropout': 0.2, 'weight_decay': 1e-05, 'lr': 0.001}
Ensemble members (chosen on validation): ['A0 baseline (box, 24h, L1)', 'A6 Transformer (same data/loss)']

## Stage B — test (2021–2024), seeds [0, 1, 2]

| configuration | 6h | 12h | 24h | 48h | 72h | mean |
|---|---:|---:|---:|---:|---:|---:|
| A0 baseline (box, 24h, L1) | 32 ± 0 | 64 ± 1 | 131 ± 3 | 286 ± 6 | 469 ± 9 | 197 ± 4 |
| A6 Transformer (same data/loss) | 32 ± 1 | 64 ± 2 | 132 ± 5 | 289 ± 10 | 464 ± 11 | 196 ± 5 |
| A7 k-NN analog (box) | 31 | 62 | 129 | 284 | 455 | 192 |
| A8 gradient boosting | 28 | 58 | 126 | 286 | 468 | 193 |
| Ensemble (best_neural+transformer) | 31 ± 1 | 62 ± 1 | 128 ± 2 | 281 ± 4 | 457 ± 4 | 192 ± 2 |

Paired storm-level bootstrap at 72 h (negative = better than baseline):

- A0 baseline (box, 24h, L1) vs baseline: +0 km, 95% CI [+0, +0] over 44 storms
- Ensemble (best_neural+transformer) vs baseline: -8 km, 95% CI [-16, +2] over 44 storms
