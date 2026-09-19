# G03 — Pipeline làm sạch

- **Ngày:** 2026-09-19.
- **Phạm vi:** T03-001–T03-020.
- **Implementation:** `Phase2Pipeline` ghép parse→merge→coerce/validate→deduplicate→sort→interpolate→feature→atomic Parquet; cleaning chỉ nội suy trong từng storm, không fill 0 cho unknown; duplicate timestamp và jump bất thường có reject/flag; quality JSON ghi counters/ranges.
- **Kiểm thử:** fixture 5 fix có một giá trị wind thiếu được nội suy và flag; export Parquet/quality round-trip; các tests cleaning/contract hiện có phủ invalid range, duplicate, time order và storm isolation. Batch mục tiêu: 41 passed.
- **Kết quả:** output deterministic theo fixture và không để file `.tmp` sau lỗi/thành công.

