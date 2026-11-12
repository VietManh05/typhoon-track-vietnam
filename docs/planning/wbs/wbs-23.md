# G23 — Kiểm thử xuyên hệ thống

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có 6 file test cũ; chưa có kiểm thử chuỗi hoàn chỉnh.
- Đầu vào: Các contract trước đã có unit tests và fixtures nhỏ.
- Gate phụ thuộc: G19, G21, G22.
- Vùng file dự kiến: tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Raw→train→bundle→inference→API→UI chạy; failure modes có assertion; load đo được thay vì tuyên bố production-ready.

<a id="gate-g23"></a>
## Gate G23

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t23-001"></a>
## T23-001 — Haversine.

- **Trạng thái:** pending.
- **Nguồn:** 23.1 Unit; dòng [1147](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1147).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.1 Unit.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Haversine.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Haversine.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Điểm trùng cho 0 km; cặp điểm chuẩn khớp dung sai; wrap longitude không tạo khoảng cách vòng trái đất.
- **Kịch bản tiểu mục:** Fixture độc lập có expected values; test chức năng ảnh hưởng kết quả, không chỉ mirror implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-002"></a>
## T23-002 — Bearing.

- **Trạng thái:** pending.
- **Nguồn:** 23.1 Unit; dòng [1148](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1148).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.1 Unit.
- **Task trước trong tiểu mục:** T23-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Bearing.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Bearing.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Hướng bắc/đông/tây đúng; 359→1 là đổi hướng nhỏ; điểm trùng có quy tắc công bố.
- **Kịch bản tiểu mục:** Fixture độc lập có expected values; test chức năng ảnh hưởng kết quả, không chỉ mirror implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-003"></a>
## T23-003 — Position.

- **Trạng thái:** pending.
- **Nguồn:** 23.1 Unit; dòng [1149](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1149).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.1 Unit.
- **Task trước trong tiểu mục:** T23-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Position.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Position.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture độc lập có expected values; test chức năng ảnh hưởng kết quả, không chỉ mirror implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-004"></a>
## T23-004 — Feature builder.

- **Trạng thái:** pending.
- **Nguồn:** 23.1 Unit; dòng [1150](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1150).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.1 Unit.
- **Task trước trong tiểu mục:** T23-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Feature builder.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Feature builder.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture độc lập có expected values; test chức năng ảnh hưởng kết quả, không chỉ mirror implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-005"></a>
## T23-005 — Scaler.

- **Trạng thái:** pending.
- **Nguồn:** 23.1 Unit; dòng [1151](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1151).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.1 Unit.
- **Task trước trong tiểu mục:** T23-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Scaler.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Scaler.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fit train-only; val/test cực trị không đổi stats; save/load giữ order/fill; finite round-trip <=1e-6.
- **Kịch bản tiểu mục:** Fixture độc lập có expected values; test chức năng ảnh hưởng kết quả, không chỉ mirror implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-006"></a>
## T23-006 — Dataset.

- **Trạng thái:** pending.
- **Nguồn:** 23.1 Unit; dòng [1152](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1152).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.1 Unit.
- **Task trước trong tiểu mục:** T23-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Dataset.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Dataset.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture độc lập có expected values; test chức năng ảnh hưởng kết quả, không chỉ mirror implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-007"></a>
## T23-007 — Model.

- **Trạng thái:** pending.
- **Nguồn:** 23.1 Unit; dòng [1153](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1153).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.1 Unit.
- **Task trước trong tiểu mục:** T23-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Model.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Model.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture độc lập có expected values; test chức năng ảnh hưởng kết quả, không chỉ mirror implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-008"></a>
## T23-008 — Cone.

- **Trạng thái:** pending.
- **Nguồn:** 23.1 Unit; dòng [1154](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1154).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.1 Unit.
- **Task trước trong tiểu mục:** T23-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Cone.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cone.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** GeoJSON [lon,lat], ring đóng/topology hợp lệ; dateline có xử lý; coverage thực nghiệm khác radius minh họa.
- **Kịch bản tiểu mục:** Fixture độc lập có expected values; test chức năng ảnh hưởng kết quả, không chỉ mirror implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-009"></a>
## T23-009 — Alert rules.

- **Trạng thái:** pending.
- **Nguồn:** 23.1 Unit; dòng [1155](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1155).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.1 Unit.
- **Task trước trong tiểu mục:** T23-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Alert rules.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Alert rules.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture độc lập có expected values; test chức năng ảnh hưởng kết quả, không chỉ mirror implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-010"></a>
## T23-010 — Raw → clean.

