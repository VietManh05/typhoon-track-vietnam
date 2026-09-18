# R05 — Chốt schema và thời gian

- Trạng thái: complete
- Files: `src/typhoon_vn/ingestion/models.py`, `features/schema.py`, `features/bridge.py`, `api/schemas.py`, `docs/contracts/observations.md`, `tests/test_phase2_contracts.py`.

## Kết quả

- Observation bắt buộc tọa độ hữu hạn, datetime aware/UTC, provenance không rỗng và wind unit thuộc vocabulary hỗ trợ.
- Raw `latitude/longitude` được bridge thành `lat/lon`; knot đổi sang m/s; provenance và acquisition time được giữ.
- API từ chối naive datetime, NaN/Infinity và kiểm tra `valid_time = issue_time + horizon_hours`.

## Kiểm chứng

`.venv\Scripts\python.exe -m pytest -q --basetemp=.pytest-tmp5 --junitxml=docs\planning\evidence\phase2-pytest.xml`

Actual: `49 passed, 2 warnings in 10.45s`; exit code 0. Các test contract gồm timezone +07→UTC, knot→m/s, provenance, NaN/Inf, naive datetime, unknown unit và forecast times.
