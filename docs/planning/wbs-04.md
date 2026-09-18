# G04 — Feature engineering

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có feature builder; môi trường và hợp đồng train/serve cần kiểm chứng.
- Đầu vào: Track sạch, timestamp UTC, dữ liệu môi trường có available_at.
- Gate phụ thuộc: G02, G03.
- Vùng file dự kiến: src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Mỗi feature có dtype, đơn vị, nguồn, missing policy; train/serve cùng thuật toán và thứ tự; chỉ dùng thông tin đã có tại issue_time.

<a id="gate-g04"></a>
## Gate G04

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t04-001"></a>
## T04-001 — latitude.

- **Trạng thái:** pending.
- **Nguồn:** 4.1 Position; dòng [616](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:616).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.1 Position.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: latitude.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “latitude.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hợp lệ/ngoài biên/NaN/Inf và wrap longitude; output giữ đúng đơn vị tọa độ.
- **Kịch bản tiểu mục:** Tạo fixture lat=[10,11,13], lon=[120,119,117]; lag/delta reset ở storm mới; xử lý wrap 179→-179 theo policy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-002"></a>
## T04-002 — longitude.

- **Trạng thái:** pending.
- **Nguồn:** 4.1 Position; dòng [617](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:617).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.1 Position.
- **Task trước trong tiểu mục:** T04-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: longitude.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “longitude.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hợp lệ/ngoài biên/NaN/Inf và wrap longitude; output giữ đúng đơn vị tọa độ.
- **Kịch bản tiểu mục:** Tạo fixture lat=[10,11,13], lon=[120,119,117]; lag/delta reset ở storm mới; xử lý wrap 179→-179 theo policy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-003"></a>
## T04-003 — delta latitude.

- **Trạng thái:** pending.
- **Nguồn:** 4.1 Position; dòng [618](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:618).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.1 Position.
- **Task trước trong tiểu mục:** T04-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: delta latitude.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “delta latitude.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hợp lệ/ngoài biên/NaN/Inf và wrap longitude; output giữ đúng đơn vị tọa độ.
- **Kịch bản tiểu mục:** Tạo fixture lat=[10,11,13], lon=[120,119,117]; lag/delta reset ở storm mới; xử lý wrap 179→-179 theo policy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-004"></a>
## T04-004 — delta longitude.

- **Trạng thái:** pending.
- **Nguồn:** 4.1 Position; dòng [619](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:619).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.1 Position.
- **Task trước trong tiểu mục:** T04-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: delta longitude.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “delta longitude.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hợp lệ/ngoài biên/NaN/Inf và wrap longitude; output giữ đúng đơn vị tọa độ.
- **Kịch bản tiểu mục:** Tạo fixture lat=[10,11,13], lon=[120,119,117]; lag/delta reset ở storm mới; xử lý wrap 179→-179 theo policy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-005"></a>
## T04-005 — Position lag 1.

- **Trạng thái:** pending.
- **Nguồn:** 4.1 Position; dòng [620](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:620).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.1 Position.
- **Task trước trong tiểu mục:** T04-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Position lag 1.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Position lag 1.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Tạo fixture lat=[10,11,13], lon=[120,119,117]; lag/delta reset ở storm mới; xử lý wrap 179→-179 theo policy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-006"></a>
## T04-006 — Position lag 2.

- **Trạng thái:** pending.
- **Nguồn:** 4.1 Position; dòng [621](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:621).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.1 Position.
- **Task trước trong tiểu mục:** T04-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Position lag 2.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Position lag 2.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Tạo fixture lat=[10,11,13], lon=[120,119,117]; lag/delta reset ở storm mới; xử lý wrap 179→-179 theo policy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-007"></a>
## T04-007 — Position lag 3.

- **Trạng thái:** pending.
- **Nguồn:** 4.1 Position; dòng [622](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:622).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.1 Position.
- **Task trước trong tiểu mục:** T04-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Position lag 3.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Position lag 3.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Tạo fixture lat=[10,11,13], lon=[120,119,117]; lag/delta reset ở storm mới; xử lý wrap 179→-179 theo policy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-008"></a>
## T04-008 — Haversine distance.

- **Trạng thái:** pending.
- **Nguồn:** 4.2 Motion; dòng [625](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:625).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.2 Motion.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Haversine distance.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Haversine distance.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Điểm trùng cho 0 km; cặp điểm chuẩn khớp dung sai; wrap longitude không tạo khoảng cách vòng trái đất.
- **Kịch bản tiểu mục:** Hai fix có thời gian biết trước; distance/delta_hours ra km/h; đổi hướng 359→1 là 2 độ; duplicate timestamp không chia 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-009"></a>
## T04-009 — Bearing.

