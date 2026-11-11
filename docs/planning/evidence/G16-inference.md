# G16 — Dịch vụ inference

- **Ngày:** 2026-09-19.
- **Trạng thái:** complete.
- **Actual:** Load bundle một lần, shared scaler/schema, direct multi-horizon, output vật lý/provenance, cache thread-safe và fallback có cờ/lý do/log.
- **Focused:** **20 passed**, exit 0 (`phase4-focused-pytest.xml`).
- **Coverage:** **83%** trên module Phase 4 (`phase4-coverage.xml`).
- **Regression:** **148 passed, 1 skipped**, exit 0 (`phase4-regression-pytest.xml`).
- **Skip duy nhất:** `tests/integration/test_postgis.py` cần `POSTGIS_TEST_URL`; máy hiện tại không có Docker executable.
- **Quality:** flake8 toàn `src tests migrations`, Black toàn phạm vi và compileall đều pass; isort riêng file Phase 4 pass.
