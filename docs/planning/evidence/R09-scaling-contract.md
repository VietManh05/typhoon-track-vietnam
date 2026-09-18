# R09 — Scaler train-only

- Trạng thái: complete
- Files: `features/scaling.py`, `tests/test_features.py`, `tests/test_phase2_contracts.py`.

## Kết quả

- Statistics chỉ thay đổi khi gọi `fit`; transform held-out extrema không thay mean train.
- NaN/Inf được điền bằng train-only finite mean; all-missing dùng neutral zero kèm warning.
- Artifact lưu scaler, feature order và fill values; load không fit lại.
- Missing/reordered feature columns bị reject.
- Save/load transform→inverse round-trip đạt sai số tối đa <= `1e-6`.

Kiểm chứng: full suite `49 passed`, exit code 0; JUnit `docs/planning/evidence/phase2-pytest.xml`.