- **Trạng thái:** pending.
- **Nguồn:** 23.2 Integration; dòng [1158](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1158).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.2 Integration.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Raw → clean.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Raw → clean.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture raw nhỏ → clean → feature → split → train 1 epoch → bundle → reload → forecast → API → UI; không gọi Internet trong CI.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-011"></a>
## T23-011 — Clean → feature.

- **Trạng thái:** pending.
- **Nguồn:** 23.2 Integration; dòng [1159](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1159).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.2 Integration.
- **Task trước trong tiểu mục:** T23-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Clean → feature.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Clean → feature.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture raw nhỏ → clean → feature → split → train 1 epoch → bundle → reload → forecast → API → UI; không gọi Internet trong CI.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-012"></a>
## T23-012 — Feature → dataset.

- **Trạng thái:** pending.
- **Nguồn:** 23.2 Integration; dòng [1160](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1160).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.2 Integration.
- **Task trước trong tiểu mục:** T23-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Feature → dataset.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Feature → dataset.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture raw nhỏ → clean → feature → split → train 1 epoch → bundle → reload → forecast → API → UI; không gọi Internet trong CI.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-013"></a>
## T23-013 — Dataset → train.

- **Trạng thái:** pending.
- **Nguồn:** 23.2 Integration; dòng [1161](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1161).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.2 Integration.
- **Task trước trong tiểu mục:** T23-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Dataset → train.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Dataset → train.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture raw nhỏ → clean → feature → split → train 1 epoch → bundle → reload → forecast → API → UI; không gọi Internet trong CI.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-014"></a>
## T23-014 — Train → model.

- **Trạng thái:** pending.
- **Nguồn:** 23.2 Integration; dòng [1162](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1162).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.2 Integration.
- **Task trước trong tiểu mục:** T23-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Train → model.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Train → model.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture raw nhỏ → clean → feature → split → train 1 epoch → bundle → reload → forecast → API → UI; không gọi Internet trong CI.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-015"></a>
## T23-015 — Model → inference.

- **Trạng thái:** pending.
- **Nguồn:** 23.2 Integration; dòng [1163](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1163).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.2 Integration.
- **Task trước trong tiểu mục:** T23-014; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Model → inference.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Model → inference.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture raw nhỏ → clean → feature → split → train 1 epoch → bundle → reload → forecast → API → UI; không gọi Internet trong CI.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-016"></a>
## T23-016 — Inference → API.

- **Trạng thái:** pending.
- **Nguồn:** 23.2 Integration; dòng [1164](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1164).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.2 Integration.
- **Task trước trong tiểu mục:** T23-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Inference → API.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Inference → API.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture raw nhỏ → clean → feature → split → train 1 epoch → bundle → reload → forecast → API → UI; không gọi Internet trong CI.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-017"></a>
## T23-017 — API → frontend.

- **Trạng thái:** pending.
- **Nguồn:** 23.2 Integration; dòng [1165](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1165).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.2 Integration.
- **Task trước trong tiểu mục:** T23-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: API → frontend.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “API → frontend.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture raw nhỏ → clean → feature → split → train 1 epoch → bundle → reload → forecast → API → UI; không gọi Internet trong CI.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-018"></a>
## T23-018 — Missing observation.

- **Trạng thái:** pending.
- **Nguồn:** 23.3 Edge cases; dòng [1168](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1168).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.3 Edge cases.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Missing observation.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Missing observation.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Mỗi edge case có expected status/output/warning; không để exception hoặc NaN lọt response.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-019"></a>
## T23-019 — Missing SST.

- **Trạng thái:** pending.
- **Nguồn:** 23.3 Edge cases; dòng [1169](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1169).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.3 Edge cases.
- **Task trước trong tiểu mục:** T23-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Missing SST.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Missing SST.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Mỗi edge case có expected status/output/warning; không để exception hoặc NaN lọt response.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-020"></a>
## T23-020 — Missing wind shear.

- **Trạng thái:** pending.
- **Nguồn:** 23.3 Edge cases; dòng [1170](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1170).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.3 Edge cases.
- **Task trước trong tiểu mục:** T23-019; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Missing wind shear.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-020.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Missing wind shear.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Mỗi edge case có expected status/output/warning; không để exception hoặc NaN lọt response.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-021"></a>
## T23-021 — Sudden turn.

- **Trạng thái:** pending.
- **Nguồn:** 23.3 Edge cases; dòng [1171](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1171).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.3 Edge cases.
- **Task trước trong tiểu mục:** T23-020; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Sudden turn.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-021.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Sudden turn.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mỗi edge case có expected status/output/warning; không để exception hoặc NaN lọt response.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-022"></a>
## T23-022 — Near coastline.

