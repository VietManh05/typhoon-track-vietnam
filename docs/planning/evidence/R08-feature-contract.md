# R08 — Feature order

- Trạng thái: complete
- Files: `features/build.py`, `datasets/typhoon_dataset.py`, `docs/contracts/features.md`, `tests/test_phase2_contracts.py`.

Dataset gọi `FeatureBuilder.transform` trước khi chọn columns và dùng `FEATURE_COLUMNS` làm vocabulary/order mặc định. Derived lag/delta được điền theo cách causal tại đầu storm để tensor model hữu hạn. Custom feature list thiếu hoặc trùng bị reject. Persisted scaler kiểm tra missing/reordered columns.

Kiểm chứng: dataset và builder trả cùng thứ tự; model/training regression không còn NaN; full suite `49 passed`, exit code 0.