- **Trạng thái:** pending.
- **Nguồn:** 4.2 Motion; dòng [626](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:626).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.2 Motion.
- **Task trước trong tiểu mục:** T04-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Bearing.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Bearing.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Hướng bắc/đông/tây đúng; 359→1 là đổi hướng nhỏ; điểm trùng có quy tắc công bố.
- **Kịch bản tiểu mục:** Hai fix có thời gian biết trước; distance/delta_hours ra km/h; đổi hướng 359→1 là 2 độ; duplicate timestamp không chia 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-010"></a>
## T04-010 — Speed.

- **Trạng thái:** pending.
- **Nguồn:** 4.2 Motion; dòng [627](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:627).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.2 Motion.
- **Task trước trong tiểu mục:** T04-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Speed.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Speed.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Hai fix có thời gian biết trước; distance/delta_hours ra km/h; đổi hướng 359→1 là 2 độ; duplicate timestamp không chia 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-011"></a>
## T04-011 — Acceleration.

- **Trạng thái:** pending.
- **Nguồn:** 4.2 Motion; dòng [628](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:628).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.2 Motion.
- **Task trước trong tiểu mục:** T04-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Acceleration.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Acceleration.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Hai fix có thời gian biết trước; distance/delta_hours ra km/h; đổi hướng 359→1 là 2 độ; duplicate timestamp không chia 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-012"></a>
## T04-012 — Bearing change.

- **Trạng thái:** pending.
- **Nguồn:** 4.2 Motion; dòng [629](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:629).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.2 Motion.
- **Task trước trong tiểu mục:** T04-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Bearing change.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Bearing change.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Hướng bắc/đông/tây đúng; 359→1 là đổi hướng nhỏ; điểm trùng có quy tắc công bố.
- **Kịch bản tiểu mục:** Hai fix có thời gian biết trước; distance/delta_hours ra km/h; đổi hướng 359→1 là 2 độ; duplicate timestamp không chia 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-013"></a>
## T04-013 — Turning rate.

- **Trạng thái:** pending.
- **Nguồn:** 4.2 Motion; dòng [630](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:630).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.2 Motion.
- **Task trước trong tiểu mục:** T04-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Turning rate.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Turning rate.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Hai fix có thời gian biết trước; distance/delta_hours ra km/h; đổi hướng 359→1 là 2 độ; duplicate timestamp không chia 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-014"></a>
## T04-014 — Direction sin/cos.

- **Trạng thái:** pending.
- **Nguồn:** 4.2 Motion; dòng [631](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:631).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.2 Motion.
- **Task trước trong tiểu mục:** T04-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Direction sin/cos.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Direction sin/cos.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Hướng bắc/đông/tây đúng; 359→1 là đổi hướng nhỏ; điểm trùng có quy tắc công bố.
- **Kịch bản tiểu mục:** Hai fix có thời gian biết trước; distance/delta_hours ra km/h; đổi hướng 359→1 là 2 độ; duplicate timestamp không chia 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-015"></a>
## T04-015 — Distance to coastline.

- **Trạng thái:** pending.
- **Nguồn:** 4.3 Coast; dòng [634](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:634).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.3 Coast.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Distance to coastline.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Distance to coastline.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Điểm trùng cho 0 km; cặp điểm chuẩn khớp dung sai; wrap longitude không tạo khoảng cách vòng trái đất.
- **Kịch bản tiểu mục:** Điểm kiểm thử ở bờ và ngoài biển; dùng geodesic km và shoreline thật; dữ liệu coastline toy phải có nhãn approximate.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-016"></a>
## T04-016 — Bearing to coastline.

- **Trạng thái:** pending.
- **Nguồn:** 4.3 Coast; dòng [635](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:635).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.3 Coast.
- **Task trước trong tiểu mục:** T04-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Bearing to coastline.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Bearing to coastline.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Hướng bắc/đông/tây đúng; 359→1 là đổi hướng nhỏ; điểm trùng có quy tắc công bố.
- **Kịch bản tiểu mục:** Điểm kiểm thử ở bờ và ngoài biển; dùng geodesic km và shoreline thật; dữ liệu coastline toy phải có nhãn approximate.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-017"></a>
## T04-017 — Nearest coastline point.