- **Trạng thái:** pending.
- **Nguồn:** 23.3 Edge cases; dòng [1172](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1172).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.3 Edge cases.
- **Task trước trong tiểu mục:** T23-021; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Near coastline.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-022.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Near coastline.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mỗi edge case có expected status/output/warning; không để exception hoặc NaN lọt response.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-023"></a>
## T23-023 — Weakening storm.

- **Trạng thái:** pending.
- **Nguồn:** 23.3 Edge cases; dòng [1173](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1173).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.3 Edge cases.
- **Task trước trong tiểu mục:** T23-022; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Weakening storm.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-023.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Weakening storm.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mỗi edge case có expected status/output/warning; không để exception hoặc NaN lọt response.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-024"></a>
## T23-024 — Invalid coordinate.

- **Trạng thái:** pending.
- **Nguồn:** 23.3 Edge cases; dòng [1174](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1174).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.3 Edge cases.
- **Task trước trong tiểu mục:** T23-023; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Invalid coordinate.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-024.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Invalid coordinate.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mỗi edge case có expected status/output/warning; không để exception hoặc NaN lọt response.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-025"></a>
## T23-025 — Duplicate observation.

- **Trạng thái:** pending.
- **Nguồn:** 23.3 Edge cases; dòng [1175](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1175).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.3 Edge cases.
- **Task trước trong tiểu mục:** T23-024; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Duplicate observation.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-025.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Duplicate observation.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mỗi edge case có expected status/output/warning; không để exception hoặc NaN lọt response.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-026"></a>
## T23-026 — Multiple active storms.

- **Trạng thái:** pending.
- **Nguồn:** 23.3 Edge cases; dòng [1176](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1176).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.3 Edge cases.
- **Task trước trong tiểu mục:** T23-025; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Multiple active storms.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-026.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Multiple active storms.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mỗi edge case có expected status/output/warning; không để exception hoặc NaN lọt response.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-027"></a>
## T23-027 — API concurrent requests.

- **Trạng thái:** pending.
- **Nguồn:** 23.4 Load; dòng [1179](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1179).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.4 Load.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: API concurrent requests.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-027.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “API concurrent requests.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Cấu hình tải và phần cứng ghi rõ; đo p50/p95/error rate; chạy concurrency, cache mất kết nối và worker redelivery; không load test nguồn bên ngoài.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-028"></a>
## T23-028 — Database load.

- **Trạng thái:** pending.
- **Nguồn:** 23.4 Load; dòng [1180](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1180).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.4 Load.
- **Task trước trong tiểu mục:** T23-027; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Database load.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-028.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Database load.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Cấu hình tải và phần cứng ghi rõ; đo p50/p95/error rate; chạy concurrency, cache mất kết nối và worker redelivery; không load test nguồn bên ngoài.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-029"></a>
## T23-029 — Cache load.

- **Trạng thái:** pending.
- **Nguồn:** 23.4 Load; dòng [1181](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1181).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.4 Load.
- **Task trước trong tiểu mục:** T23-028; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Cache load.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-029.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cache load.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hit/miss/expiry, observation sửa/model đổi và outage; cache key bao gồm input+model revision.
- **Kịch bản tiểu mục:** Cấu hình tải và phần cứng ghi rõ; đo p50/p95/error rate; chạy concurrency, cache mất kết nối và worker redelivery; không load test nguồn bên ngoài.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-030"></a>
## T23-030 — Worker retry.

- **Trạng thái:** pending.
- **Nguồn:** 23.4 Load; dòng [1182](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1182).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.4 Load.
- **Task trước trong tiểu mục:** T23-029; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Worker retry.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-030.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Worker retry.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fake transport lỗi rồi thành công; số lần thử/timeout theo cấu hình; hết retry có trạng thái thất bại và log.
- **Kịch bản tiểu mục:** Cấu hình tải và phần cứng ghi rõ; đo p50/p95/error rate; chạy concurrency, cache mất kết nối và worker redelivery; không load test nguồn bên ngoài.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t23-031"></a>
## T23-031 — Traffic spike scenario.

- **Trạng thái:** pending.
- **Nguồn:** 23.4 Load; dòng [1183](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1183).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21, G22; contract/fixture của tiểu mục 23.4 Load.
- **Task trước trong tiểu mục:** T23-030; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Các contract trước đã có unit tests và fixtures nhỏ; yêu cầu riêng: Traffic spike scenario.
- **File/đầu ra:** thay đổi nhỏ trong tests/; tests/integration/; tests/model/; tests/frontend/; tests/load/; evidence tại evidence/T23-031.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Traffic spike scenario.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G23, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Cấu hình tải và phần cứng ghi rõ; đo p50/p95/error rate; chạy concurrency, cache mất kết nối và worker redelivery; không load test nguồn bên ngoài.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
