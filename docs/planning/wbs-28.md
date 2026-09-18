# G28 — Demo và nghiệm thu

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Chưa nghiệm thu.
- Đầu vào: Release candidate, checklist DoD, fixtures và evidence.
- Gate phụ thuộc: G23, G25, G26, G27.
- Vùng file dự kiến: docs/acceptance/; reports/; tests/integration/; viz/frontend/.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.

<a id="gate-g28"></a>
## Gate G28

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t28-001"></a>
## T28-001 — Chọn một cơn bão.

- **Trạng thái:** pending.
- **Nguồn:** Demo 1 — Dữ liệu; dòng [1273](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1273).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 1 — Dữ liệu.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Chọn một cơn bão.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chọn một cơn bão.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-002"></a>
## T28-002 — Hiển thị lịch sử.

- **Trạng thái:** pending.
- **Nguồn:** Demo 1 — Dữ liệu; dòng [1274](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1274).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 1 — Dữ liệu.
- **Task trước trong tiểu mục:** T28-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Hiển thị lịch sử.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Hiển thị lịch sử.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-003"></a>
## T28-003 — Chứng minh data pipeline.

- **Trạng thái:** pending.
- **Nguồn:** Demo 1 — Dữ liệu; dòng [1275](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1275).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 1 — Dữ liệu.
- **Task trước trong tiểu mục:** T28-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Chứng minh data pipeline.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chứng minh data pipeline.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-004"></a>
## T28-004 — Load model.

- **Trạng thái:** pending.
- **Nguồn:** Demo 2 — Model; dòng [1278](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1278).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 2 — Model.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Load model.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Load model.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-005"></a>
## T28-005 — Nhập observation.

- **Trạng thái:** pending.
- **Nguồn:** Demo 2 — Model; dòng [1279](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1279).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 2 — Model.
- **Task trước trong tiểu mục:** T28-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Nhập observation.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Nhập observation.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-006"></a>
## T28-006 — Sinh 6/12/24/48/72h.

- **Trạng thái:** pending.
- **Nguồn:** Demo 2 — Model; dòng [1280](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1280).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 2 — Model.
- **Task trước trong tiểu mục:** T28-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Sinh 6/12/24/48/72h.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Sinh 6/12/24/48/72h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-007"></a>
## T28-007 — Hiển thị metric.

- **Trạng thái:** pending.
- **Nguồn:** Demo 2 — Model; dòng [1281](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1281).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 2 — Model.
- **Task trước trong tiểu mục:** T28-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Hiển thị metric.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Hiển thị metric.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-008"></a>
## T28-008 — Actual track.

- **Trạng thái:** pending.
- **Nguồn:** Demo 3 — Bản đồ; dòng [1284](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1284).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 3 — Bản đồ.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Actual track.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Actual track.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-009"></a>
## T28-009 — Forecast track.

- **Trạng thái:** pending.
- **Nguồn:** Demo 3 — Bản đồ; dòng [1285](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1285).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 3 — Bản đồ.
- **Task trước trong tiểu mục:** T28-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Forecast track.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Forecast track.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-010"></a>
## T28-010 — Cone.

- **Trạng thái:** pending.
- **Nguồn:** Demo 3 — Bản đồ; dòng [1286](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1286).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 3 — Bản đồ.
- **Task trước trong tiểu mục:** T28-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Cone.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cone.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** GeoJSON [lon,lat], ring đóng/topology hợp lệ; dateline có xử lý; coverage thực nghiệm khác radius minh họa.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-011"></a>
## T28-011 — Province impact.

- **Trạng thái:** pending.
- **Nguồn:** Demo 3 — Bản đồ; dòng [1287](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1287).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 3 — Bản đồ.
- **Task trước trong tiểu mục:** T28-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Province impact.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Province impact.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-012"></a>
## T28-012 — Swagger.

- **Trạng thái:** pending.
- **Nguồn:** Demo 4 — API; dòng [1290](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1290).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 4 — API.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Swagger.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Swagger.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-013"></a>
## T28-013 — POST forecast.

