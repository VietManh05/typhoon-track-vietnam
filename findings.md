# Findings — Typhoon VN

## Yêu cầu mới nhất

Lập lại bằng skill planning-with-files, chia thành từng task nhỏ chi tiết. Phạm vi dài hạn vẫn là toàn roadmap gồm API/dashboard. Phiên này chỉ lập lại kế hoạch; ảnh là ví dụ sử dụng skill, không yêu cầu cài thêm skill hay khởi động lại Codex.

## Tài liệu nguồn và cấu trúc

ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md có 1.451 dòng và 818 checkbox:
- 155 yêu cầu tổng quan.
- 635 task WBS.
- 28 tiêu chí DoD toàn dự án.

Kế hoạch giữ nguyên nội dung nguồn, thêm task cards, dependency, acceptance scenarios, traceability và 24 task bổ sung để cụ thể hóa các mục tổng quan chưa có task độc lập trong WBS. 14 task R là lát cắt ưu tiên, không phải scope cộng thêm.

## Hiện trạng có bằng chứng

- Python .venv: 3.11.9.
- Đã cài và kiểm tra metadata: torch 2.14.0, FastAPI 0.141.1, SQLAlchemy 2.0.54, Redis 5.3.1.
- Có ingestion, features, datasets, LSTM/Seq2Seq/attention/Transformer, loss, trainer và metrics/backtest.
- README vẫn mô tả giai đoạn 0–1; CLI clean-data/train còn placeholder.
- Phiên trước đã ghi api/schemas.py, api/app.py, inference/service.py, operations/store.py, operations/worker.py cùng thay đổi dependencies/settings/features init.
- Code API/inference/operations đó chưa được kiểm thử. training.pipeline được import khi load/predict model nhưng chưa tồn tại.
- Redis hiện chỉ setex, chưa có read path. SQL cache có code nhưng chưa test.
- Store dùng create_all và payload JSON; chưa thay thế migration Alembic, schema PostGIS và spatial indexes.
- Worker hiện đọc snapshot JSON; chưa có provider live/scheduler/retry pipeline đầy đủ.
- Frontend chưa triển khai. Static mount có điều kiện không phải bằng chứng có dashboard.
- Test baseline phiên trước lỗi collection do thiếu torch/FastAPI; sau install chưa chạy lại.
- Test trainer mặc định ghi vào checkpoints: cần cô lập tmp_path trước full suite.
- Dataset chọn default features trước khi tạo derived features; gap thời gian, zero-ratio split và storm qua năm cần test/sửa.
- Checkpoint được save trước history/scheduler update; chưa restore đầy đủ state.
- Repository đang có cây file untracked lớn; giữ nguyên dữ liệu/checkpoint/thư mục lạ, không reset/cleanup.

## Quyết định thiết kế của kế hoạch

Giữ src/typhoon_vn, test theo contract, dữ liệu point-in-time, scaler fit train-only, source-aware identity. React/TypeScript/Leaflet dự kiến cho dashboard. PostgreSQL/PostGIS/Alembic là nghiệm thu production; SQLite chỉ local/test. Trained model, heuristic baseline và synthetic demo phải phân biệt rõ.

Chưa xác minh thông số API nguồn/dữ liệu địa lý hiện hành qua Internet trong phiên lập kế hoạch. Mỗi task nguồn có bước xác minh primary documentation khi triển khai; không coi tri thức trong roadmap là bằng chứng nguồn hiện hành.

## Lỗi và cách xử lý

Sandbox helper khởi tạo lỗi → shell được phê duyệt. cp1252 không in được tiếng Việt → python -X utf8. Lệnh sinh file dài hơn giới hạn Windows → cấu hình JSON và generator tách file. Generator khởi tạo từ chối chạy lại nếu catalog tồn tại để bảo vệ trạng thái task.

## Tài nguyên

- task_plan.md — trạng thái điều phối.
- docs/planning/README.md — chỉ mục.
- docs/planning/next_tasks.md — R01–R14.
- docs/planning/execution_policy.md — dependency/gates/quyết định.
- docs/planning/traceability.md — mapping mỗi checkbox nguồn.
- docs/planning/history/2026-09-18-before-replan/ — bản trước khi lập lại.


## Kết quả kiểm tra kế hoạch
Coverage 818/818, không trùng ID, dependency DAG hợp lệ, roadmap hash không đổi. Chi tiết tại docs/planning/plan_validation.json. Đây là kiểm chứng cấu trúc kế hoạch, không phải bằng chứng phần mềm đã hoạt động.

## Findings triển khai R01–R09

- Repository chưa có commit nền; toàn bộ cây dự án untracked, vì vậy `git diff` rỗng không chứng minh workspace sạch.
- Pytest temp mặc định dưới `C:\Users\YOU\AppData\Local\Temp` bị PermissionError; local `--basetemp` chạy ổn định.
- Dataset cũ suy target bằng row offset nên có thể dùng +18 thay +12 khi dữ liệu gap; đã đổi sang exact timestamp lookup.
- Feature list cũ được chọn trước khi tạo derived features; đã thống nhất `FeatureBuilder` + `FEATURE_COLUMNS` cho train/serve.
- Khi mở rộng sang canonical feature vocabulary, lag đầu storm tạo NaN làm model loss/uncertainty NaN; đã pad causal bằng fix hiện tại và giữ tensor hữu hạn.
- Year split cũ chia theo row year, có thể leak storm qua năm; đã gán whole storm theo năm của fix cuối.
- Full suite hiện pass 49 tests; còn 2 deprecation warnings từ FastAPI/Starlette dependencies.
