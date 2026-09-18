# G16 — Dịch vụ inference

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Vừa viết bản nháp; baseline có, trained path thiếu load_bundle/predict_bundle.
- Đầu vào: Artifact đã kiểm tra, chuỗi fixes có source và thời gian.
- Gate phụ thuộc: G15.
- Vùng file dự kiến: src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Load một lần; shared feature/scaler; output vật lý; fallback có cờ; request đồng thời không đổi state model.

<a id="gate-g16"></a>
## Gate G16

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t16-001"></a>
## T16-001 — Load model một lần.

- **Trạng thái:** pending.
- **Nguồn:** 16.1 Forecaster; dòng [968](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:968).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.1 Forecaster.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Load model một lần.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Load model một lần.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** So tensor training và serving từ cùng chuỗi lịch sử; bundle sai schema/hash phải fail; inference không fit lại scaler.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-002"></a>
## T16-002 — Load scaler.

- **Trạng thái:** pending.
- **Nguồn:** 16.1 Forecaster; dòng [969](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:969).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.1 Forecaster.
- **Task trước trong tiểu mục:** T16-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Load scaler.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Load scaler.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fit train-only; val/test cực trị không đổi stats; save/load giữ order/fill; finite round-trip <=1e-6.
- **Kịch bản tiểu mục:** So tensor training và serving từ cùng chuỗi lịch sử; bundle sai schema/hash phải fail; inference không fit lại scaler.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-003"></a>
## T16-003 — Load feature schema.

- **Trạng thái:** pending.
- **Nguồn:** 16.1 Forecaster; dòng [970](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:970).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.1 Forecaster.
- **Task trước trong tiểu mục:** T16-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Load feature schema.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Load feature schema.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** So tensor training và serving từ cùng chuỗi lịch sử; bundle sai schema/hash phải fail; inference không fit lại scaler.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-004"></a>
## T16-004 — Validate input.

- **Trạng thái:** pending.
- **Nguồn:** 16.1 Forecaster; dòng [971](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:971).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.1 Forecaster.
- **Task trước trong tiểu mục:** T16-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Validate input.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Validate input.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** So tensor training và serving từ cùng chuỗi lịch sử; bundle sai schema/hash phải fail; inference không fit lại scaler.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-005"></a>
## T16-005 — Build features.

- **Trạng thái:** pending.
- **Nguồn:** 16.1 Forecaster; dòng [972](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:972).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.1 Forecaster.
- **Task trước trong tiểu mục:** T16-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Build features.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Build features.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Build/config exit 0; smoke service; secrets/raw/checkpoints ngoài build context trừ artifact được chọn.
- **Kịch bản tiểu mục:** So tensor training và serving từ cùng chuỗi lịch sử; bundle sai schema/hash phải fail; inference không fit lại scaler.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-006"></a>
## T16-006 — Predict.

- **Trạng thái:** pending.
- **Nguồn:** 16.1 Forecaster; dòng [973](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:973).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.1 Forecaster.
- **Task trước trong tiểu mục:** T16-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Predict.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Predict.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** So tensor training và serving từ cùng chuỗi lịch sử; bundle sai schema/hash phải fail; inference không fit lại scaler.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-007"></a>
## T16-007 — Denormalize.

- **Trạng thái:** pending.
- **Nguồn:** 16.1 Forecaster; dòng [974](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:974).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.1 Forecaster.
- **Task trước trong tiểu mục:** T16-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Denormalize.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Denormalize.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** So tensor training và serving từ cùng chuỗi lịch sử; bundle sai schema/hash phải fail; inference không fit lại scaler.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-008"></a>
## T16-008 — Generate uncertainty.

- **Trạng thái:** pending.
- **Nguồn:** 16.1 Forecaster; dòng [975](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:975).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.1 Forecaster.
- **Task trước trong tiểu mục:** T16-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Generate uncertainty.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Generate uncertainty.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** So tensor training và serving từ cùng chuỗi lịch sử; bundle sai schema/hash phải fail; inference không fit lại scaler.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-009"></a>
## T16-009 — Generate impact.

- **Trạng thái:** pending.
- **Nguồn:** 16.1 Forecaster; dòng [976](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:976).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.1 Forecaster.
- **Task trước trong tiểu mục:** T16-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Generate impact.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Generate impact.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** So tensor training và serving từ cùng chuỗi lịch sử; bundle sai schema/hash phải fail; inference không fit lại scaler.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-010"></a>
## T16-010 — Return standardized result.

- **Trạng thái:** pending.
- **Nguồn:** 16.1 Forecaster; dòng [977](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:977).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.1 Forecaster.
- **Task trước trong tiểu mục:** T16-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Return standardized result.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Return standardized result.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** So tensor training và serving từ cùng chuỗi lịch sử; bundle sai schema/hash phải fail; inference không fit lại scaler.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-011"></a>
## T16-011 — Lấy observations gần nhất.

