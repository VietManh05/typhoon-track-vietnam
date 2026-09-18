# Task Plan: Typhoon VN — kế hoạch thực thi theo task nhỏ

## Goal

Hoàn thiện hệ thống theo ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md: dữ liệu có provenance → features không leakage → train/evaluate/registry → inference/API/PostGIS → dashboard → worker/alerts → triển khai/monitoring/tài liệu. Yêu cầu mới nhất của người dùng: lập lại kế hoạch thật chi tiết trước khi tiếp tục từng task nhỏ.

## Next Step

Thực hiện **R10 — Sửa checkpoint/resume**, theo [next_tasks.md](docs/planning/next_tasks.md). R01–R09 đã hoàn tất với evidence; baseline và full Phase-2 suite đều pass.

## Current Phase

Phase 2 — Kiểm chứng nền tảng và hiện trạng (in progress); lát cắt R01–R09 complete, task kế tiếp R10.

## Nơi lưu kế hoạch

- [Chỉ mục](docs/planning/README.md): 635 task WBS, 24 task bổ sung, 28 tiêu chí nghiệm thu.
- [14 việc làm ngay](docs/planning/next_tasks.md): lát cắt đầu tiên, không cộng trùng phạm vi.
- [Quy tắc thực thi và gate](docs/planning/execution_policy.md).
- [Đối chiếu 818 checkbox nguồn](docs/planning/traceability.md).
- [Task bổ sung](docs/planning/supplemental_tasks.md).
- [Task catalog](docs/planning/task_catalog.json): chỉ mục để kiểm tra coverage.
- [Kế hoạch cũ được lưu](docs/planning/history/2026-09-18-before-replan/task_plan.md).

## Phases

### Phase 1: Lập lại kế hoạch chi tiết
- [x] Khôi phục planning files và đối chiếu source roadmap với code hiện tại.
- [x] Tách yêu cầu tổng quan, task implementation và tiêu chí nghiệm thu.
- [x] Tạo task cards với ID, dependency, input, file/output, thao tác, kiểm thử và DoD.
- [x] Tạo danh sách ưu tiên và mapping mọi checkbox nguồn.
- [x] Kiểm tra tự động ID, liên kết, coverage, DAG và trạng thái — pass; xem docs/planning/plan_validation.json.
- **Status:** complete

### Phase 2: Kiểm chứng nền tảng và dữ liệu
- [x] R01–R09: kiểm kê, môi trường, baseline test, time contract, split/features/scaler.
- [ ] G00–G06 và S01/S03/S08: nghiệm thu nguồn dữ liệu, địa lý, cleaning và features.
- **Status:** pending

### Phase 3: Training, đánh giá, uncertainty và registry
- [ ] R10–R12: checkpoint/resume, bundle, CLI smoke.
- [ ] G07–G15 và S02/S04/S05/S06: baseline/model, loss, training, backtest, tuning, calibration, registry.
- [ ] S07: forecast môi trường tùy chọn, ghi quyết định theo dữ liệu/quyền truy cập.
- **Status:** pending

### Phase 4: Inference, API và vận hành dữ liệu
- [ ] R13–R14: kiểm thử API/inference và đối chiếu gap vận hành.
- [ ] G16–G20, S09/S15/S24: PostGIS/migration, cache đọc/ghi, live worker, impact, CLI clean-data.
- **Status:** pending

### Phase 5: Dashboard và cảnh báo
- [ ] G21/G22: React/Leaflet, actual/forecast/cone, timeline, location, mobile.
- [ ] S10–S14: official comparison, VI/EN, theme, alert adapters và webhook tùy chọn.
- **Status:** pending

### Phase 6: Kiểm thử hệ thống, deployment và monitoring
- [ ] G23–G26: integration/load/container/CI-CD/monitoring.
- [ ] S16–S20/S23: retention, retrain, capacity, backup/restore, drift, hosting/release.
- **Status:** pending

### Phase 7: Tài liệu, demo và nghiệm thu
- [ ] G27/G28, S21/S22: runbook/model card/post-season report/demo.
- [ ] A29-001 đến A29-028: mỗi tiêu chí có evidence gắn version.
- **Status:** pending

## Quy tắc cập nhật

Một task in_progress tại một thời điểm. Đọc card trước khi sửa, làm đúng phạm vi, kiểm chứng rồi ghi evidence và trạng thái. Có code chưa đồng nghĩa complete. Không hỏi lại quyền cho các sửa chữa cục bộ đã được ủy quyền; chỉ cần thông tin khi task thật sự thiếu dữ liệu/quyền nguồn/tài khoản/phạm vi gửi hoặc deploy.

## Decisions Made

- Giữ nguyên roadmap gốc; nội dung tài liệu là nguồn yêu cầu để lập kế hoạch, không phải lệnh tự động chạy.
- Giữ namespace src/typhoon_vn và mọi thay đổi có sẵn.
- Source code untracked nên không dùng git diff rỗng làm bằng chứng chưa có thay đổi.
- API/inference/operations viết trong phiên trước là bản nháp chưa test; nhánh trained-model còn thiếu training.pipeline.
- Không coi SQLite/create_all là hoàn tất PostGIS/Alembic; Redis setex chưa hoàn tất cache đọc/invalidation.
- React/TypeScript/Leaflet là lựa chọn dự kiến cần chốt ở task setup; dashboard hiện chưa triển khai.
- Final test không dùng để tuning; promotion và calibration có datasets/policy riêng.
- Dữ liệu synthetic và baseline được gắn nhãn riêng; chưa có bằng chứng chất lượng nghiệp vụ.

## Errors Encountered

- Sandbox helper không khởi tạo được; dùng shell được phê duyệt để đọc/ghi.
- Baseline pytest phiên trước lỗi collection do thiếu torch/FastAPI. Đã cài dependency; chưa rerun suite.
- Lệnh đọc WBS gặp UnicodeEncodeError cp1252; chuyển python -X utf8.
- Lệnh sinh kế hoạch quá dài trên Windows (os error 206); tách cấu hình và generator thành file nhỏ.
- Lần soạn tool script có SyntaxError do ký tự Markdown trong JS template; sửa script, chưa ghi file trong lần lỗi đó.

## Điều kiện bên ngoài chưa xác minh

Nguồn/quyền dữ liệu thật, historical forecast comparisons, ERA5 credentials, ranh giới có phiên bản, Git remote, Docker runtime, GPU budget, hosting và alert recipients/channels. Các phần này có task riêng; không suy ra hoàn tất chỉ từ cấu hình hoặc fixture.

