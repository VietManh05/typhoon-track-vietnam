# Phase 4 — Backend M3

- **Ngày:** 2026-09-19.
- **Phạm vi:** G16–G20 và S09/S15/S24.
- **Trạng thái:** **complete**.
- **Hoàn tất:** G16/G17/G18/G19/G20 và S09/S15/S24.
- **Focused:** **20 passed**, coverage **83%**, exit 0.
- **PostGIS acceptance:** `tests/integration/test_postgis.py` **1 passed** với `POSTGIS_TEST_URL`; migration upgrade/downgrade, constraints, SRID, GiST và `ST_Intersects` overlap/boundary-touch đã được xác nhận trên PostGIS 16/PostGIS 3.4.
- **Regression:** **149 passed**, exit 0 (`phase4-regression-pytest.xml`).
- **Docker:** Docker Desktop 4.91.0 + WSL 2.7.13 đang chạy; data disk cũ được giữ backup tại `docker_data.vhdx.backup-20260919`.
