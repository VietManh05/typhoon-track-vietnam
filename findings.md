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

## Findings R10 — Checkpoint/resume

- Workspace đã có triển khai R10 trong `src/typhoon_vn/training/trainer.py` và contract tests trong `tests/test_training_resume.py`, nhưng task card vẫn là pending và chưa có evidence.
- Checkpoint version 2 hiện lưu model, optimizer, scheduler kind/state, best loss/epoch, patience counter, history và RNG Python/NumPy/Torch/CUDA; ghi atomically qua file `.tmp` rồi `os.replace`.
- `fit()` cập nhật scheduler, history, learning rate và early-stop state trước khi ghi `best.pt`/`last.pt`; validation rỗng hoặc non-finite bị từ chối trước khi tạo best checkpoint giả.
- Contract test dự kiến so 2 epoch liên tục với 1 epoch + resume, kiểm tra history/LR/early-stop/weights và scheduler mismatch. Cần chạy test để xác nhận hành vi thật trước khi đánh dấu complete.
- Kiểm chứng 2026-09-19: test riêng R10 pass 3/3; full suite pass 61/61, còn 2 deprecation warnings từ dependency. JUnit mới: `docs/planning/evidence/R10-pytest.xml`, SHA-256 `03420916B24C5D963BD03C663F4175D06E6DACAAD20D285168563A66735CA035`.
- Trong khi kiểm chứng R10, workspace xuất hiện thay đổi đồng thời ngoài phạm vi lượt này: R11–R14 được đánh dấu complete, thêm evidence/test và sửa CLI/task catalog. Phải bảo toàn và đối chiếu các thay đổi đó, không nhận là kết quả của lượt R10 này.
- Evidence R10 do tiến trình đồng thời tạo ra khớp với kiểm chứng độc lập: 61 tests, checkpoint contract version 2 và weights resume khớp `atol=1e-7, rtol=0`. R10 đủ điều kiện complete.
- Evidence R14 đề xuất G18 tiếp theo cho riêng các gap vận hành, nhưng `execution_policy.md` và các phase còn mở yêu cầu sau R01–R14 tiếp tục chuỗi toàn backlog từ G00. Chọn chính sách điều phối cấp cao làm nguồn thứ tự.

## Findings T00-001 — Repository

- Project root `D:/IT-Dev/python-projects/Typhoon_vn` là Git worktree hợp lệ, nhánh hiện tại `main`, HEAD `b5223d4db796008d4dc90e16641cbdf91e95222b`.
- Remote `origin` đã cấu hình tới `https://github.com/VietManh05/typhoon-track-vietnam.git`, khác tên `typhoon-vn-forecast-system` trong roadmap.
- Theo chính sách bảo toàn dự án và không tự tạo remote/push, T00-001 được xử lý như kiểm chứng repository hiện hữu; không đổi identity/remote nếu người dùng chưa yêu cầu.

## Findings T00-002 — Branch nền

- Trước thay đổi, local chỉ có `main` tại `b5223d4db796008d4dc90e16641cbdf91e95222b`, theo dõi `origin/main`; remote refs cũng chỉ có `origin/main`.
- `develop` chưa tồn tại. Phạm vi an toàn là tạo local ref `develop` từ HEAD, không checkout và không push.
- Đã tạo `develop` từ HEAD thành công; current branch vẫn là `main`, cả hai refs cùng trỏ `b5223d4db796008d4dc90e16641cbdf91e95222b`, `develop` chưa có upstream.

## Findings T00-003 — Feature branch

- Catalog từng chuyển T00-003 sang `in_progress` trong lúc WBS còn `pending`; sau thời gian chờ không có evidence/ref mới. Đã đồng bộ WBS và tiếp quản task.
- Đã tạo local `codex/g00-foundation` từ `develop`; `main`, `develop` và feature ref cùng base commit. Không checkout, upstream hoặc push.

## Findings T00-004 — .gitignore

