# Steering-flow study — NCEP/NCAR R1 predictors

Evaluation windows (Vietnam region, 48 h history): val 435, test 526.
Environmental predictors: dlm_u, dlm_v, u500, v500, shear_u, shear_v, z500, dz500_n, dz500_s, dz500_e, dz500_w.

## Stage A — validation 2017–2020 (seed 0)

| configuration | 6h | 12h | 24h | 48h | 72h | mean |
|---|---:|---:|---:|---:|---:|---:|
| P0 LSTM track-only (baseline) | 33 | 67 | 140 | 298 | 466 | 201 |
| E1 LSTM + steering (box) | 33 | 64 | 131 | 284 | 446 | 192 |
| E2 LSTM + steering (whole basin) | 31 | 61 | 129 | 293 | 472 | 197 |
| E3 + haversine loss | 31 | 60 | 128 | 282 | 450 | 190 |
| E4 + wider/regularised | 32 | 61 | 129 | 281 | 439 | 188 |
| E5 Transformer + steering | 33 | 61 | 126 | 279 | 450 | 190 |
| E6 gradient boosting + steering | 27 | 56 | 121 | 282 | 472 | 192 |
| E7 k-NN analog + steering | 34 | 67 | 139 | 306 | 486 | 206 |

Selected: **E4 + wider/regularised**; ensemble members: ['E4 + wider/regularised', 'E5 Transformer + steering']

## Stage B — test 2021–2024 (seeds [0, 1, 2])

| configuration | 6h | 12h | 24h | 48h | 72h | mean |
|---|---:|---:|---:|---:|---:|---:|
| P0 LSTM track-only (baseline) | 32 ± 0 | 64 ± 1 | 131 ± 3 | 286 ± 6 | 469 ± 9 | 197 ± 4 |
| E4 + wider/regularised | 30 ± 1 | 58 ± 1 | 118 ± 5 | 270 ± 9 | 465 ± 13 | 188 ± 6 |
| E5 Transformer + steering | 30 ± 1 | 57 ± 2 | 115 ± 2 | 265 ± 2 | 450 ± 3 | 183 ± 2 |
| E6 gradient boosting + steering | 26 | 50 | 106 | 260 | 437 | 176 |
| E7 k-NN analog + steering | 30 | 58 | 119 | 270 | 450 | 185 |
| Ensemble (neural+transformer) | 28 ± 1 | 54 ± 0 | 112 ± 1 | 259 ± 5 | 443 ± 12 | 179 ± 4 |

Paired storm-level bootstrap at 72 h (negative = better than track-only):

- E4 + wider/regularised vs P0 LSTM track-only (baseline): -18 km, 95% CI [-50, +12] over 44 storms
- Ensemble (neural+transformer) vs P0 LSTM track-only (baseline): -35 km, 95% CI [-62, -9] over 44 storms

## YAGI 2024 (issued 2024-09-04 06Z), 72 h

- P0 LSTM track-only (baseline): 623 km
- E4 + wider/regularised: 673 km
- Ensemble (neural+transformer): 664 km
- E7 k-NN analog + steering: 530 km
