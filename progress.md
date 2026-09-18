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
