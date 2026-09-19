# G02 — Dữ liệu địa lý Việt Nam

- **Ngày:** 2026-09-19.
- **Phạm vi:** T02-001–T02-019.
- **Nguồn:** GADM 4.1 được kiểm chứng là nguồn boundary theo quốc gia nhưng có điều khoản academic/non-commercial và hạn chế redistribution; GSHHG yêu cầu URL release do operator phê duyệt.
- **Implementation:** download adapters lưu lineage; `features/geospatial.py` ép WGS84, chuẩn hóa tên tỉnh, simplify polyline, distance-to-coast, point-in-polygon, bbox spatial index, nearest province và danh mục location ID duy nhất.
- **Kiểm thử:** acceptance fixture phủ CRS sai/đúng, containment, nearest, coastline distance, simplify, Unicode `Đ/đ`, ID và distance của special locations; nằm trong batch 41 passed.
- **Quyết định ngoại vi:** không commit/tái phân phối GADM/GSHHG thật; raw download chỉ chạy khi operator xác nhận licence/release URL.

