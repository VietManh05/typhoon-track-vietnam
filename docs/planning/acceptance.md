# G29 — Definition of Done toàn dự án

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Tất cả tiêu chí chưa được nghiệm thu.
- Đầu vào: Kết quả từng nhóm và evidence gắn với version.
- Gate phụ thuộc: G28.
- Vùng file dự kiến: docs/planning/acceptance.md; docs/acceptance/.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.

<a id="gate-g29"></a>
## Gate G29

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="a29-001"></a>
## A29-001 — Có dữ liệu lịch sử có provenance.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1313](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1313).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có dữ liệu lịch sử có provenance.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có dữ liệu lịch sử có provenance.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-002"></a>
## A29-002 — Có pipeline ingestion tự động.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1314](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1314).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có pipeline ingestion tự động.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có pipeline ingestion tự động.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-003"></a>
## A29-003 — Có validation và cleaning.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1315](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1315).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có validation và cleaning.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có validation và cleaning.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-004"></a>
## A29-004 — Có feature engineering.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1316](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1316).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có feature engineering.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có feature engineering.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-005"></a>
## A29-005 — Không có data leakage.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1317](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1317).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Không có data leakage.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Không có data leakage.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Storm không giao train/val/test kể cả qua năm; ratio=0 đúng nghĩa; split IDs/seed được lưu.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-006"></a>
## A29-006 — Có train/validation/test độc lập.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1318](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1318).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có train/validation/test độc lập.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có train/validation/test độc lập.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-007"></a>
## A29-007 — Có baseline.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1319](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1319).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có baseline.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có baseline.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-008"></a>
## A29-008 — Có ít nhất một model ML hoạt động.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1320](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1320).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có ít nhất một model ML hoạt động.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có ít nhất một model ML hoạt động.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-009"></a>
## A29-009 — Có multi-horizon forecast.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1321](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1321).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có multi-horizon forecast.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có multi-horizon forecast.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-010"></a>
## A29-010 — Có metric theo km.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1322](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1322).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có metric theo km.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có metric theo km.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-011"></a>
## A29-011 — Có backtest.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1323](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1323).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có backtest.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có backtest.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-012"></a>
## A29-012 — Có uncertainty/cone.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1324](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1324).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có uncertainty/cone.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có uncertainty/cone.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** GeoJSON [lon,lat], ring đóng/topology hợp lệ; dateline có xử lý; coverage thực nghiệm khác radius minh họa.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-013"></a>
## A29-013 — Có model version.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1325](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1325).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có model version.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có model version.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-014"></a>
## A29-014 — Có inference service.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1326](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1326).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có inference service.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có inference service.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-015"></a>
## A29-015 — Có FastAPI.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1327](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1327).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-014; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có FastAPI.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có FastAPI.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-016"></a>
## A29-016 — Có PostgreSQL/PostGIS.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1328](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1328).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có PostgreSQL/PostGIS.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có PostgreSQL/PostGIS.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-017"></a>
## A29-017 — Có dashboard bản đồ.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1329](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1329).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có dashboard bản đồ.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có dashboard bản đồ.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-018"></a>
## A29-018 — Có actual + forecast track.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1330](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1330).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có actual + forecast track.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có actual + forecast track.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-019"></a>
## A29-019 — Có vùng ảnh hưởng.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1331](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1331).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có vùng ảnh hưởng.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có vùng ảnh hưởng.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-020"></a>
## A29-020 — Có cảnh báo nếu triển khai.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1332](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1332).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-019; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có cảnh báo nếu triển khai.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-020.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có cảnh báo nếu triển khai.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-021"></a>
## A29-021 — Có unit/integration/model tests.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1333](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1333).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-020; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có unit/integration/model tests.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-021.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có unit/integration/model tests.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-022"></a>
## A29-022 — Có Docker.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1334](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1334).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-021; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có Docker.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-022.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có Docker.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Build/config exit 0; smoke service; secrets/raw/checkpoints ngoài build context trừ artifact được chọn.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-023"></a>
## A29-023 — Có CI/CD cơ bản.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1335](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1335).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-022; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có CI/CD cơ bản.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-023.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có CI/CD cơ bản.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-024"></a>
## A29-024 — Có logging/monitoring cơ bản.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1336](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1336).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-023; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có logging/monitoring cơ bản.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-024.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có logging/monitoring cơ bản.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-025"></a>
## A29-025 — Có tài liệu cài đặt.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1337](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1337).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-024; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có tài liệu cài đặt.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-025.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có tài liệu cài đặt.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-026"></a>
## A29-026 — Có tài liệu kiến trúc.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1338](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1338).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-025; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có tài liệu kiến trúc.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-026.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có tài liệu kiến trúc.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-027"></a>
## A29-027 — Có báo cáo đánh giá.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1339](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1339).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-026; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có báo cáo đánh giá.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-027.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có báo cáo đánh giá.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Có task implementation đã complete và evidence; không đóng chỉ vì file hoặc mô tả tồn tại.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="a29-028"></a>
## A29-028 — Có disclaimer rõ ràng.

- **Trạng thái:** pending.
- **Nguồn:** 29. DEFINITION OF DONE TOÀN PROJECT; dòng [1340](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1340).
- **Loại:** nghiệm thu, không viết code trùng.
- **Phụ thuộc:** G28; contract/fixture của tiểu mục 29. DEFINITION OF DONE TOÀN PROJECT.
- **Task trước trong tiểu mục:** A29-027; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Kết quả từng nhóm và evidence gắn với version; yêu cầu riêng: Có disclaimer rõ ràng.
- **File/đầu ra:** thay đổi nhỏ trong docs/planning/acceptance.md; docs/acceptance/; evidence tại evidence/A29-028.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có disclaimer rõ ràng.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G29, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Nội dung khớp implementation đã kiểm chứng; ví dụ chạy được; link đúng; phân biệt demo/thực nghiệm/vận hành.
- **Kịch bản tiểu mục:** Mỗi tiêu chí đóng bằng test/report/demo; mục cần nguồn/tài khoản phải chờ bằng chứng thực tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
