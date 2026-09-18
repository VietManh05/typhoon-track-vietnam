# R04 — Baseline pytest

- Thời gian: 2026-09-18 22:00 +07:00
- Trạng thái: complete

## Lệnh

`.venv\Scripts\python.exe -m pytest -q --basetemp=.pytest-tmp --junitxml=docs\planning\evidence\R04-pytest.xml`

- Expected: suite collection thành công; ghi đầy đủ pass/fail và JUnit XML; không sửa checkpoint workspace.
- Actual: `39 passed, 2 warnings in 22.62s`.
- Exit code: 0.
- Report: `docs/planning/evidence/R04-pytest.xml`.

## Cảnh báo

1. FastAPI TestClient cảnh báo `httpx` integration deprecated và gợi ý `httpx2`.
2. Starlette cảnh báo alias `anyio.abc.BlockingPortal` deprecated.

Hai cảnh báo nằm trong dependency, không làm baseline thất bại. Checkpoint workspace đã được cô lập ở R03.