- **Trạng thái:** pending.
- **Nguồn:** 4.3 Coast; dòng [636](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:636).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.3 Coast.
- **Task trước trong tiểu mục:** T04-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Nearest coastline point.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Nearest coastline point.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Điểm kiểm thử ở bờ và ngoài biển; dùng geodesic km và shoreline thật; dữ liệu coastline toy phải có nhãn approximate.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-018"></a>
## T04-018 — Distance to nearest province.

- **Trạng thái:** pending.
- **Nguồn:** 4.3 Coast; dòng [637](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:637).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.3 Coast.
- **Task trước trong tiểu mục:** T04-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Distance to nearest province.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Distance to nearest province.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Điểm trùng cho 0 km; cặp điểm chuẩn khớp dung sai; wrap longitude không tạo khoảng cách vòng trái đất.
- **Kịch bản tiểu mục:** Điểm kiểm thử ở bờ và ngoài biển; dùng geodesic km và shoreline thật; dữ liệu coastline toy phải có nhãn approximate.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-019"></a>
## T04-019 — Hour.

- **Trạng thái:** pending.
- **Nguồn:** 4.4 Time; dòng [640](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:640).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.4 Time.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Hour.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Hour.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Test giờ 23→0, tháng 12→1, năm nhuận và UTC; chu kỳ và season flag có định nghĩa rõ, không phụ thuộc dữ liệu test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-020"></a>
## T04-020 — Hour sin/cos.

- **Trạng thái:** pending.
- **Nguồn:** 4.4 Time; dòng [641](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:641).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.4 Time.
- **Task trước trong tiểu mục:** T04-019; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Hour sin/cos.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-020.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Hour sin/cos.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Test giờ 23→0, tháng 12→1, năm nhuận và UTC; chu kỳ và season flag có định nghĩa rõ, không phụ thuộc dữ liệu test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-021"></a>
## T04-021 — Day.

- **Trạng thái:** pending.
- **Nguồn:** 4.4 Time; dòng [642](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:642).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.4 Time.
- **Task trước trong tiểu mục:** T04-020; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Day.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-021.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Day.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Test giờ 23→0, tháng 12→1, năm nhuận và UTC; chu kỳ và season flag có định nghĩa rõ, không phụ thuộc dữ liệu test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-022"></a>
## T04-022 — Day sin/cos.

- **Trạng thái:** pending.
- **Nguồn:** 4.4 Time; dòng [643](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:643).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.4 Time.
- **Task trước trong tiểu mục:** T04-021; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Day sin/cos.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-022.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Day sin/cos.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Test giờ 23→0, tháng 12→1, năm nhuận và UTC; chu kỳ và season flag có định nghĩa rõ, không phụ thuộc dữ liệu test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-023"></a>
## T04-023 — Month.

- **Trạng thái:** pending.
- **Nguồn:** 4.4 Time; dòng [644](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:644).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.4 Time.
- **Task trước trong tiểu mục:** T04-022; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Month.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-023.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Month.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Test giờ 23→0, tháng 12→1, năm nhuận và UTC; chu kỳ và season flag có định nghĩa rõ, không phụ thuộc dữ liệu test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-024"></a>
## T04-024 — Month sin/cos.

- **Trạng thái:** pending.
- **Nguồn:** 4.4 Time; dòng [645](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:645).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.4 Time.
- **Task trước trong tiểu mục:** T04-023; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Month sin/cos.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-024.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Month sin/cos.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Test giờ 23→0, tháng 12→1, năm nhuận và UTC; chu kỳ và season flag có định nghĩa rõ, không phụ thuộc dữ liệu test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-025"></a>
## T04-025 — Day of year.

- **Trạng thái:** pending.
- **Nguồn:** 4.4 Time; dòng [646](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:646).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.4 Time.
- **Task trước trong tiểu mục:** T04-024; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Day of year.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-025.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Day of year.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Test giờ 23→0, tháng 12→1, năm nhuận và UTC; chu kỳ và season flag có định nghĩa rõ, không phụ thuộc dữ liệu test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-026"></a>
## T04-026 — Day-of-year sin/cos.

- **Trạng thái:** pending.
- **Nguồn:** 4.4 Time; dòng [647](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:647).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.4 Time.
- **Task trước trong tiểu mục:** T04-025; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Day-of-year sin/cos.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-026.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Day-of-year sin/cos.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Test giờ 23→0, tháng 12→1, năm nhuận và UTC; chu kỳ và season flag có định nghĩa rõ, không phụ thuộc dữ liệu test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-027"></a>
## T04-027 — Season flag.

