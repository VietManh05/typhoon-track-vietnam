# Phase 3 — Training, evaluation, uncertainty và registry

- **Ngày:** 2026-09-19.
- **Phạm vi:** G07–G15 và S02/S04/S05/S06/S07; 146 task WBS + 5 supplemental.
- **Focused:** **61 passed**, 1 warning, exit 0 (`phase3-functional-pytest.xml`).
- **Regression ngoài ba module API/frontend lỗi collection:** **131 passed**, 1 warning, exit 0 (`phase3-regression-pytest.xml`).
- **Lint/compile Phase 3:** flake8 và compileall trên source/test/script Phase 3 đều exit 0 trong lượt xác minh cuối.
- **Functional artifacts:** `reports/evaluation/persistence-backtest.json`, `persistence-track-error.svg`, `calibrated-cone-synthetic.json`, `quantile-calibration-synthetic.json`, `sequence-length-ablation.json`.
- **Full-suite record:** `phase3-full-pytest.xml` có 3 collection errors do `APIKeyHeader` chưa được import trong `src/typhoon_vn/api/app.py`. Ở trạng thái worktree cuối, `compileall src tests` còn báo dấu `)` dư tại `app.py:319`. Các thay đổi API/frontend này nằm ngoài phạm vi Phase 3 nên không được sửa trong lượt chốt này.
- **Tuyên bố evidence:** kết quả trên xác nhận contract chức năng/reproducibility bằng fixture local/synthetic. Không xác nhận skill khí tượng trên dữ liệu thật, operational calibration hoặc quyền promote production.

## Gate evidence

- [G07 — Baseline cổ điển](G07-baselines.md)
- [G08 — LSTM cơ sở](G08-lstm.md)
- [G09 — Seq2Seq, attention và Transformer](G09-sequence-models.md)
- [G10 — Loss và tối ưu](G10-loss-optimization.md)
- [G11 — Bất định và cone](G11-uncertainty.md)
- [G12 — Training tái lập](G12-training.md)
- [G13 — Đánh giá và backtest](G13-evaluation.md)
- [G14 — Tuning và kiểm định theo mùa](G14-tuning-validation.md)
- [G15 — Model registry và promotion](G15-registry.md)
