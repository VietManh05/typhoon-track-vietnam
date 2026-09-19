# Phase 2 — Kiểm chứng nền tảng và dữ liệu

- **Trạng thái:** complete (2026-09-19).
- **Scope hoàn tất:** R01–R14; G00–G06 (256/256 WBS tasks); S01, S03, S08.
- **Plan gate:** `python -X utf8 docs/planning/tools/validate_plan.py` → pass; 818/818 source checkboxes, 731 dependency nodes, 2.977 links, roadmap hash unchanged.
- **Data acceptance:** 41 passed; JUnit `phase2-data-gate-pytest.xml`.
- **Full regression:** 105 passed, 2 dependency deprecation warnings; JUnit `phase2-final-pytest.xml`.
- **Lint:** flake8 pass; isort/Black pass trên 83 Python files thuộc phạm vi. Hai file đồng thời `tests/test_frontend_build.py` và `tests/test_refactor_root_imports.py` được giữ nguyên/loại khỏi lint Phase 2; cả hai vẫn được full pytest collect.
- **DVC:** fixture stage sinh lock/output; repro lần hai no-op; status up to date; không remote/push.
- **Ngoại vi còn cần operator ở phase phù hợp:** tải/redistribute nguồn thật theo licence, credentials ERA5, approved JTWC/NCHMF/PCTT exports, GSHHG release URL và DVC remote.
- **Git:** không tạo commit/push mới khi đóng phase; thay đổi user/frontend/concurrent được giữ nguyên.

