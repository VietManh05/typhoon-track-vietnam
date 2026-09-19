# Phase 4 prework — resilient forecast cache contract

- **Thời gian:** 2026-09-19 (Asia/Ho_Chi_Minh)
- **Phạm vi:** prework cho G20/T20-002..T20-006 bằng fake Redis; không cần dữ liệu Phase 2, model Phase 3 hoặc Redis service thật.
- **Trạng thái planning:** không chuyển G20/T20 sang complete vì dependency G17 và các gate M1/M2 chưa đạt.

## Thay đổi

- Thêm `src/typhoon_vn/operations/cache.py` với `ForecastCache` và protocol Redis tối thiểu.
- Cache key canonical bao gồm storm ID, toàn bộ input revision và model revision.
- Payload ghi JSON deterministic với TTL bắt buộc dương.
- Read/write/invalidation fail-open khi Redis outage để caller tiếp tục qua durable DB/compute path.
- Invalidation theo storm xóa mọi input/model revision nhưng không ảnh hưởng storm khác.
- Thêm `tests/test_cache.py` dùng fake Redis in-memory để kiểm chứng độc lập external service.
- Không sửa `api/app.py`, `operations/store.py` hoặc `operations/worker.py` vì đang có thay đổi đồng thời; wiring API được giữ cho task G17/G20 chính thức.

## Kiểm chứng

- Focused cache tests ban đầu: **5 passed in 0.09s**.
- Cache + API/health regression: **10 passed, 2 dependency warnings in 6.23s**, exit 0.
- Full suite: **95 passed, 2 dependency warnings in 16.39s**, exit 0.
- Target flake8/Black/isort cho `cache.py` và `test_cache.py`: pass.
- JUnit: `docs/planning/evidence/phase4-cache-prework-pytest.xml`.
- Repository-wide flake8 còn bị chặn bởi ba F401 trong `tests/test_frontend_build.py`, file frontend đồng thời ngoài lát cắt này.

## Giới hạn

Đây là adapter contract đã kiểm chứng bằng fake. Chưa wiring vào FastAPI, chưa chứng minh Redis thật, DB fallback end-to-end, observation event invalidation hoặc model promotion invalidation. Vì vậy G20 và Phase 4 vẫn pending.
