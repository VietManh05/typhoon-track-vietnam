# G27 — Tài liệu và hướng dẫn

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có tài liệu giai đoạn đầu; README lệch code.
- Đầu vào: Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu.
- Gate phụ thuộc: G26.
- Vùng file dự kiến: README.md; docs/; docs/runbook.md; docs/model-card.md.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.

<a id="gate-g27"></a>
## Gate G27

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t27-001"></a>
## T27-001 — Architecture.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1252](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1252).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: Architecture.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Architecture.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Nội dung khớp implementation đã kiểm chứng; ví dụ chạy được; link đúng; phân biệt demo/thực nghiệm/vận hành.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t27-002"></a>
## T27-002 — Data source.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1253](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1253).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** T27-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: Data source.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Data source.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t27-003"></a>
## T27-003 — Data dictionary.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1254](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1254).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** T27-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: Data dictionary.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Data dictionary.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t27-004"></a>
## T27-004 — Feature engineering.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1255](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1255).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** T27-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: Feature engineering.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Feature engineering.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t27-005"></a>
## T27-005 — Dataset.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1256](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1256).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** T27-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: Dataset.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Dataset.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t27-006"></a>
## T27-006 — Model.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1257](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1257).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** T27-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: Model.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Model.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t27-007"></a>
## T27-007 — Training.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1258](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1258).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** T27-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: Training.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Training.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t27-008"></a>
## T27-008 — Evaluation.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1259](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1259).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** T27-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: Evaluation.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Evaluation.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t27-009"></a>
## T27-009 — API.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1260](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1260).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** T27-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: API.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “API.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t27-010"></a>
## T27-010 — Database.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1261](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1261).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** T27-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: Database.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Database.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t27-011"></a>
## T27-011 — Frontend.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1262](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1262).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** T27-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: Frontend.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Frontend.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t27-012"></a>
## T27-012 — Deployment.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1263](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1263).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** T27-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: Deployment.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Deployment.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t27-013"></a>
## T27-013 — Runbook.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1264](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1264).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** T27-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: Runbook.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Runbook.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Nội dung khớp implementation đã kiểm chứng; ví dụ chạy được; link đúng; phân biệt demo/thực nghiệm/vận hành.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t27-014"></a>
## T27-014 — User guide.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1265](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1265).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** T27-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: User guide.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “User guide.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Nội dung khớp implementation đã kiểm chứng; ví dụ chạy được; link đúng; phân biệt demo/thực nghiệm/vận hành.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t27-015"></a>
## T27-015 — Disclaimer.

- **Trạng thái:** pending.
- **Nguồn:** 27. DOCUMENTATION; dòng [1266](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1266).
- **Loại:** tài liệu dựa trên kết quả đã chạy.
- **Phụ thuộc:** G26; contract/fixture của tiểu mục 27. DOCUMENTATION.
- **Task trước trong tiểu mục:** T27-014; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Bằng chứng test và interfaces thực tế của các nhóm đã nghiệm thu; yêu cầu riêng: Disclaimer.
- **File/đầu ra:** thay đổi nhỏ trong README.md; docs/; docs/runbook.md; docs/model-card.md; evidence tại evidence/T27-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Disclaimer.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G27, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Nội dung khớp implementation đã kiểm chứng; ví dụ chạy được; link đúng; phân biệt demo/thực nghiệm/vận hành.
- **Kịch bản tiểu mục:** Quickstart được chạy lại từ sạch; tài liệu theo version; demo/real và giới hạn mô hình tách rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