- **Trạng thái:** pending.
- **Nguồn:** 4.4 Time; dòng [648](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:648).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.4 Time.
- **Task trước trong tiểu mục:** T04-026; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Season flag.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-027.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Season flag.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Test giờ 23→0, tháng 12→1, năm nhuận và UTC; chu kỳ và season flag có định nghĩa rõ, không phụ thuộc dữ liệu test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-028"></a>
## T04-028 — Wind.

- **Trạng thái:** pending.
- **Nguồn:** 4.5 Intensity; dòng [651](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:651).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.5 Intensity.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Wind.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-028.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Wind.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Knot→m/s, hPa, unknown category và class vắng trong train; one-hot giữ chiều cố định; class không suy tự động từ test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-029"></a>
## T04-029 — Pressure.

- **Trạng thái:** pending.
- **Nguồn:** 4.5 Intensity; dòng [652](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:652).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.5 Intensity.
- **Task trước trong tiểu mục:** T04-028; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Pressure.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-029.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Pressure.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Knot→m/s, hPa, unknown category và class vắng trong train; one-hot giữ chiều cố định; class không suy tự động từ test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-030"></a>
## T04-030 — Intensity category.

- **Trạng thái:** pending.
- **Nguồn:** 4.5 Intensity; dòng [653](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:653).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.5 Intensity.
- **Task trước trong tiểu mục:** T04-029; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Intensity category.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-030.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Intensity category.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Knot→m/s, hPa, unknown category và class vắng trong train; one-hot giữ chiều cố định; class không suy tự động từ test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-031"></a>
## T04-031 — Wind change.

- **Trạng thái:** pending.
- **Nguồn:** 4.5 Intensity; dòng [654](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:654).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.5 Intensity.
- **Task trước trong tiểu mục:** T04-030; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Wind change.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-031.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Wind change.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Knot→m/s, hPa, unknown category và class vắng trong train; one-hot giữ chiều cố định; class không suy tự động từ test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-032"></a>
## T04-032 — Pressure change.

- **Trạng thái:** pending.
- **Nguồn:** 4.5 Intensity; dòng [655](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:655).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.5 Intensity.
- **Task trước trong tiểu mục:** T04-031; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Pressure change.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-032.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Pressure change.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Knot→m/s, hPa, unknown category và class vắng trong train; one-hot giữ chiều cố định; class không suy tự động từ test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-033"></a>
## T04-033 — Download SST.

- **Trạng thái:** pending.
- **Nguồn:** 4.6 SST; dòng [658](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:658).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.6 SST.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Download SST.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-033.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Download SST.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Mock bytes xác định và HTTP failure; checksum/raw giữ nguyên; lần tải thật phải có nguồn hợp lệ và evidence riêng.
- **Kịch bản tiểu mục:** Grid SST nhỏ có expected center/gradient tính tay; Celsius/Kelvin và missing mask rõ; chọn field available_at không sau issue_time.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-034"></a>
## T04-034 — Match timestamp.

- **Trạng thái:** pending.
- **Nguồn:** 4.6 SST; dòng [659](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:659).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.6 SST.
- **Task trước trong tiểu mục:** T04-033; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Match timestamp.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-034.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Match timestamp.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt.
- **Kịch bản tiểu mục:** Grid SST nhỏ có expected center/gradient tính tay; Celsius/Kelvin và missing mask rõ; chọn field available_at không sau issue_time.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-035"></a>
## T04-035 — Match grid.

- **Trạng thái:** pending.
- **Nguồn:** 4.6 SST; dòng [660](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:660).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.6 SST.
- **Task trước trong tiểu mục:** T04-034; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Match grid.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-035.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Match grid.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Grid SST nhỏ có expected center/gradient tính tay; Celsius/Kelvin và missing mask rõ; chọn field available_at không sau issue_time.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-036"></a>
## T04-036 — Sample SST at storm center.

- **Trạng thái:** pending.
- **Nguồn:** 4.6 SST; dòng [661](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:661).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.6 SST.
- **Task trước trong tiểu mục:** T04-035; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Sample SST at storm center.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-036.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Sample SST at storm center.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Grid SST nhỏ có expected center/gradient tính tay; Celsius/Kelvin và missing mask rõ; chọn field available_at không sau issue_time.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-037"></a>
## T04-037 — Calculate SST gradient.

