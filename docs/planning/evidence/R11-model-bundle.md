# R11 — Model bundle contract

- **Trạng thái:** complete cho local validated bundle; external signing/promotion vẫn là production backlog.
- **Files:** `training/pipeline.py`, `docs/contracts/model-bundle.md`, `tests/test_model_bundle.py`.

Bundle gồm manifest, weights, strict JSON scaler và split manifest. Loader kiểm tra strict schema, allowlist model constructor, feature order/hash, dimensions, calibration horizons và SHA-256 của mọi payload trước deserialize; weights dùng `weights_only=True`. Corrupt checksum, feature/schema mismatch và irregular input fail closed. Export/load/predict round-trip đã test.

Giới hạn được ghi rõ: checksum nội bộ phát hiện corruption nhưng production vẫn cần pin/sign digest manifest ngoài bundle. Không tuyên bố bundle synthetic smoke là promoted production model.

Full suite: **61 passed**, exit 0; JUnit `R10-R14-pytest.xml`.