- Rule hiện tại đã ignore đúng `.env`, `.env.*`, `data/raw/*`, `data/processed/*`, `checkpoints/*.pt|*.pth|*.ckpt`, `.venv/`, `__pycache__/` và `.pytest-*/`; `.env.example` được unignore có chủ đích.
- `git ls-files` phát hiện checkpoint legacy `checkpoints/best_model_epoch53_loss0.0185.pth` đã nằm trong index/HEAD. Ignore rule không tác động file đã track; phải giữ file vật lý và xử lý untrack riêng nếu task cho phép, không xóa dữ liệu.
- Catalog đã hiển thị T00-004 `complete` trong lúc kiểm chứng; cần đọc WBS/evidence trước khi cập nhật tiếp để tránh ghi đè tiến trình đồng thời.
- Evidence T00-004 xác nhận các allowlist/negative controls pass và `.gitignore` không cần patch. Ngoại lệ checkpoint legacy đang tracked vẫn được giữ nguyên trên đĩa và theo dõi như gap index riêng.

## Findings T00-005–T00-006

- README đã được tiến trình đồng thời cập nhật theo implementation hiện tại và có `tests/test_readme.py`; CLI help + README/health contracts pass 2 tests.
- LICENSE là MIT đầy đủ; `pyproject.toml` và editable distribution metadata cùng khai báo LICENSE; `tests/test_package_metadata.py` pass.

## Findings T00-007 — CONTRIBUTING

- CONTRIBUTING đã mô tả Python 3.11, extras thực tế, pytest/pre-commit, provenance/safety checklist, remote thật và quy tắc không reset/push dirty worktree; `tests/test_contributing.py` cùng README/package contracts pass 3 tests.
- Project docs dùng convention `feature/<task-id>-<slug>`; local ref T00-003 đã tạo là `codex/g00-foundation` theo prefix workspace. Giữ nguyên refs, không tự xóa/đổi; ghi khác biệt để xử lý khi branch thực sự được dùng.
- Catalog hiện T00-008 `complete`, T00-009 `in_progress`; cần đọc evidence trước khi đồng bộ WBS và tiếp tục đúng task active.

## Findings T00-008–T00-009

- Conventional Commit validator đã có trong `scripts/validate_commit_msg.py`, đăng ký local `commit-msg` hook và được evidence xác nhận 10 cases + CLI exit behavior pass.
- T00-009 dùng `tests/test_precommit_config.py` để copy config/validator vào Git repo dưới `tmp_path`; chạy riêng local hook với message valid/invalid, tránh cài/chạm hook của dirty worktree thật.
- Kiểm chứng T00-009 pass 11 tests trong 24.88s; pre-commit config và commit-message execution đều đạt, không cài hook vào repository thật.

## Findings T00-010 — Lint

- Lần chạy đầu: `flake8 src tests` exit 1; `isort --check-only src tests` exit 0; `black --check src tests` exit 0 (74 files unchanged).
- Flake8 báo 33 lỗi: unused imports, các dòng E501 và hai F821 thật tại `typhoon_dataset.py` do dùng `haversine_km`/`bearing_deg` nhưng chưa import.
- Sau sửa có mục tiêu, lần tiếp quản còn 16 F401; đã bỏ đúng import thừa trong 10 tệp và isort lại 8 tệp bị thay đổi nhóm import.
- Kết quả cuối: flake8/isort/Black đều exit 0; Black giữ nguyên 74 files. Full pytest pass 75 tests với 2 dependency deprecation warnings.
- Lần pytest dùng temp mặc định gặp 13 setup errors do quyền truy cập `pytest-of-YOU`; chạy lại bằng basetemp trong workspace pass toàn bộ. Đây là lỗi môi trường, không phải regression sản phẩm.

## Findings T00-011 — Commit cấu trúc ban đầu

- `HEAD` bị host khóa tại `main`; cả `git switch` và `git symbolic-ref` đều không cập nhật được HEAD, trong khi `git update-ref` cho ref G00 hoạt động.
- Pre-commit `--all-files` lần đầu tự format 30 tệp legacy ngoài manifest. Sau khi người dùng cho phép, đã hoàn nguyên chính xác các thay đổi hook đó và chạy lại hook chỉ trên staged snapshot; tất cả hook pass.
- Roadmap được khôi phục LF để SHA-256 tiếp tục khớp catalog; plan validator pass với 818/818 checkbox và source unchanged.
- `.grapuco/`, báo cáo `.txt`, file `.docx` đang bị xóa, temp artefacts và frontend xuất hiện đồng thời đều bị loại khỏi snapshot. Không push hoặc sửa remote.