- **Trạng thái:** pending.
- **Nguồn:** 4.6 SST; dòng [662](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:662).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.6 SST.
- **Task trước trong tiểu mục:** T04-036; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Calculate SST gradient.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-037.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Calculate SST gradient.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Loss/gradient hữu hạn với fixture đúng; NaN/empty phải fail rõ và không lưu best checkpoint giả.
- **Kịch bản tiểu mục:** Grid SST nhỏ có expected center/gradient tính tay; Celsius/Kelvin và missing mask rõ; chọn field available_at không sau issue_time.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-038"></a>
## T04-038 — Validate missing.

- **Trạng thái:** pending.
- **Nguồn:** 4.6 SST; dòng [663](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:663).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.6 SST.
- **Task trước trong tiểu mục:** T04-037; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Validate missing.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-038.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Validate missing.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Grid SST nhỏ có expected center/gradient tính tay; Celsius/Kelvin và missing mask rõ; chọn field available_at không sau issue_time.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-039"></a>
## T04-039 — Cache extracted feature.

- **Trạng thái:** pending.
- **Nguồn:** 4.6 SST; dòng [664](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:664).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.6 SST.
- **Task trước trong tiểu mục:** T04-038; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Cache extracted feature.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-039.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cache extracted feature.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hit/miss/expiry, observation sửa/model đổi và outage; cache key bao gồm input+model revision.
- **Kịch bản tiểu mục:** Grid SST nhỏ có expected center/gradient tính tay; Celsius/Kelvin và missing mask rõ; chọn field available_at không sau issue_time.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-040"></a>
## T04-040 — Load ERA5.

- **Trạng thái:** pending.
- **Nguồn:** 4.7 Atmospheric Features; dòng [667](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:667).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.7 Atmospheric Features.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Load ERA5.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-040.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Load ERA5.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture u/v ở 850/200hPa; shear=sqrt((u200-u850)^2+(v200-v850)^2); pressure Pa→hPa; không dùng field tương lai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-041"></a>
## T04-041 — Extract sea-level pressure.

- **Trạng thái:** pending.
- **Nguồn:** 4.7 Atmospheric Features; dòng [668](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:668).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.7 Atmospheric Features.
- **Task trước trong tiểu mục:** T04-040; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Extract sea-level pressure.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-041.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Extract sea-level pressure.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Fixture u/v ở 850/200hPa; shear=sqrt((u200-u850)^2+(v200-v850)^2); pressure Pa→hPa; không dùng field tương lai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-042"></a>
## T04-042 — Extract 850 hPa wind.

- **Trạng thái:** pending.
- **Nguồn:** 4.7 Atmospheric Features; dòng [669](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:669).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.7 Atmospheric Features.
- **Task trước trong tiểu mục:** T04-041; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Extract 850 hPa wind.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-042.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Extract 850 hPa wind.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Fixture u/v ở 850/200hPa; shear=sqrt((u200-u850)^2+(v200-v850)^2); pressure Pa→hPa; không dùng field tương lai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-043"></a>
## T04-043 — Extract 200 hPa wind.

- **Trạng thái:** pending.
- **Nguồn:** 4.7 Atmospheric Features; dòng [670](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:670).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.7 Atmospheric Features.
- **Task trước trong tiểu mục:** T04-042; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Extract 200 hPa wind.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-043.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Extract 200 hPa wind.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Fixture u/v ở 850/200hPa; shear=sqrt((u200-u850)^2+(v200-v850)^2); pressure Pa→hPa; không dùng field tương lai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-044"></a>
## T04-044 — Extract humidity if available.

- **Trạng thái:** pending.
- **Nguồn:** 4.7 Atmospheric Features; dòng [671](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:671).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.7 Atmospheric Features.
- **Task trước trong tiểu mục:** T04-043; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Extract humidity if available.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-044.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Extract humidity if available.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture u/v ở 850/200hPa; shear=sqrt((u200-u850)^2+(v200-v850)^2); pressure Pa→hPa; không dùng field tương lai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-045"></a>
## T04-045 — Calculate wind shear.

- **Trạng thái:** pending.
- **Nguồn:** 4.7 Atmospheric Features; dòng [672](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:672).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.7 Atmospheric Features.
- **Task trước trong tiểu mục:** T04-044; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Calculate wind shear.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-045.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Calculate wind shear.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Fixture u/v ở 850/200hPa; shear=sqrt((u200-u850)^2+(v200-v850)^2); pressure Pa→hPa; không dùng field tương lai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-046"></a>
## T04-046 — Validate units.

