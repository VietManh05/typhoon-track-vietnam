# R12 — Train CLI và integration smoke

- **Trạng thái:** complete
- **Files:** `training/config_loader.py`, `training/run.py`, `cli.py`, `tests/test_training_pipeline.py`.

`typhoon-vn train --config <yaml> --output-dir <dir>` đọc config strict, seed RNG, split whole-storm, lưu split IDs/seed/dataset hash, fit scaler chỉ trên train, train LSTM nhỏ, export và reload bundle. Config unknown/invalid bị reject. Smoke test dùng synthetic data và output luôn ghi rõ không phải skill metric bão thật.

Integration test thực thi 1 epoch trong `tmp_path`, xác nhận bundle reload được và train/val IDs không giao nhau. Full suite: **61 passed**, exit 0.
