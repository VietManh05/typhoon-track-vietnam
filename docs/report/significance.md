# Paired storm-level bootstrap at 72 h

## vs persistence

Reference: Persistence, 72 h, 50 test storms, 5000 storm-level bootstrap resamples (negative = better than the reference).

| method | mean diff (km) | 95% CI | better in % of resamples |
|---|---:|---:|---:|
| CLIPER-proxy | -15 | [-101, +65] | 65% |
| k-NN analog | -201 | [-268, -131] | 100% |
| Gradient boosting | -191 | [-252, -126] | 100% |
| LSTM | -203 | [-262, -145] | 100% |
| Attention-LSTM | -173 | [-229, -116] | 100% |
| Transformer | -200 | [-257, -142] | 100% |

## vs LSTM

Reference: LSTM, 72 h, 50 test storms, 5000 storm-level bootstrap resamples (negative = better than the reference).

| method | mean diff (km) | 95% CI | better in % of resamples |
|---|---:|---:|---:|
| Persistence | +203 | [+145, +262] | 0% |
| CLIPER-proxy | +188 | [+113, +256] | 0% |
| k-NN analog | +3 | [-29, +34] | 43% |
| Gradient boosting | +12 | [-20, +48] | 23% |
| Attention-LSTM | +30 | [+12, +50] | 0% |
| Transformer | +3 | [-16, +22] | 37% |