- **Trạng thái:** pending.
- **Nguồn:** 4.7 Atmospheric Features; dòng [673](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:673).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.7 Atmospheric Features.
- **Task trước trong tiểu mục:** T04-045; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Validate units.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-046.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Validate units.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Fixture u/v ở 850/200hPa; shear=sqrt((u200-u850)^2+(v200-v850)^2); pressure Pa→hPa; không dùng field tương lai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-047"></a>
## T04-047 — Cache features.

- **Trạng thái:** pending.
- **Nguồn:** 4.7 Atmospheric Features; dòng [674](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:674).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.7 Atmospheric Features.
- **Task trước trong tiểu mục:** T04-046; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Cache features.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-047.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cache features.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hit/miss/expiry, observation sửa/model đổi và outage; cache key bao gồm input+model revision.
- **Kịch bản tiểu mục:** Fixture u/v ở 850/200hPa; shear=sqrt((u200-u850)^2+(v200-v850)^2); pressure Pa→hPa; không dùng field tương lai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-048"></a>
## T04-048 — Tạo danh sách feature chính thức.

- **Trạng thái:** pending.
- **Nguồn:** 4.8 Feature Schema; dòng [677](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:677).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.8 Feature Schema.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Tạo danh sách feature chính thức.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-048.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo danh sách feature chính thức.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Manifest liệt kê tên/order/dtype/unit/source/missing policy/version; cột mới/thiếu/đổi thứ tự phải được phát hiện trước inference.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-049"></a>
## T04-049 — Đặt dtype.

- **Trạng thái:** pending.
- **Nguồn:** 4.8 Feature Schema; dòng [678](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:678).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.8 Feature Schema.
- **Task trước trong tiểu mục:** T04-048; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Đặt dtype.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-049.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Đặt dtype.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Manifest liệt kê tên/order/dtype/unit/source/missing policy/version; cột mới/thiếu/đổi thứ tự phải được phát hiện trước inference.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-050"></a>
## T04-050 — Đặt đơn vị.

- **Trạng thái:** pending.
- **Nguồn:** 4.8 Feature Schema; dòng [679](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:679).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.8 Feature Schema.
- **Task trước trong tiểu mục:** T04-049; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Đặt đơn vị.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-050.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Đặt đơn vị.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Manifest liệt kê tên/order/dtype/unit/source/missing policy/version; cột mới/thiếu/đổi thứ tự phải được phát hiện trước inference.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-051"></a>
## T04-051 — Đặt mô tả.

- **Trạng thái:** pending.
- **Nguồn:** 4.8 Feature Schema; dòng [680](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:680).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.8 Feature Schema.
- **Task trước trong tiểu mục:** T04-050; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Đặt mô tả.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-051.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Đặt mô tả.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Manifest liệt kê tên/order/dtype/unit/source/missing policy/version; cột mới/thiếu/đổi thứ tự phải được phát hiện trước inference.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-052"></a>
## T04-052 — Đặt nguồn.

- **Trạng thái:** pending.
- **Nguồn:** 4.8 Feature Schema; dòng [681](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:681).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.8 Feature Schema.
- **Task trước trong tiểu mục:** T04-051; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Đặt nguồn.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-052.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Đặt nguồn.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Manifest liệt kê tên/order/dtype/unit/source/missing policy/version; cột mới/thiếu/đổi thứ tự phải được phát hiện trước inference.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-053"></a>
## T04-053 — Đặt missing policy.

- **Trạng thái:** pending.
- **Nguồn:** 4.8 Feature Schema; dòng [682](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:682).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.8 Feature Schema.
- **Task trước trong tiểu mục:** T04-052; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Đặt missing policy.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-053.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Đặt missing policy.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Manifest liệt kê tên/order/dtype/unit/source/missing policy/version; cột mới/thiếu/đổi thứ tự phải được phát hiện trước inference.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t04-054"></a>
## T04-054 — Tạo data dictionary.

- **Trạng thái:** pending.
- **Nguồn:** 4.8 Feature Schema; dòng [683](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:683).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G03; contract/fixture của tiểu mục 4.8 Feature Schema.
- **Task trước trong tiểu mục:** T04-053; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Track sạch, timestamp UTC, dữ liệu môi trường có available_at; yêu cầu riêng: Tạo data dictionary.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/build.py; src/typhoon_vn/features/schema.py; src/typhoon_vn/features/store.py; docs/data-dictionary.md; tests/test_features.py; evidence tại evidence/T04-054.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo data dictionary.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G04, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Manifest liệt kê tên/order/dtype/unit/source/missing policy/version; cột mới/thiếu/đổi thứ tự phải được phát hiện trước inference.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
