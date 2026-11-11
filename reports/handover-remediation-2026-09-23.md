# Kết quả khắc phục trước bàn giao — 2026-09-23

## Phạm vi đạt

- Bản Cloudflare Pages công khai tại <https://baoviet2026.pages.dev/> đã được triển khai lại trên dự án hiện có, không mở dịch vụ trả phí. Bản frontend dùng asset `index-6hKCiF9o.js` và CSS `index-CWSxAr3C.css`.
- Lỗi đăng nhập API key giả đã được sửa: frontend chỉ nhận `authenticated: true` từ `/auth/session`; backend kiểm tra quyền; Pages báo không hỗ trợ xác thực và ẩn nút đăng nhập.
- Pages `/ready` trả 503 JSON thay vì 200 HTML. `/health` vẫn là liveness, không phải khả năng dự báo. Các endpoint xác thực/cảnh báo không có backend trả 503 JSON rõ ràng.
- Badge “LIVE” và chuông cảnh báo chỉ bật khi backend khỏe và feed bão trực tiếp khả dụng; Pages báo `stormFeed:false` nên giao diện giữ đúng trạng thái demo.
- Backend: 254 passed, 1 skipped (PostGIS cần `POSTGIS_TEST_URL`), 3 dependency warnings. Frontend: 19 passed; lint/typecheck, build và kiểm tra Pages output đạt. Black, isort, flake8 đạt trên `src`, `tests`, `migrations`.

## Kiểm tra trên URL công khai

- `/auth/capabilities`: 200 JSON `available:false`.
- `/auth/session`: 503 JSON `authenticated:false`.
- `/token` (POST) và `/alerts` (GET): 503 JSON, không rơi vào trang HTML.
- `/ready`: 503 JSON `status:not_ready`.
- `/health`: 200 JSON, `stormFeed:false`, `alertDelivery:false`.
- `/typhoons/active`: 200 JSON, danh sách rỗng và `feedAvailable:false`.
- Trang chủ và asset `index-6hKCiF9o.js`: HTTP 200.
- Sửa chồng lấn mobile giữa nút lớp bản đồ và ô tìm kiếm; CSS `index-CWSxAr3C.css` đã triển khai và trả HTTP 200. Ảnh kiểm tra công khai ở `reports/qa-mobile-public-final-2026-09-23.png` cho thấy hai control tách nhau ở khung 390×844.

Đã tạo gói mã nguồn demo `reports/typhoon-vn-demo-source-2026-09-23.zip` có `HANDOVER-MANIFEST.json` ghi SHA-256 từng file và được xác minh sau khi đóng gói. Gói loại trừ `.env.preview`, dữ liệu runtime, model, `node_modules` và cache. Gói này là ảnh chụp checkout hiện tại, **không thay cho release commit/tag**; người nhận có thể đối chiếu checksum trong manifest rồi chạy lại kiểm thử theo `docs/deployment.md`.

Smoke test tự động trên URL công khai đạt 23/23 và kiểm tra Chrome DevTools đạt 10/10 mục (trạng thái demo và bố cục). Kết quả lưu tại `reports/demo-release-smoke-2026-09-23.json` và `reports/demo-ui-smoke-2026-09-23.json`. Người nhận ký xác nhận UAT theo `reports/demo-uat-checklist-2026-09-23.md`.

CLI NCHMF chạy được trên nguồn công khai ngày 2026-09-23, tạo snapshot tham khảo gồm 62 quan sát nhiệt độ và 10 liên kết bản tin tại `reports/nchmf-weather-2026-09-23.json`. Snapshot này chưa phải nguồn vị trí/quỹ đạo bão, chưa xác nhận quyền lưu trữ/phân phối dài hạn và không được đưa vào gói nguồn demo.

## Quyết định nghiệm thu

**Có thể nghiệm thu bản demo/hỗ trợ tham khảo với điều kiện người nhận xác nhận UAT giao diện, nội dung và giới hạn dữ liệu. Chưa đủ điều kiện nghiệm thu vận hành dự báo/cảnh báo bão.**

Các cổng còn thiếu không thể được thay bằng code hoặc dữ liệu mẫu: (1) nguồn bão/NCHMF trực tiếp có quyền sử dụng và kiểm tra độ trễ; (2) model được đánh giá trên dữ liệu thực, có bundle promoted; (3) backend HTTPS, PostGIS, worker và `/ready` được smoke trên môi trường đích; (4) người nhận cảnh báo, quy trình phê duyệt, giám sát và rollback; (5) bản mã nguồn sạch được chốt bằng commit/tag và đối chiếu với deploy. Trong lượt này Docker Engine không kết nối được, test PostGIS thật bị skip, không có `checkpoints/promoted/manifest.json` hay `.env.production`. Không được diễn giải bản Pages hoặc demo bão là hệ thống cảnh báo chính thức.

Checkout hiện tại vốn có hàng trăm thay đổi và nhiều file chưa được theo dõi; chưa tự ý stage/commit hoặc xóa chúng. Trước khi giao mã nguồn, cần chủ dự án rà soát thay đổi, tách bí mật/dữ liệu runtime, commit/tag bản đã kiểm tra và lưu hash của gói bàn giao.
