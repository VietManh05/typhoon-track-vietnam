from pathlib import Path
import json
root=Path.cwd()
p=root/"task_plan.md"
s=p.read_text(encoding="utf-8-sig")
s=s.replace("- [ ] Kiểm tra tự động ID, liên kết, coverage, DAG và trạng thái.",
            "- [x] Kiểm tra tự động ID, liên kết, coverage, DAG và trạng thái — pass; xem docs/planning/plan_validation.json.")
s=s.replace("- **Status:** in_progress","- **Status:** complete",1)
s=s.replace("Phase 2 — Kiểm chứng nền tảng và hiện trạng; task kế tiếp R01 chưa bắt đầu.",
            "Phase 2 — Kiểm chứng nền tảng và hiện trạng (pending); task kế tiếp R01 chưa bắt đầu.")
p.write_text(s,encoding="utf-8")
with (root/"progress.md").open("a",encoding="utf-8") as f:
    f.write("""
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
""")
with (root/"findings.md").open("a",encoding="utf-8") as f:
    f.write("\n## Kết quả kiểm tra kế hoạch\nCoverage 818/818, không trùng ID, dependency DAG hợp lệ, roadmap hash không đổi. Chi tiết tại docs/planning/plan_validation.json. Đây là kiểm chứng cấu trúc kế hoạch, không phải bằng chứng phần mềm đã hoạt động.\n")

