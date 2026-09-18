# R02 — Kiểm tra Python và extras

- Thời gian: 2026-09-18 22:00 +07:00
- Trạng thái: complete

## Lệnh và kết quả

1. `.venv\Scripts\python.exe --version`
   - Expected: Python 3.11.
   - Actual: `Python 3.11.9`.
   - Exit code: 0.
2. `.venv\Scripts\python.exe -m pip check`
   - Expected: không có dependency conflict.
   - Actual: `No broken requirements found.`
   - Exit code: 0.
3. Import smoke: `numpy,pandas,torch,fastapi,sqlalchemy,redis`
   - Expected: tất cả import thành công và in phiên bản.
   - Actual: numpy 2.4.6; pandas 2.3.3; torch 2.14.0+cpu; FastAPI 0.141.1; SQLAlchemy 2.0.54; Redis 5.3.1.
   - Exit code: 0.

## Kết luận

Môi trường Python và các extras cần cho baseline hiện dùng được. Đây là bằng chứng import/dependency, không phải bằng chứng product tests. Tiếp theo: R03 cô lập checkpoint test.
