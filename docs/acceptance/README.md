# Hồ sơ nghiệm thu — Typhoon VN (G29, 28 tiêu chí)

Ngày nghiệm thu: 2026-11-05 · Nhánh `VietManh05/review-project-next-steps` (PR #1)
· Website: <https://baoviet2026.pages.dev>

Quy ước: **Đạt** = có kết quả chạy thật kiểm chứng; **Đạt một phần** = có nhưng
còn giới hạn nêu rõ; **Chưa đạt** = chưa có. Không đánh "Đạt" chỉ vì file tồn tại.

## Kiểm tra tự động tại thời điểm nghiệm thu

| Lệnh | Kết quả |
|---|---|
| `python -m pytest -q` | 171 passed, 3 skipped (spec chưa có implementation, có lý do) |
| `flake8` / `isort --check` / `black --check` trên `src tests scripts` | sạch |
| `cd viz/frontend && npx tsc --noEmit && npm test` | TypeScript sạch; 29/29 test Node |
| `python scripts/check_dashboard_sync.py` (sau `vite build --outDir dist`) | dashboard khớp bản build (44 file) |

## Bảng nghiệm thu

| Mã | Tiêu chí | Kết quả | Bằng chứng |
|---|---|---|---|
| A29-001 | Dữ liệu lịch sử có provenance | **Đạt** | IBTrACS v04r01 kèm SHA-256 file nguồn (`B01`), lineage JSON khi tải (`ingestion/lineage.py`), `source_url` trên mỗi quan trắc; dữ liệu demo/phát lại gắn nhãn `synthetic-demo`, hindcast gắn "IBTrACS best track (hindcast)" |
| A29-002 | Pipeline ingestion tự động | **Đạt** | `typhoon-vn worker --ibtracs-active` (service `worker` trong compose, 6 h/lần); chạy thật 2026-11-05 lấy bão IN-FA (WP302026); cron mẫu `infra/scheduler` |
| A29-003 | Validation và cleaning | **Đạt** | `features/cleaning.py` (toạ độ/vật lý, khử trùng, sắp xếp, nội suy, gắn cờ); test `tests/test_features.py`; báo cáo làm sạch trong `B01` |
| A29-004 | Feature engineering | **Đạt** | 47 đặc trưng quỹ đạo/thời gian/bờ biển dùng chung train–serve; 11 đặc trưng dòng dẫn đường (`features/steering.py`, test `tests/test_steering.py`) |
| A29-005 | Không rò rỉ dữ liệu | **Đạt** | Chia theo năm, giữ nguyên cả cơn bão; scaler fit trên train; mọi lựa chọn trên validation, test chạy một lần (`training_study.md`, `steering_study.md`); thư viện k-NN phục vụ loại bão test |
| A29-006 | Train/val/test độc lập | **Đạt** | train 1980–2016, val 2017–2020, test 2021–2024 (895/110/84 bão) |
| A29-007 | Baseline | **Đạt** | Persistence, CLIPER-proxy (`models/baselines.py`); 72 h: 676 / 677 km |
| A29-008 | Ít nhất một model ML hoạt động | **Đạt** | LSTM phục vụ qua API/website; thêm k-NN, gradient boosting, Attention-LSTM, Transformer (`comparison.md`) |
| A29-009 | Dự báo nhiều mốc | **Đạt** | 6/12/24/48/72 h |
| A29-010 | Metric theo km | **Đạt** | Sai số vòng lớn (`evaluation/metrics.py`); along/cross-track |
| A29-011 | Backtest | **Đạt** | `evaluation/backtest.py`; 714 cửa sổ test; 20 hindcast bão ảnh hưởng VN (`export_hindcast.py`) |
| A29-012 | Uncertainty/cone | **Đạt** | Nón hiệu chỉnh phân vị 80% trên validation; độ phủ test 82–86% (`B01`) |
| A29-013 | Model version | **Đạt** | Bundle có `version`, `dataset_version`, checksum; API trả `model_revision` (SHA-256); registry + promotion gate + rollback (`tests/test_registry.py`) |
| A29-014 | Inference service | **Đạt** | `inference/service.py`, `inference/analog.py`; dự báo qua container trùng khớp hindcast công bố |
| A29-015 | FastAPI | **Đạt** | `/health`, `/ready`, `/version`, `/forecast`, `/typhoons/*`; chế độ production bắt buộc API key, không fallback baseline (đã chạy thật) |
| A29-016 | PostgreSQL/PostGIS | **Đạt một phần** | Alembic migration kiểm chứng trên PostGIS 16-3.4 (Docker) và trong CI; **chưa dùng cột/truy vấn không gian** — PostGIS đang được dùng như PostgreSQL |
| A29-017 | Dashboard bản đồ | **Đạt** | <https://baoviet2026.pages.dev>: bão JMA trực tiếp, chế độ "Dự báo lại" |
| A29-018 | Actual + forecast track | **Đạt** | Quỹ đạo quan trắc, dự báo, quỹ đạo thực tế sau dự báo (tím) và gợi ý k-NN (hồng) |
| A29-019 | Vùng ảnh hưởng | **Đạt** | Tỉnh nằm trong nón bất định + khoảng cách gần nhất tới trọng tâm 63 tỉnh theo từng mốc dự báo (dashboard, `calculateProvinceImpacts`); `/typhoons/{id}/impact` cho một vị trí. Phạm vi: hình học (không mô hình gió/mưa/lũ), giao diện ghi rõ |
| A29-020 | Cảnh báo nếu triển khai | **Đạt** | Đăng ký vị trí/bán kính/thời hạn → bản nháp cảnh báo idempotent có cooldown; kênh gửi webhook ký HMAC-SHA256, thử lại tối đa 5 lần, không gửi trùng, chỉ HTTPS (`operations/delivery.py`, `tests/test_alert_delivery.py` với máy nhận cục bộ). **Tắt mặc định** (`ALERT_DELIVERY_ENABLED`) — bật khi có phê duyệt nghiệp vụ |
| A29-021 | Unit/integration/model tests | **Đạt** | 171 test Python (unit, API, migration SQLite/PostGIS, model, pipeline) + 29 test Node (Functions, frontend) |
| A29-022 | Docker | **Đạt một phần** | Image build và chạy `healthy`, user không root, phục vụ model đã train (2026-11-05, commit `5a55fd0`); bản sửa bảo mật cài torch (`cc5c19c`) **chưa build lại** do máy thiếu bộ nhớ |
| A29-023 | CI/CD cơ bản | **Đạt một phần** | Workflow lint/test/PostGIS/frontend/đồng bộ dashboard; **chưa chạy được** vì tài khoản GitHub bị khoá do billing; deploy Pages thủ công bằng `wrangler` |
| A29-024 | Logging/monitoring cơ bản | **Đạt** | Log mỗi request (request id, path, status, ms) + header `X-Request-ID`; `/metrics` định dạng Prometheus (histogram độ trễ, số dự báo, lỗi); **giám sát chất lượng mô hình thực tế**: dự báo đã phát được đối chiếu quan trắc đến sau (`operations/monitoring.py`, `typhoon-vn monitor`, exit 2 khi suy giảm). Chạy trên 20 hindcast: độ phủ nón 80/85/95/95/90% tại 6–72 h, sai số 72 h 408 km → `ok` |
| A29-025 | Tài liệu cài đặt | **Đạt** | `README.md`, `docs/frontend.md`, `.env.example`, `make dashboard`, mục "Tái lập kết quả" trong báo cáo |
| A29-026 | Tài liệu kiến trúc | **Đạt** | `docs/architecture.md` (cập nhật theo hệ thống thực tế) |
| A29-027 | Báo cáo đánh giá | **Đạt** | `docs/report/README.md` + `comparison.md`, `significance.md`, `training_study.md`, `steering_study.md`, `cases.md` |
| A29-028 | Disclaimer rõ ràng | **Đạt** | Trong mọi response API, banner website, chế độ dự báo lại, báo cáo |

**Tổng hợp:** 25 Đạt · 3 Đạt một phần (A29-016 PostGIS không gian, A29-022 Docker build lại, A29-023 CI do billing) · 0 Chưa đạt.

## Kết quả mô hình (tóm tắt)

- Mô hình đang phục vụ (LSTM, chỉ quỹ đạo), test 2021–2024: 34 / 66 / 135 / 294 /
  470 km tại 6–72 h; tốt hơn persistence ~30% tại 72 h (có ý nghĩa thống kê).
- Thêm dòng dẫn đường NCEP + ensemble LSTM/Transformer (chọn trên validation):
  72 h tốt hơn mô hình đang phục vụ **35 km, KTC 95% [−62, −9]**; trung bình các
  mốc 179 vs 197 km. **Chưa đưa vào vận hành** (cần dữ liệu khí quyển tại thời
  điểm dự báo).

## Rủi ro và việc còn mở

1. **AI chat `/api/ai/chat`** (có từ trước): giới hạn tần suất theo isolate, Origin
   tùy chọn → có thể bị gọi hàng loạt làm tốn quota Ollama. Đề xuất: Turnstile
   (miễn phí) + giới hạn chi tiêu phía Ollama.
2. **GitHub Actions** bị khoá do billing → CI chưa chạy; cần mở khoá tại
   github.com/settings/billing.
3. **Docker** (cần ~4 GB RAM trống, hiện bị chiếm bởi ứng dụng khác): build lại sau `cc5c19c`:
   `docker build -f infra/docker/Dockerfile -t typhoon-vn .`
4. **Đưa mô hình có dòng dẫn đường vào vận hành**: cần nguồn phân tích khí quyển
   gần thời gian thực (ví dụ GFS analysis), mở rộng định dạng bundle cho cột môi
   trường và ensemble, hiệu chỉnh lại nón.
5. **Ca khó (YAGI 2024)**: mọi mô hình vẫn dự báo đổi hướng tây bắc; cần dữ liệu
   độ phân giải cao hơn / đặc trưng dạng ảnh.
6. JMA không cung cấp thời điểm cho quỹ đạo quá khứ, nên website không chạy mô
   hình trên bão đang hoạt động (chỉ trên hindcast).
