# Task Plan: Typhoon VN — kế hoạch thực thi theo task nhỏ

## Goal

Hoàn thiện hệ thống theo ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md: dữ liệu có provenance → features không leakage → train/evaluate/registry → inference/API/PostGIS → dashboard → worker/alerts → triển khai/monitoring/tài liệu. Yêu cầu mới nhất của người dùng: lập lại kế hoạch thật chi tiết trước khi tiếp tục từng task nhỏ.

## Next Step

Phase 2 đã hoàn tất. Bước kế tiếp khi bắt đầu Phase 3 là **T07-001 — Implement persistence**; chưa chuyển task này sang `in_progress`.

## Current Phase

Phase 2 — Kiểm chứng nền tảng và dữ liệu (complete); không có task đang `in_progress`.

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
- [x] G00: nền tảng repository và môi trường đã nghiệm thu đủ T00-001–T00-045.
- [x] G01–G06: nghiệm thu nguồn dữ liệu, địa lý, cleaning và features.
- [x] S01/S03/S08: bổ sung contract dữ liệu bắt buộc của Phase 2.
- **Status:** complete — [evidence](docs/planning/evidence/PHASE-2.md)

### Phase 3: Training, đánh giá, uncertainty và registry
- [x] R10–R12: checkpoint/resume, bundle, CLI smoke.
- [ ] G07–G15 và S02/S04/S05/S06: baseline/model, loss, training, backtest, tuning, calibration, registry.
- [ ] S07: forecast môi trường tùy chọn, ghi quyết định theo dữ liệu/quyền truy cập.
- **Status:** pending

### Phase 4: Inference, API và vận hành dữ liệu
- [x] R13–R14: kiểm thử API/inference và đối chiếu gap vận hành.
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
- Sau khi R01–R14 complete, ưu tiên `execution_policy.md` và các phase chưa hoàn tất: tiếp tục từ task pending đầu tiên của G00. Dòng “G18 tiếp theo” trong evidence R14 chỉ là khuyến nghị xử lý các gap vận hành của riêng audit R14, không thay thế thứ tự toàn backlog.

## Errors Encountered

- Sandbox helper không khởi tạo được; dùng shell được phê duyệt để đọc/ghi.
- Phiên 2026-09-19: `resolve-plan-dir.ps1` không trả về đường dẫn dù không có `PLAN_ID`, `PWF_PLAN_ROOT` hay `.planning/`; đã xác nhận thủ công chế độ legacy bằng ba file planning ở project root và tiếp tục tại đó.
- Phiên 2026-09-19: `apply_patch` tích hợp lỗi sandbox helper với cả đường dẫn tuyệt đối lẫn tương đối; wrapper batch làm hỏng patch nhiều dòng, nên gọi trực tiếp chế độ apply-patch của Codex.
- Phiên 2026-09-19: patch nhiều file chốt T00-002 gặp context conflict vì WBS đã đổi từ `in_progress` sang `complete`. Chế độ apply-patch trực tiếp có thể áp dụng các file đứng trước rồi mới dừng; luôn đọc lại từng file sau lỗi, không giả định patch nhiều file là atomic.
- Phiên 2026-09-19: sau thời gian chờ, T00-003 vẫn lệch trạng thái (catalog `in_progress`, WBS `pending`), không có evidence/ref mới; tiếp quản và đồng bộ task thay vì tiếp tục chờ vô hạn.
- Phiên 2026-09-19: lệnh đọc T00-008 gọi nhầm `tests/test_commit_convention.py`; file đúng là `tests/test_commit_message.py`. Không lặp lại tên sai.
- T00-010 complete: flake8/isort/Black đều pass; full pytest pass 75 tests với 2 dependency deprecation warnings. Evidence: `docs/planning/evidence/T00-010.md`; JUnit: `docs/planning/evidence/T00-010-pytest.xml`.
- Next Step: T00-011 chỉ được bắt đầu khi người dùng cho phép rõ ràng việc tạo commit; chưa stage/commit/push.
- T00-011 complete: snapshot được kiểm chứng bằng pre-commit, 75 tests và plan validator; commit target local `codex/g00-foundation`, không đổi `main` hoặc push. Evidence: `docs/planning/evidence/T00-011.md`.
- Next Step: T00-012, kiểm chứng/tạo `data/raw` và ghi evidence.
- T00-012 complete: `data/raw` tồn tại; `.gitkeep` tracked; raw fixture bị ignore và placeholder không bị ignore. Không sửa hoặc đọc sâu dữ liệu hiện có. Evidence: `docs/planning/evidence/T00-012.md`.
- Next Step: T00-013, kiểm chứng/tạo `data/interim`.
- T00-013–T00-031 complete: data placeholders/ignore pass; roadmap directories được map vào package `src/typhoon_vn`, flat tests, `viz/frontend`, `configs` và `docs` hiện có; không tạo namespace trùng hoặc nhận frontend đồng thời.
- T00-032–T00-045 complete: Python 3.11.9 khớp pin/runtime; toàn bộ extras cần thiết cài editable; `pip check` sạch; import/version contracts của Torch, pandas/NumPy, scikit-learn, FastAPI/Uvicorn, SQLAlchemy/Alembic, pytest, MLflow, Optuna đạt; `.env.example`, config loader và Makefile được kiểm chứng.
- G00 complete: 45/45 task có evidence và trạng thái đồng bộ. Không nhận các thay đổi frontend đồng thời; lint Phase 2 tạm loại đúng `tests/test_frontend_build.py` vì ba F401 thuộc batch khác.
- Next Step: T01-001, bắt đầu G01 bằng kiểm chứng source/URL IBTrACS và provenance contract.
- Phase 2 complete: G00–G06 đạt 256/256 task complete; S01/S03/S08 complete. Data gate 41 passed; full regression 105 passed; plan validator/lint/DVC status pass. Evidence: `docs/planning/evidence/PHASE-2.md`.
- Không bắt đầu Phase 3 và không tạo commit/push mới. Next Step khi tiếp tục: T07-001 — Implement persistence.
- Baseline pytest phiên trước lỗi collection do thiếu torch/FastAPI. Đã cài dependency; chưa rerun suite.
- Lệnh đọc WBS gặp UnicodeEncodeError cp1252; chuyển python -X utf8.
- Lệnh sinh kế hoạch quá dài trên Windows (os error 206); tách cấu hình và generator thành file nhỏ.
- Lần soạn tool script có SyntaxError do ký tự Markdown trong JS template; sửa script, chưa ghi file trong lần lỗi đó.

## Điều kiện bên ngoài chưa xác minh

Nguồn/quyền dữ liệu thật, historical forecast comparisons, ERA5 credentials, ranh giới có phiên bản, Git remote, Docker runtime, GPU budget, hosting và alert recipients/channels. Các phần này có task riêng; không suy ra hoàn tất chỉ từ cấu hình hoặc fixture.
