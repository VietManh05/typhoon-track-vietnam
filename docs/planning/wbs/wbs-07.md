# G07 — Baseline cổ điển

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có persistence và damped-persistence mang tên CLIPER; chưa chứng minh CLIPER nghiệp vụ.
- Đầu vào: Cùng split, cùng issue_time/horizon và tọa độ vật lý.
- Gate phụ thuộc: G06.
- Vùng file dự kiến: src/typhoon_vn/models/baselines.py; tests/test_baselines.py; docs/baselines.md.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Persistence có xử lý wrap longitude; CLIPER thật cần phương pháp/dữ liệu kiểm chứng; heuristic phải đặt tên trung thực.

<a id="gate-g07"></a>
## Gate G07

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t07-001"></a>
## T07-001 — Implement persistence.

- **Trạng thái:** pending.
- **Nguồn:** 7.1 Persistence; dòng [744](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:744).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G06; contract/fixture của tiểu mục 7.1 Persistence.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Cùng split, cùng issue_time/horizon và tọa độ vật lý; yêu cầu riêng: Implement persistence.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/baselines.py; tests/test_baselines.py; docs/baselines.md; evidence tại evidence/T07-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Implement persistence.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G07, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Bão đứng yên, đi thẳng và qua kinh tuyến 180; so điểm đích tính độc lập theo elapsed time; cùng horizon với ML.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t07-002"></a>
## T07-002 — Generate 6h.

- **Trạng thái:** pending.
- **Nguồn:** 7.1 Persistence; dòng [745](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:745).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G06; contract/fixture của tiểu mục 7.1 Persistence.
- **Task trước trong tiểu mục:** T07-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cùng split, cùng issue_time/horizon và tọa độ vật lý; yêu cầu riêng: Generate 6h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/baselines.py; tests/test_baselines.py; docs/baselines.md; evidence tại evidence/T07-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Generate 6h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G07, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Bão đứng yên, đi thẳng và qua kinh tuyến 180; so điểm đích tính độc lập theo elapsed time; cùng horizon với ML.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t07-003"></a>
## T07-003 — Generate 12h.

- **Trạng thái:** pending.
- **Nguồn:** 7.1 Persistence; dòng [746](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:746).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G06; contract/fixture của tiểu mục 7.1 Persistence.
- **Task trước trong tiểu mục:** T07-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cùng split, cùng issue_time/horizon và tọa độ vật lý; yêu cầu riêng: Generate 12h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/baselines.py; tests/test_baselines.py; docs/baselines.md; evidence tại evidence/T07-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Generate 12h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G07, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Bão đứng yên, đi thẳng và qua kinh tuyến 180; so điểm đích tính độc lập theo elapsed time; cùng horizon với ML.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t07-004"></a>
## T07-004 — Generate 24h.

- **Trạng thái:** pending.
- **Nguồn:** 7.1 Persistence; dòng [747](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:747).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G06; contract/fixture của tiểu mục 7.1 Persistence.
- **Task trước trong tiểu mục:** T07-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cùng split, cùng issue_time/horizon và tọa độ vật lý; yêu cầu riêng: Generate 24h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/baselines.py; tests/test_baselines.py; docs/baselines.md; evidence tại evidence/T07-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Generate 24h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G07, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Bão đứng yên, đi thẳng và qua kinh tuyến 180; so điểm đích tính độc lập theo elapsed time; cùng horizon với ML.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t07-005"></a>
## T07-005 — Generate 48h.

- **Trạng thái:** pending.
- **Nguồn:** 7.1 Persistence; dòng [748](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:748).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G06; contract/fixture của tiểu mục 7.1 Persistence.
- **Task trước trong tiểu mục:** T07-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cùng split, cùng issue_time/horizon và tọa độ vật lý; yêu cầu riêng: Generate 48h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/baselines.py; tests/test_baselines.py; docs/baselines.md; evidence tại evidence/T07-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Generate 48h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G07, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Bão đứng yên, đi thẳng và qua kinh tuyến 180; so điểm đích tính độc lập theo elapsed time; cùng horizon với ML.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t07-006"></a>
## T07-006 — Generate 72h.

