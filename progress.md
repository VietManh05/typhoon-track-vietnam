# Progress log

## 2026-09-18
- Read planning-with-files skill and templates, resolved plan directory, inspected roadmap and major interfaces.
- Confirmed full-roadmap scope with user.
- Created task_plan.md, findings.md and progress.md before implementation.
- Baseline tests pending. No implementation code modified yet.
- Error: sandbox helper initialization failed; escalated read succeeded.

- Baseline pytest failed collection: torch and FastAPI missing; dependency install running. apply_patch update failed because sandbox helper cannot initialize; use approved shell writes.

## 2026-09-18 — Lập lại kế hoạch theo yêu cầu mới
- Phạm vi phiên: chỉ lập kế hoạch chi tiết; không sửa thêm code sản phẩm.
- Đính chính nhật ký cũ: phiên triển khai trước đã thêm API/schema/inference/store/worker và sửa dependencies/settings/features init. Các thay đổi đó chưa được kiểm thử; nhánh trained-model thiếu training.pipeline.
- Dependency install trước đó đã hoàn tất; phiên này chỉ kiểm tra metadata phiên bản, không rerun pytest.
- Giữ bản planning cũ tại docs/planning/history/2026-09-18-before-replan/.
- Tạo 635 task WBS, 24 task bổ sung, 28 tiêu chí nghiệm thu và 14 task ưu tiên R01–R14 (lát cắt, không cộng trùng scope).
- Mỗi card có nguồn, ID, trạng thái, gate/task phụ thuộc, input, file/output, bước làm, kiểm thử và DoD.
- Đã ghi 61 kịch bản kiểm thử theo tiểu mục, chính sách leakage/calibration/registry, ngoại vi và thứ tự thực thi.
- Cập nhật task_plan.md/findings.md; giữ roadmap gốc nguyên trạng.
- Chưa tạo evidence giả cho task chưa thực hiện.

### Kiểm chứng kế hoạch
- Lệnh: .venv/Scripts/python.exe -X utf8 docs/planning/tools/validate_plan.py
- Kết quả: PASS, exit code 0.
- Mapping nguồn: 818/818 checkbox; 155 yêu cầu tổng quan.
- Kiểm tra 731 nodes dependency không vòng; ID không trùng; 2.710 links hợp lệ trong lần kiểm tra.
- Source SHA-256 không đổi.
- Báo cáo: docs/planning/plan_validation.json.
- Không chạy product tests hoặc training trong phiên lập kế hoạch.

### Lỗi đã xử lý
- Sandbox helper startup thất bại: chuyển shell được phê duyệt.
- UnicodeEncodeError cp1252 ở stdout: dùng python -X utf8.
- SyntaxError khi soạn tool script: sửa cách đóng chuỗi trước khi ghi file.
- Windows os error 206, command quá dài: tách generator và config JSON.
- Rà soát task mẫu phát hiện keyword wind khớp nhầm window: đổi sang word-boundary, bổ sung kiểm thử riêng cho window và kiểm tra lại.

### Trạng thái kết thúc phiên
- Phase 1 lập lại kế hoạch: complete.
- Phase 2 và các implementation tasks: pending.
- Next Step: R01, kiểm kê trạng thái làm việc; sau đó R02 môi trường và R03 cô lập checkpoint trước baseline pytest.

## 2026-09-18 — Triển khai R01–R09
- R01–R02 complete: xác nhận repository chưa có HEAD/toàn bộ untracked; Python 3.11.9, pip check và import smoke pass.
- R03 complete: test trainer ghi checkpoint vào `tmp_path`; hash `checkpoints/best.pt` và `last.pt` không đổi. Dùng `--basetemp` local do temp mặc định bị từ chối quyền.
- R04 complete: baseline 39 passed, 2 dependency deprecation warnings.
- R05 complete: chốt observation/time/provenance contract xuyên ingestion, feature bridge và API; từ chối naive datetime, non-finite values và wind unit lạ.
- R06–R08 complete: target lookup theo timestamp thật; gap/duplicate được xử lý; split giữ nguyên whole storm; feature builder/order dùng chung train-serving.
- R09 complete: scaler train-only, lưu fill/order/statistics, reject missing/extra/reordered và round-trip <=1e-6.
- Full suite sau thay đổi: 49 passed, 2 warnings in 10.45s; JUnit `docs/planning/evidence/phase2-pytest.xml`.
- Next Step: R10 checkpoint/resume deterministic.