## Findings T00-012 — `data/raw`

- `data/raw` và `.gitkeep` đã tồn tại; placeholder được Git track và được rule phủ định giữ khỏi ignore.
- Một raw fixture giả định match `data/raw/*`; `git status` không thấy payload nào dưới namespace này.
- Các namespace con hiện có được coi là workspace/dữ liệu cục bộ, giữ nguyên và không đọc sâu; task chỉ chốt contract thư mục, không tải hoặc sinh dữ liệu.

## Findings T00-013–T00-031 — Cấu trúc repository

- `data/interim`, `data/processed`, `data/external` đều có tracked `.gitkeep`; payload giả định bị ignore và placeholder không bị ignore.
- Giữ namespace đóng gói `src/typhoon_vn`; ingestion/features/datasets/models/training/inference/evaluation/API import pass. Preprocessing map vào features cleaning/schema/store; alerts map vào operations store/worker.
- Giữ test layout phẳng và map unit/integration/model theo file hiện có; không tạo cây test trùng.
- `viz/frontend`, `configs`, `docs` tồn tại. Các file frontend/dashboard xuất hiện đồng thời không được nhận hoặc sửa trong batch này.

## Findings T00-032–T00-045 — Environment

- `.python-version`, `requires-python` và runtime `.venv` cùng khóa Python 3.11.9.
- `pyproject.toml` đã bổ sung Alembic cho API extra và Optuna cho experiment extra; Makefile setup cài đủ `api,train,ingestion,dev,experiment`.
- Editable install hoàn tất; `pip check` không phát hiện dependency hỏng. Các dependency chính được kiểm chứng bằng import/version: Torch 2.14.0+cpu, pandas 2.3.3, NumPy 2.4.6, scikit-learn 1.9.1, FastAPI 0.141.1, Uvicorn 0.53.0, SQLAlchemy 2.0.54, Alembic 1.20.0, pytest 8.4.2, MLflow 3.16.1, Optuna 4.9.0 và DVC 3.67.1.
- Environment contract suite pass 6 tests; `.env.example`, settings override và Makefile extras có test hồi quy.
- `tests/test_frontend_build.py` xuất hiện từ tiến trình frontend đồng thời và có ba F401 không thuộc G00. Batch lint Phase 2 loại đúng file này, giữ nguyên nội dung và không nhận thay đổi frontend.

## Findings Phase 2 — Data gate hoàn tất

- Downloader hiện reject body rỗng, retry hữu hạn timeout/429/5xx, fail-fast 4xx khác, ghi checksum và không để partial file. Parser/merge giữ raw provenance, source units và conflicts.
- Geospatial contract dùng WGS84 rõ ràng, bbox index + exact polygon filter và khoảng cách geodesic; dữ liệu GADM/GSHHG thật không được commit/tái phân phối tự động.
- Cleaning pipeline nội suy chỉ trong storm, không dùng 0 cho unknown, giữ flags/counters; output Parquet và quality report ghi atomic.
- Environmental features chọn field mới nhất đã available tại issue time; final reanalysis xuất bản sau issue time bị từ chối để tránh leakage.
- Feature schema có fixed order, dtype/unit/source/missing policy, version và fingerprint; feature store reject missing/extra/reorder/dtype/fingerprint drift.
- Dataset targets theo timestamp chính xác cho 6/12/24/48/72h, whole-storm splits và manifest IDs; scaler chỉ fit train.
- DVC stage dùng synthetic fixture hợp pháp, lock có dependency/output hashes, lần repro thứ hai no-op; remote chỉ cấu hình local qua `DVC_REMOTE_URL`, chưa push.
- Full suite cuối pass 105 tests. Hai file test frontend/refactor xuất hiện đồng thời được giữ nguyên và chỉ loại khỏi lint phạm vi; full pytest vẫn collect chúng.
