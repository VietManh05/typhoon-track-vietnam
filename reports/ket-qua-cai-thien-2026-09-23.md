# Kết quả cải thiện sau review — 23/09/2026

Đã triển khai sửa chữa cho **15/15 mục trong báo cáo**, kiểm chứng ở phạm vi
local dưới đây. Điều này không đồng nghĩa đã nghiệm thu production: Docker daemon
không chạy, PostGIS thật chưa chạy lại, chưa có model nghiệp vụ được train lại.

## Trạng thái từng mục

| Mục | Sửa đổi | Bằng chứng/giới hạn |
| --- | --- | --- |
| R01 | Tách input scaled khỏi target WGS84 | Test mọi sample giữ nguyên target và source frame |
| R02 | Backtest nhận scaler; thêm `backtest_bundle`; từ chối learned model thiếu scaler | Backtest/serving parity trên cửa sổ có lịch sử motion/lag |
| R03 | Hai migration adoption riêng: archive schema cũ rồi backfill | SQLite có dữ liệu giữ đủ observation/forecast/points/subscription/alert; mở lại không nhân đôi; lỗi dữ liệu rollback cả DDL; unknown schema bị từ chối |
| R04 | Bắt RedisError ở forecast/weather cache, cả ghi và invalidation | Test ConnectionError và TimeoutError; API forecast vẫn trả kết quả, weather fallback memory hoạt động |
| R05 | Migration đặt trong package, đường dẫn tuyệt đối từ module; Dockerfiles cập nhật | Cài wheel bằng pip vào thư mục tạm; process `-I` ở cwd khác repo mở Store memory/file thành công |
| R06 | FastAPI có `/api/weather/bundle` | Endpoint test trả đúng `{current,hourly,daily}`; AI FastAPI trả 503 có giải thích, chưa bổ sung adapter AI |
| R07 | Dashboard đăng nhập account/API key, header credential chỉ lưu memory; proxy `/token` | Test login/key/bearer/logout/401, type-check/build đạt; chưa chạy browser/nginx production end-to-end |
| R08 | Lấy uncertainty_method từ bundle | Test giữ nguyên nhãn heuristic |
| R09 | Đọc feature/scaler hash đúng trường manifest | Test response khớp digest bundle |
| R10 | Export weights từ best.pt, giữ last.pt cho resume | Test hai epoch có validation xấu đi, bundle bằng best và khác last |
| R11 | Promotion kiểm tra finite và miền giá trị, cả policy thresholds | Test NaN/Inf/error âm/coverage vượt 1 bị từ chối |
| R12 | Worker/API cùng dùng request canonical và model cache revision | Test snapshot worker tạo đúng key API đọc |
| R13 | Worker CLI tạo/đóng Redis client và truyền cache vào run_worker | Test snapshot invalidate active-list; Redis/worker container thật chưa chạy |
| R14 | Token monitoring riêng chỉ có quyền `/metrics`, mount secret vào API/Prometheus | API tests: metrics token đọc metrics được, không đọc storm được; compose config pass; scrape thật chưa chạy |
| R15 | Format các file sửa và test_api_auth.py | Black/isort/flake8 toàn bộ src/tests đạt |

Bổ sung liên quan: cache identity có manifest digest để model train lại cùng display
version không lấy forecast cũ; Redis hit cũng làm mới cảnh báo quan trắc quá 24h;
Settings TTL/max entries được truyền vào forecaster; CI chạy frontend tests và
kiểm chứng installed wheel.

## Kiểm chứng thực chạy

- Full backend: **252 passed, 1 skipped, 3 warnings**, 27,08 giây.
  [JUnit](improvements-20260923-pytest.xml).
- Skip duy nhất: PostGIS cần `POSTGIS_TEST_URL`. Docker CLI có mặt nhưng daemon
  không kết nối được (`dockerDesktopLinuxEngine` pipe không tồn tại).
- Frontend: **17/17 tests**, TypeScript pass; production build pass (1.925 modules).
- Flake8 và isort check: pass. Black check: **139 files unchanged**.
- Wheel: build/cài `--no-deps`/startup memory SQLite và file SQLite ngoài repo: pass.
  Dependency dùng lại từ venv, không kiểm chứng một máy hoàn toàn sạch.
- Production compose: `config --quiet` pass khi dùng `configs/deploy.env.example`
  cho cả interpolation và `TYPHOON_ENV_FILE`; đây là kiểm tra cấu hình, không chạy container.
- Không chạy provider thời tiết/Ollama thật, gửi cảnh báo, train/promote model
  production, migrate database vận hành hoặc deploy.

Các lỗi đã có trong báo cáo cũ được giữ nguyên làm snapshot trước sửa. Script probe
được điều chỉnh để vẫn chạy sau khi Store khởi tạo thành công; nó ưu tiên wheel
trong `.pytest-temp/improved-wheel`. Regression tests mới nằm tại
`tests/test_review_regressions.py`; frontend tests thêm trong `viz/frontend/tests/api.test.mjs`.

## Thay đổi tương thích cần chú ý

1. **Bundle schema 2:** schema 1 bị từ chối. Cần train và đánh giá lại model cũ;
   không sửa manifest version bằng tay. Các trọng số cũ không bị xóa hay ghi đè.
2. **Database legacy:** dừng writer cũ và backup trước khi rollout. Archive
   `legacy_v1_*` được giữ; adoption forward-only, có rollback transaction khi lỗi.
   Downgrade tự động database đã adoption bị chặn để tránh mất dữ liệu mới.
3. **Monitoring:** tạo file token ngẫu nhiên theo `METRICS_TOKEN_HOST_FILE` trước
   khi khởi động production compose. Không có secret mới nào được tạo/commit trong phiên.
4. **Dashboard auth:** credential trong memory, reload cần đăng nhập lại. Đây là
   tích hợp với auth hiện có, không mở rộng thành hệ thống nhiều tenant.

Xem [hướng dẫn nâng cấp](../docs/review-upgrade-2026-09-23.md) và
[hợp đồng model bundle](../docs/contracts/model-bundle.md).

Skill `ecc:database-migrations` được dùng để tách migration schema/data, giữ
migration operational đã có và lưu archive phục vụ khôi phục. Test hiện xác nhận
SQLite; cần thêm drill PostgreSQL trên backup có dung lượng đại diện trước rollout.

## File/nhóm file đã thay đổi

- `datasets/typhoon_dataset.py`, `evaluation/backtest.py`, `evaluation/__init__.py`.
- `training/run.py`, `training/pipeline.py`, `training/registry.py`, `inference/service.py`.
- `operations/store.py`, `cache.py`, `worker.py`, package migrations/legacy_migrations;
  migration operational gốc được di chuyển vào package.
- `api/app.py`, `settings.py`, `weather/cache.py`.
- `viz/frontend/src/services/api.ts`, `components/AuthControl.tsx`, `Header.tsx`,
  `AlertModal.tsx`, Vite proxy và tests; dashboard assets được build lại từ source.
- `pyproject.toml`, `alembic.ini`, Dockerfiles/nginx/compose/Prometheus, CI,
  `configs/deploy.env.example`, ignore rules cho secrets.
- Regression tests, `scripts/verify_wheel.py`, tài liệu/báo cáo liên quan.

Không reset/stage/commit/push. Build thay các bundle frontend cũ bằng bundle mới;
source frontend vẫn giữ trong workspace để tái build. Những thay đổi không liên
quan đã có trước được giữ nguyên.