## 2026-09-19 — Tiếp tục theo planning
- Đã đọc lại toàn bộ `task_plan.md`, `progress.md`, `findings.md`; xác nhận bước kế tiếp là R10 checkpoint/resume deterministic.
- `PLAN_ID` và `PWF_PLAN_ROOT` đều không được đặt, không có `.planning/`; `resolve-plan-dir.ps1` trả rỗng nên dùng planning legacy ở project root theo trạng thái thực tế.
- Giữ nguyên thay đổi có sẵn của người dùng: `bao_cao_du_an_typhoon_vn.docx` đang bị xóa/0 byte và hai báo cáo TXT đang untracked; không sửa hoặc dọn các file này.
- `apply_patch` tích hợp lỗi sandbox helper; wrapper batch không truyền đúng patch nhiều dòng, sau đó chuyển sang gọi trực tiếp chế độ apply-patch của Codex.
- Bắt đầu R10; chưa sửa code sản phẩm trong phiên này tại thời điểm ghi log.
- Đã đọc task card, trainer và tests: triển khai R10 đã tồn tại nhưng chưa được planning/evidence xác nhận; chuyển R10 và Phase 2 sang `in_progress`.
- Test R10: `.venv\\Scripts\\python.exe -m pytest tests\\test_training_resume.py -q --basetemp=.pytest-r10-20260919` → 3 passed in 4.92s.
- Full suite + JUnit: `.venv\\Scripts\\python.exe -m pytest -q --basetemp=.pytest-r10-full-20260919 --junitxml=docs\\planning\\evidence\\R10-pytest.xml` → 61 passed, 2 dependency warnings in 12.91s.
- Phát hiện thay đổi đồng thời không thuộc lượt hiện tại: R11–R14/evidence/tests/CLI/task catalog đang được cập nhật. Giữ nguyên, không ghi đè và không nhận là kết quả của lượt này; cần đối chiếu trước khi chọn Next Step.
- Đối chiếu `R10-checkpoint-resume.md` và JUnit R10–R14: kết quả đồng nhất với lần chạy độc lập; chuyển R10 sang `complete` và gắn evidence.
- R01–R14 hiện complete. Giải quyết mâu thuẫn thứ tự bằng `execution_policy.md`: bước kế tiếp là chọn task pending đầu tiên của G00, không nhảy thẳng qua các gate dữ liệu/model còn mở tới G18.
- Chọn T00-001 là task pending đầu tiên của G00 và chuyển sang `in_progress`. Git root/nhánh/HEAD/remote đã được kiểm chứng read-only; chưa tạo branch, remote hay push.
- T00-001 complete: evidence `docs/planning/evidence/T00-001.md`; Git worktree non-bare, `main`, HEAD và origin đều hợp lệ. Giữ remote thực tế `typhoon-track-vietnam`, không đổi tên/push.
- Next Step: T00-002, kiểm chứng/tạo local `develop` mà không checkout hoặc push.
- T00-002 chuyển `in_progress`: `main` hiện có và tracking `origin/main`; `develop` chưa có ở local/remote. Chuẩn bị tạo local ref từ HEAD, không đổi working tree.
- `git branch develop HEAD` exit 0; current branch vẫn `main`, local `main`/`develop` cùng trỏ base HEAD.
- Patch nhiều file chốt T00-002 gặp context conflict; đọc lại cho thấy apply-patch trực tiếp có thể đã áp dụng các file đứng trước khi dừng. Đã xác nhận `evidence/T00-002.md`, WBS/catalog complete và sửa nhật ký, không giả định tính atomic.
- Catalog hiện đánh T00-003 `in_progress` bởi tiến trình đồng thời. Tạm không sửa T00-003 để duy trì một task active và tránh mất cập nhật.
- Sau lần chờ, T00-003 không có evidence/ref mới và WBS/catalog lệch nhau; đã tiếp quản và đồng bộ WBS `in_progress`.
- T00-003 complete: `git branch codex/g00-foundation develop` exit 0; kiểm chứng ref pass, current branch vẫn `main`, không push. Evidence: `docs/planning/evidence/T00-003.md`.
- Next Step: T00-004, kiểm chứng và hoàn thiện `.gitignore`.
- T00-004 audit: representative positive controls đều được `git check-ignore --no-index -v` match; `.env.example` được rule phủ định giữ lại. Phát hiện checkpoint `.pth` legacy đang tracked dù pattern ignore đã đúng.
- Catalog đồng thời đã chuyển T00-004 sang `complete`; tạm chưa sửa task/evidence cho đến khi đọc bản hiện có.
- Đối chiếu evidence và đồng bộ WBS: T00-004, T00-005, T00-006 complete. README contracts pass 2 tests; LICENSE metadata contract pass 1 test.
- Next Step: T00-007, audit/hoàn thiện CONTRIBUTING theo branch và command contracts hiện tại.
- T00-007 complete theo evidence: CONTRIBUTING/documentation contracts pass 3 tests; WBS đã đồng bộ.
- Catalog cho thấy T00-008 complete và T00-009 in_progress; chưa sửa hai task này trước khi đọc evidence để tránh xung đột.
- T00-008 complete theo evidence; WBS đã đồng bộ.
- T00-009 chuyển `in_progress`; sẽ kiểm chứng commit-message + pre-commit config trong isolated repository. Lần đọc đầu dùng nhầm tên `test_commit_convention.py`; tên đúng là `test_commit_message.py`.
- T00-009 complete: 11 tests pass trong 24.88s; evidence `docs/planning/evidence/T00-009.md`. Không cài hoặc sửa Git hooks của dirty worktree.
- T00-010 complete. Lint cuối: flake8 pass, isort check pass, Black pass 74 files. Full regression pass 75 tests; 2 dependency deprecation warnings; JUnit `docs/planning/evidence/T00-010-pytest.xml`.
- Next Step: T00-011 — commit cấu trúc ban đầu, nhưng chỉ sau khi người dùng cho phép rõ ràng; chưa stage/commit/push.
- T00-011 `in_progress`: người dùng đã cho phép tiếp tục. `HEAD` bị host khóa ở `main`, nên chuẩn bị snapshot bằng index tạm và chỉ cập nhật ref `codex/g00-foundation`; không thay đổi `main` hoặc remote.
- T00-011 complete: pre-commit pass; full regression 75 passed; plan validator pass; Conventional Commit message pass. Snapshot loại artefact người dùng/tạm và chỉ cập nhật ref local `codex/g00-foundation`; không push.
- Next Step: T00-012 — kiểm chứng/tạo `data/raw`.
- T00-012 complete: directory tồn tại; `.gitkeep` tracked; `data/raw/*` ignore payload và allowlist placeholder hoạt động; không phát sinh thay đổi dưới `data/raw`.
- Next Step: T00-013 — kiểm chứng/tạo `data/interim`.
- T00-013–T00-031 complete: ba data directories còn lại có tracked placeholders và ignore đúng; các namespace source/test/API/frontend/config/docs được map vào layout hiện tại và import smoke pass.
- Next Step: T00-032 — khóa Python version.
- T00-032–T00-045 complete: khóa Python 3.11.9; bổ sung Alembic và Optuna vào extras; Makefile setup cài đủ api/train/ingestion/dev/experiment; editable install và `pip check` pass.
- Environment contract suite pass 6 tests; flake8/isort/Black pass trên phạm vi Phase 2. `tests/test_frontend_build.py` bị loại khỏi lint batch vì là thay đổi frontend đồng thời ngoài G00.
- Đã tạo evidence T00-032–T00-045 và đồng bộ catalog/WBS. G00 đạt 45/45 complete.
- Next Step: T01-001 — xác định và kiểm chứng URL/source IBTrACS.