- **Trạng thái:** pending.
- **Nguồn:** Demo 4 — API; dòng [1291](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1291).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 4 — API.
- **Task trước trong tiểu mục:** T28-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: POST forecast.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “POST forecast.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-014"></a>
## T28-014 — Response.

- **Trạng thái:** pending.
- **Nguồn:** Demo 4 — API; dòng [1292](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1292).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 4 — API.
- **Task trước trong tiểu mục:** T28-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Response.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Response.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-015"></a>
## T28-015 — Error handling.

- **Trạng thái:** pending.
- **Nguồn:** Demo 4 — API; dòng [1293](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1293).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 4 — API.
- **Task trước trong tiểu mục:** T28-014; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Error handling.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Error handling.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-016"></a>
## T28-016 — Mock observation mới.

- **Trạng thái:** pending.
- **Nguồn:** Demo 5 — Real-time; dòng [1296](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1296).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 5 — Real-time.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Mock observation mới.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Mock observation mới.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-017"></a>
## T28-017 — Worker nhận dữ liệu.

- **Trạng thái:** pending.
- **Nguồn:** Demo 5 — Real-time; dòng [1297](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1297).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 5 — Real-time.
- **Task trước trong tiểu mục:** T28-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Worker nhận dữ liệu.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Worker nhận dữ liệu.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-018"></a>
## T28-018 — Trigger inference.

- **Trạng thái:** pending.
- **Nguồn:** Demo 5 — Real-time; dòng [1298](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1298).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 5 — Real-time.
- **Task trước trong tiểu mục:** T28-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Trigger inference.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Trigger inference.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-019"></a>
## T28-019 — Dashboard cập nhật.

- **Trạng thái:** pending.
- **Nguồn:** Demo 5 — Real-time; dòng [1299](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1299).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 5 — Real-time.
- **Task trước trong tiểu mục:** T28-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Dashboard cập nhật.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Dashboard cập nhật.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-020"></a>
## T28-020 — Tạo subscription.

- **Trạng thái:** pending.
- **Nguồn:** Demo 6 — Alert; dòng [1302](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1302).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 6 — Alert.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Tạo subscription.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-020.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo subscription.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-021"></a>
## T28-021 — Kích hoạt rule.

- **Trạng thái:** pending.
- **Nguồn:** Demo 6 — Alert; dòng [1303](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1303).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 6 — Alert.
- **Task trước trong tiểu mục:** T28-020; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Kích hoạt rule.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-021.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kích hoạt rule.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-022"></a>
## T28-022 — Sinh cảnh báo.

- **Trạng thái:** pending.
- **Nguồn:** Demo 6 — Alert; dòng [1304](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1304).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 6 — Alert.
- **Task trước trong tiểu mục:** T28-021; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Sinh cảnh báo.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-022.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Sinh cảnh báo.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Kịch bản có input/version, bước thao tác, expected/actual và ảnh/log; chạy lại được trên release candidate.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t28-023"></a>
## T28-023 — Kiểm tra throttle.

- **Trạng thái:** pending.
- **Nguồn:** Demo 6 — Alert; dòng [1305](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1305).
- **Loại:** demo bằng chứng.
- **Phụ thuộc:** G23, G25, G26, G27; contract/fixture của tiểu mục Demo 6 — Alert.
- **Task trước trong tiểu mục:** T28-022; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Release candidate, checklist DoD, fixtures và evidence; yêu cầu riêng: Kiểm tra throttle.
- **File/đầu ra:** thay đổi nhỏ trong docs/acceptance/; reports/; tests/integration/; viz/frontend/; evidence tại evidence/T28-023.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra throttle.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G28, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fake transport không gửi trùng event qua restart/redelivery; cooldown đúng biên; không gửi tin thật trong test.
- **Kịch bản tiểu mục:** Demo data/model/map/API/worker/alert có evidence; không tự gửi tin hay deploy thật; đánh dấu external pending trung thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
