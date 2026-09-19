# R14 — Đối chiếu gap vận hành

- **Trạng thái:** complete (audit/backlog mapping, không phải production readiness)
- **Phụ thuộc:** R13 complete.

## Ma trận gap

| Nhóm | Hiện trạng/reproducer | Task WBS | Definition of Done còn lại | Blocker |
|---|---|---|---|---|
| G18 DB/PostGIS | `Store.__init__` gọi `metadata.create_all`; không có `alembic.ini/migrations`; payload JSON, không geometry/GiST/FK | T18-001–T18-019 | Alembic upgrade/downgrade trên PostGIS thật, timestamptz, geometry SRID 4326, GiST/FK/constraints và audit columns | Docker/PostGIS không có trên máy; cần migration design |
| G20 Redis | API chỉ `setex`; `compute` không `get`; TTL hard-code; không invalidation | T20-001–T20-006, T19-008 | Cache adapter read/write/expiry/invalidate, model+input revision keys, corrupt/outage fallback tests | Redis integration chưa chạy |
| G19 worker | `run_worker` chỉ đọc JSON snapshot; cùng revision vẫn infer; không cursor/retry hữu hạn/status; compose thiếu worker | T19-001–T19-010 | Live provider interface, persistent revision cursor, infer-on-change, bounded retry/backoff/status, worker service | Provider authority/credentials/terms chưa chốt |
| G22 alerts | Draft/cooldown/radius có; subscription không owner, `/alerts` trả toàn bộ, không channel/retry/history | T22-001–T22-013 và ownership prerequisite | Principal-scoped subscription/alerts, issue time/severity, fake transport, durable retry/dedup/history | Chưa có auth/tenant và delivery provider/consent policy |
| Deploy | compose truyền `DATABASE_URL` nhưng app dùng `OPERATIONAL_DATABASE_URL`; cache chưa bật; API dùng `--reload` | G18/G19/G20 | Sửa env/profile, migrate-before-start, worker service, production image/config test | Docker không có trong PATH |

## Kết luận

Local unit/integration suite pass nhưng **hệ thống chưa production-ready**. DB vẫn là source of truth; Redis read path chưa tồn tại; worker chưa live; alert chỉ draft. Không gửi cảnh báo thật và không tuyên bố PostGIS/Redis đã kiểm chứng.

Task kế tiếp theo phụ thuộc: **G18 migration/schema**, sau đó G20 cache, G19 live worker, ownership/auth và G22 delivery.