## 2026-09-19 — Hoàn tất Phase 2

- G01 complete (83/83): downloader/parser/provenance/merge/validation/quality; nguồn chính thức được đối chiếu, test dùng fixture và không mirror dữ liệu thật.
- G02 complete (19/19): WGS84, coastline distance, polygon/spatial index, province/location contracts; licence GADM/GSHHG được giữ thành operator gate.
- G03 complete (20/20): raw→clean→feature→atomic Parquet cùng cleaning/quality report.
- G04 complete (54/54): canonical feature builder, point-in-time SST/atmosphere, data dictionary/version/fingerprint.
- G05 complete (9/9): train-only scaler, save/load/inverse, schema/order/leakage checks.
- G06 complete (26/26): configurable windows, exact horizons, whole-storm split và split manifest.
- S01/S03/S08 complete: DVC fixture pipeline; strict versioned feature store; effective-date impact/province labels giữ duplicate/conflict provenance.
- Targeted Phase-2 data suite: 41 passed. Full regression: 105 passed, 2 dependency deprecation warnings.
- Plan validator pass: 818/818 checkbox, 731 nodes, 2.977 links, roadmap unchanged. Flake8/isort/Black pass trên phạm vi Phase 2.
- Phase 2 đóng với 256/256 task G00–G06 complete; không commit/push mới. Phase 3 chưa bắt đầu.
