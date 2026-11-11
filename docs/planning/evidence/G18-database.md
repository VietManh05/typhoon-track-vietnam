# G18 — Database, PostGIS và migration

- **Ngày:** 2026-09-19.
- **Trạng thái:** complete.
- **Actual:** Alembic upgrade/downgrade, audit/FK/unique/index, geometry SRID và GiST đã pass trên SQLite và PostGIS 16/PostGIS 3.4.
- **Integration:** `tests/integration/test_postgis.py` — **1 passed**.
- **Regression:** 149 passed, exit 0 (`phase4-regression-pytest.xml`).