- **Trạng thái:** pending.
- **Nguồn:** 7.1 Persistence; dòng [749](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:749).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G06; contract/fixture của tiểu mục 7.1 Persistence.
- **Task trước trong tiểu mục:** T07-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cùng split, cùng issue_time/horizon và tọa độ vật lý; yêu cầu riêng: Generate 72h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/baselines.py; tests/test_baselines.py; docs/baselines.md; evidence tại evidence/T07-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Generate 72h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G07, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Bão đứng yên, đi thẳng và qua kinh tuyến 180; so điểm đích tính độc lập theo elapsed time; cùng horizon với ML.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t07-007"></a>
## T07-007 — Evaluate.

- **Trạng thái:** pending.
- **Nguồn:** 7.1 Persistence; dòng [750](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:750).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G06; contract/fixture của tiểu mục 7.1 Persistence.
- **Task trước trong tiểu mục:** T07-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cùng split, cùng issue_time/horizon và tọa độ vật lý; yêu cầu riêng: Evaluate.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/baselines.py; tests/test_baselines.py; docs/baselines.md; evidence tại evidence/T07-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Evaluate.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G07, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Bão đứng yên, đi thẳng và qua kinh tuyến 180; so điểm đích tính độc lập theo elapsed time; cùng horizon với ML.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t07-008"></a>
## T07-008 — Xác định dữ liệu/phương pháp phù hợp.

- **Trạng thái:** pending.
- **Nguồn:** 7.2 CLIPER; dòng [753](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:753).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G06; contract/fixture của tiểu mục 7.2 CLIPER.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Cùng split, cùng issue_time/horizon và tọa độ vật lý; yêu cầu riêng: Xác định dữ liệu/phương pháp phù hợp.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/baselines.py; tests/test_baselines.py; docs/baselines.md; evidence tại evidence/T07-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xác định dữ liệu/phương pháp phù hợp.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G07, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Phân biệt CLIPER có climatology fit trên train và damped persistence heuristic; không mô tả heuristic là CLIPER đã kiểm chứng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t07-009"></a>
## T07-009 — Implement baseline.

- **Trạng thái:** pending.
- **Nguồn:** 7.2 CLIPER; dòng [754](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:754).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G06; contract/fixture của tiểu mục 7.2 CLIPER.
- **Task trước trong tiểu mục:** T07-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cùng split, cùng issue_time/horizon và tọa độ vật lý; yêu cầu riêng: Implement baseline.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/baselines.py; tests/test_baselines.py; docs/baselines.md; evidence tại evidence/T07-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Implement baseline.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G07, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Phân biệt CLIPER có climatology fit trên train và damped persistence heuristic; không mô tả heuristic là CLIPER đã kiểm chứng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t07-010"></a>
## T07-010 — Generate forecasts.

- **Trạng thái:** pending.
- **Nguồn:** 7.2 CLIPER; dòng [755](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:755).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G06; contract/fixture của tiểu mục 7.2 CLIPER.
- **Task trước trong tiểu mục:** T07-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cùng split, cùng issue_time/horizon và tọa độ vật lý; yêu cầu riêng: Generate forecasts.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/baselines.py; tests/test_baselines.py; docs/baselines.md; evidence tại evidence/T07-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Generate forecasts.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G07, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Phân biệt CLIPER có climatology fit trên train và damped persistence heuristic; không mô tả heuristic là CLIPER đã kiểm chứng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t07-011"></a>
## T07-011 — Evaluate.

- **Trạng thái:** pending.
- **Nguồn:** 7.2 CLIPER; dòng [756](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:756).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G06; contract/fixture của tiểu mục 7.2 CLIPER.
- **Task trước trong tiểu mục:** T07-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cùng split, cùng issue_time/horizon và tọa độ vật lý; yêu cầu riêng: Evaluate.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/baselines.py; tests/test_baselines.py; docs/baselines.md; evidence tại evidence/T07-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Evaluate.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G07, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Phân biệt CLIPER có climatology fit trên train và damped persistence heuristic; không mô tả heuristic là CLIPER đã kiểm chứng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t07-012"></a>
## T07-012 — Save metrics.

- **Trạng thái:** pending.
- **Nguồn:** 7.2 CLIPER; dòng [757](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:757).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G06; contract/fixture của tiểu mục 7.2 CLIPER.
- **Task trước trong tiểu mục:** T07-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cùng split, cùng issue_time/horizon và tọa độ vật lý; yêu cầu riêng: Save metrics.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/baselines.py; tests/test_baselines.py; docs/baselines.md; evidence tại evidence/T07-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Save metrics.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G07, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Phân biệt CLIPER có climatology fit trên train và damped persistence heuristic; không mô tả heuristic là CLIPER đã kiểm chứng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
