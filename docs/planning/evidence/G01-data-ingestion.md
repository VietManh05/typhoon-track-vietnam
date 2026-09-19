# G01 — Ingestion và nguồn gốc dữ liệu

- **Ngày:** 2026-09-19.
- **Phạm vi:** T01-001–T01-083.
- **Nguồn đã kiểm chứng:** CMA Best Track (1949–2025 trên trang chính thức), NOAA IBTrACS v04r01, JMA RSMC archive (1951–2026); JTWC/NCHMF dùng manifest hoặc export được phê duyệt.
- **Implementation:** downloader atomic có timeout, bounded retry, 404 fail-fast, 429/5xx retry, empty-body rejection, SHA-256 và log; parser CMA/IBTrACS/JMA/JTWC/NCHMF; canonical ID/UTC/unit/provenance; partitioned Parquet; conservative merge/conflict; validation/quality report.
- **Kiểm thử:** `python -m pytest tests/test_ingestion.py tests/test_features.py tests/test_phase2_contracts.py tests/test_phase2_data_gate.py -q` nằm trong batch 41 passed. HTTP fixture phủ 200/404/429/timeout/empty; parser fixture phủ bốn nguồn quốc tế; không tải/mirror lịch sử thật trong test.
- **Kết quả:** raw→canonical giữ URL/checksum/source/version/unit/UTC; duplicate/conflict không bị che; suspicious được flag; output ghi atomic.
- **Quyết định ngoại vi:** chức năng tải toàn lịch sử có sẵn nhưng chỉ chạy bằng lệnh operator tường minh sau rà giấy phép/dung lượng. Không coi fixture là dữ liệu chính thức.

