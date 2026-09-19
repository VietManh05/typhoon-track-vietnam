# R13 — Nghiệm thu inference/API nháp

- **Trạng thái:** complete trong phạm vi draft/local
- **Files:** `inference/service.py`, `api/app.py`, `api/schemas.py`, `tests/test_inference_api.py`.

Trained path load bundle đúng một lần, dùng shared feature/scaler path và trả 5 horizons với model/dataset/source/time/uncertainty/disclaimer. Missing/corrupt artifact fail closed; baseline chỉ chạy khi được cho phép. Stale observation sinh warning, future/invalid interval trả lỗi. API tests xác nhận auth 401, success 200, validation 422 và rate-limit 429. Output finite được kiểm tra.

Redis read/invalidation và production DB/migration không thuộc acceptance local này và được map tại R14. Full suite: **61 passed**, exit 0.
