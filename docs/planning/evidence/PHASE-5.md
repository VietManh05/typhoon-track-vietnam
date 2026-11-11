# Phase 5 — Dashboard và cảnh báo (local-ready)

- Thời điểm: 2026-09-20.
- Phạm vi: G21/G22 và S10-S14.
- Trạng thái: **local-ready**, chưa production-ready và chưa gửi cảnh báo thật.

## Kết quả

- React/TypeScript/Leaflet dashboard build và type-check thành công; có track thực/dự báo, cone, timeline, tỉnh/thành, responsive states, VI/EN và theme lưu local.
- Không còn mô phỏng đăng ký cảnh báo thành công khi API lỗi.
- Không gắn nhãn tọa độ demo là dự báo chính thức. Overlay NCHMF/JTWC chỉ được phép khi API có bulletin ghép đúng storm, issue time và valid time; hiện unavailable.
- Alert domain có rule radius/lead, severity, source/issue-time/disclaimer, idempotency, cooldown, retry hữu hạn, history/dead-letter.
- Email/SMS/Telegram/Zalo chỉ là adapter bị vô hiệu hóa; test chỉ dùng fake transport.
- Webhook tùy chọn có payload version/delivery ID, HMAC-SHA256, replay window và chặn SSRF/private destinations.

## Kiểm chứng

- `cd viz/frontend && npm run build && npm run lint` → pass; Vite chỉ cảnh báo chart chunk 507.45 kB.
- Focused Phase 5 pytest → 6 passed.
- Full regression → 155 passed, 1 skipped (PostGIS URL không được cung cấp trong lượt chạy), 3 warnings; JUnit: `phase5-regression-pytest.xml`.
- Black/isort/flake8 trên Python Phase 5 → pass.
- Planning validator → pass, 818/818 checkbox mapped, source unchanged.

## Giới hạn vận hành

Không có credentials/recipient approval nên không gửi kênh thật. Không có matched official bulletin fixture/API nên S10 được đóng bằng hành vi unavailable an toàn, không dựng dữ liệu chính thức giả. Kiểm thử viewport bằng trình duyệt và PostGIS thật cần chạy lại ở gate deployment.