- **Trạng thái:** pending.
- **Nguồn:** 16.2 Rolling Forecast; dòng [980](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:980).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.2 Rolling Forecast.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Lấy observations gần nhất.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lấy observations gần nhất.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** So direct multi-horizon với rolling; không giả target +24 là bước +6; feature môi trường tương lai không được lấy observation thật.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-012"></a>
## T16-012 — Tạo input window.

- **Trạng thái:** pending.
- **Nguồn:** 16.2 Rolling Forecast; dòng [981](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:981).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.2 Rolling Forecast.
- **Task trước trong tiểu mục:** T16-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Tạo input window.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo input window.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Cửa sổ chỉ chứa một storm, input_len đúng; fixture ngắn hơn window không tạo sample; timestamps không đảo hoặc trùng.
- **Kịch bản tiểu mục:** So direct multi-horizon với rolling; không giả target +24 là bước +6; feature môi trường tương lai không được lấy observation thật.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-013"></a>
## T16-013 — Predict bước tiếp.

- **Trạng thái:** pending.
- **Nguồn:** 16.2 Rolling Forecast; dòng [982](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:982).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.2 Rolling Forecast.
- **Task trước trong tiểu mục:** T16-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Predict bước tiếp.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Predict bước tiếp.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** So direct multi-horizon với rolling; không giả target +24 là bước +6; feature môi trường tương lai không được lấy observation thật.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-014"></a>
## T16-014 — Sinh multi-horizon.

- **Trạng thái:** pending.
- **Nguồn:** 16.2 Rolling Forecast; dòng [983](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:983).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.2 Rolling Forecast.
- **Task trước trong tiểu mục:** T16-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Sinh multi-horizon.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Sinh multi-horizon.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** So direct multi-horizon với rolling; không giả target +24 là bước +6; feature môi trường tương lai không được lấy observation thật.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-015"></a>
## T16-015 — Kiểm soát autoregressive error.

- **Trạng thái:** pending.
- **Nguồn:** 16.2 Rolling Forecast; dòng [984](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:984).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.2 Rolling Forecast.
- **Task trước trong tiểu mục:** T16-014; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Kiểm soát autoregressive error.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm soát autoregressive error.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** So direct multi-horizon với rolling; không giả target +24 là bước +6; feature môi trường tương lai không được lấy observation thật.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-016"></a>
## T16-016 — Validate output.

- **Trạng thái:** pending.
- **Nguồn:** 16.2 Rolling Forecast; dòng [985](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:985).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.2 Rolling Forecast.
- **Task trước trong tiểu mục:** T16-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Validate output.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Validate output.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** So direct multi-horizon với rolling; không giả target +24 là bước +6; feature môi trường tương lai không được lấy observation thật.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-017"></a>
## T16-017 — Phát hiện thiếu environmental feature.

- **Trạng thái:** pending.
- **Nguồn:** 16.3 Fallback; dòng [988](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:988).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.3 Fallback.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Phát hiện thiếu environmental feature.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Phát hiện thiếu environmental feature.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Missing SST/shear dùng giá trị fit train đã lưu; response có fallback_used và missing_features; từ chối nếu feature bắt buộc không khôi phục.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-018"></a>
## T16-018 — Dùng fallback hợp lệ.

- **Trạng thái:** pending.
- **Nguồn:** 16.3 Fallback; dòng [989](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:989).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.3 Fallback.
- **Task trước trong tiểu mục:** T16-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Dùng fallback hợp lệ.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Dùng fallback hợp lệ.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Missing SST/shear dùng giá trị fit train đã lưu; response có fallback_used và missing_features; từ chối nếu feature bắt buộc không khôi phục.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-019"></a>
## T16-019 — Gắn cờ `fallback_used`.

- **Trạng thái:** pending.
- **Nguồn:** 16.3 Fallback; dòng [990](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:990).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.3 Fallback.
- **Task trước trong tiểu mục:** T16-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Gắn cờ `fallback_used`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Gắn cờ `fallback_used`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Missing SST/shear dùng giá trị fit train đã lưu; response có fallback_used và missing_features; từ chối nếu feature bắt buộc không khôi phục.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t16-020"></a>
## T16-020 — Log fallback.

- **Trạng thái:** pending.
- **Nguồn:** 16.3 Fallback; dòng [991](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:991).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G15; contract/fixture của tiểu mục 16.3 Fallback.
- **Task trước trong tiểu mục:** T16-019; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Artifact đã kiểm tra, chuỗi fixes có source và thời gian; yêu cầu riêng: Log fallback.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/inference/service.py; src/typhoon_vn/inference/artifacts.py; tests/test_inference.py; evidence tại evidence/T16-020.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Log fallback.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G16, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Missing SST/shear dùng giá trị fit train đã lưu; response có fallback_used và missing_features; từ chối nếu feature bắt buộc không khôi phục.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
