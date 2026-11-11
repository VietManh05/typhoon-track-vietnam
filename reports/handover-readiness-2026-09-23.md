# Rà soát sẵn sàng bàn giao — Typhoon VN

Ngày rà soát: 2026-09-23. Checkout: `main` tại `5baf229`, có thay đổi chưa commit. Trang đang công bố: https://baoviet2026.pages.dev/.

## Kết luận

- **Có thể bàn giao bản demo có ghi rõ giới hạn**, sau khi xử lý lỗi đăng nhập giả thành công và đóng gói một phiên bản mã nguồn/tài liệu tái tạo được.
- **Chưa nghiệm thu để bàn giao vận hành dự báo/cảnh báo bão.** Cloudflare Pages là frontend + edge Functions, chưa phải stack FastAPI/PostGIS/model/worker production.

## Kiểm tra đã chạy từ checkout hiện tại

| Cổng | Kết quả |
| --- | --- |
| Backend `pytest -q` | 252 passed, 1 skipped (PostGIS cần `POSTGIS_TEST_URL`), 3 cảnh báo dependency |
| Frontend `npm test`, `npm run lint`, `npm run build` | 17 passed; TypeScript và build pass |
| Python `flake8`, `black --check`, `isort --check-only` | Pass |
| `pip check`, `npm audit --omit=dev --audit-level=high` | Không thấy dependency hỏng; 0 lỗ hổng production được npm báo |
| Plan validator | Pass, 818/818 checkbox được map; công cụ tự báo chưa chạy product tests trong lượt validator |
| Preview Compose `config --quiet` | Pass cú pháp/cấu hình |
| Docker Engine | Không kết nối được `dockerDesktopLinuxEngine`; chưa chạy được container/preview/PostGIS trong lượt này |
| Pages | Trang và asset hiện tại tải được; `/health` báo weather=true, ai=true, stormFeed=false, alertDelivery=false; weather bundle Đà Nẵng HTTP 200 |

## Vấn đề cần chốt trước bàn giao

1. **P1 — Đăng nhập API key có thể báo thành công với key giả trên Pages.** `viz/frontend/src/services/api.ts:25-33` chấp nhận bất kỳ phản hồi HTTP 200 nào từ `/typhoons/active` làm xác thực. Pages Function ở `viz/frontend/functions/typhoons/active.js` luôn trả 200 và không kiểm tra key. Đã xác nhận bằng header `X-API-Key: handover-invalid-test-key` nhận HTTP 200. Không dùng trạng thái này để chứng minh người dùng đã được xác thực. Với bản demo, nên ẩn/vô hiệu hóa đăng nhập; với backend thật, phải xác minh key ở endpoint bảo vệ đúng quyền.
2. **P1 — Chưa có dự báo bão vận hành trên bản đang công bố.** `/typhoons/active` trả `typhoons: []`, `feedAvailable: false`; `/api/weather/nchmf` trả HTTP 503; `/health` báo `alertDelivery: false`. Dữ liệu bão demo và báo cáo model synthetic không phải bằng chứng kỹ năng dự báo thật.
3. **P1 — Chưa qua cổng hạ tầng/model production.** Docker Engine không hoạt động trong lượt rà soát; test PostGIS thật bị skip; không thấy `checkpoints/promoted/manifest.json` hoặc `.env.production`. Chưa có smoke `/ready`, DB, model bundle và worker trên stack production.
4. **P1 — Gói nguồn chưa tái tạo được từ commit.** `HEAD` là `5baf229` ngày 2026-09-19, nhưng checkout có 705 mục tracked thay đổi và tổng 1.090 mục modified/untracked; riêng `viz/frontend/node_modules` có 555 mục tracked thay đổi. Nhiều source Functions/frontend đang untracked. Bản Pages đang chạy không tương ứng với một commit/tag sạch có thể checkout và build lại. `git diff --check` toàn repo cũng fail do whitespace trong node_modules được track và blank EOF trong HTML.
5. **P2 — Readiness trên Pages không đại diện cho backend.** `GET /ready` trả HTTP 200 `text/html` do SPA fallback, không phải JSON readiness. Chỉ `/health` edge báo liveness/capabilities. Không dùng `/ready` của Pages làm tín hiệu sẵn sàng vận hành.

## Điều kiện bàn giao đề xuất

**Bản demo:** sửa/ẩn đăng nhập sai; xác nhận chức năng bản đồ, thời tiết, AI và giao diện điện thoại với người nhận; chốt source commit/tag cùng URL deploy; bàn giao tài liệu sử dụng và ghi rõ bão/NCHMF/cảnh báo đang thiếu nguồn live.

**Bản vận hành:** bổ sung backend HTTPS, nguồn bão/NCHMF có quyền dùng và provenance, model bundle đã đánh giá/calibrate trên dữ liệu thực, PostGIS/Redis/worker chạy thật, `/ready` JSON đạt, quy trình alert có người nhận/duyệt, giám sát/backup/rollback và UAT trên môi trường đích. Mỗi cổng cần bằng chứng gắn với phiên bản phát hành.
