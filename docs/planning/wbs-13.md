# G13 — Đánh giá và backtest

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có metrics/backtest; chưa xác minh giá trị chuẩn và báo cáo dữ liệu thật.
- Đầu vào: Checkpoint, split IDs, targets vật lý, predictions có issue_time.
- Gate phụ thuộc: G07, G12.
- Vùng file dự kiến: src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Metric km theo 6/12/24/48/72h; baseline cùng mẫu; storms giữ lại; không dùng final test để tune.

<a id="gate-g13"></a>
## Gate G13

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t13-001"></a>
## T13-001 — Haversine prediction vs actual.

- **Trạng thái:** pending.
- **Nguồn:** 13.1 Track Error; dòng [898](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:898).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.1 Track Error.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Haversine prediction vs actual.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Haversine prediction vs actual.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Điểm trùng cho 0 km; cặp điểm chuẩn khớp dung sai; wrap longitude không tạo khoảng cách vòng trái đất.
- **Kịch bản tiểu mục:** Prediction=actual cho 0 km; tọa độ tham chiếu cho khoảng cách đã biết; không tính mean trên mảng rỗng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-002"></a>
## T13-002 — Tính 6h.

- **Trạng thái:** pending.
- **Nguồn:** 13.1 Track Error; dòng [899](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:899).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.1 Track Error.
- **Task trước trong tiểu mục:** T13-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Tính 6h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính 6h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Prediction=actual cho 0 km; tọa độ tham chiếu cho khoảng cách đã biết; không tính mean trên mảng rỗng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-003"></a>
## T13-003 — Tính 12h.

- **Trạng thái:** pending.
- **Nguồn:** 13.1 Track Error; dòng [900](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:900).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.1 Track Error.
- **Task trước trong tiểu mục:** T13-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Tính 12h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính 12h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Prediction=actual cho 0 km; tọa độ tham chiếu cho khoảng cách đã biết; không tính mean trên mảng rỗng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-004"></a>
## T13-004 — Tính 24h.

- **Trạng thái:** pending.
- **Nguồn:** 13.1 Track Error; dòng [901](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:901).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.1 Track Error.
- **Task trước trong tiểu mục:** T13-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Tính 24h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính 24h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Prediction=actual cho 0 km; tọa độ tham chiếu cho khoảng cách đã biết; không tính mean trên mảng rỗng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-005"></a>
## T13-005 — Tính 48h.

- **Trạng thái:** pending.
- **Nguồn:** 13.1 Track Error; dòng [902](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:902).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.1 Track Error.
- **Task trước trong tiểu mục:** T13-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Tính 48h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính 48h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Prediction=actual cho 0 km; tọa độ tham chiếu cho khoảng cách đã biết; không tính mean trên mảng rỗng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-006"></a>
## T13-006 — Tính 72h.

- **Trạng thái:** pending.
- **Nguồn:** 13.1 Track Error; dòng [903](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:903).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.1 Track Error.
- **Task trước trong tiểu mục:** T13-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Tính 72h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính 72h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Prediction=actual cho 0 km; tọa độ tham chiếu cho khoảng cách đã biết; không tính mean trên mảng rỗng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-007"></a>
## T13-007 — Mean.

- **Trạng thái:** pending.
- **Nguồn:** 13.1 Track Error; dòng [904](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:904).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.1 Track Error.
- **Task trước trong tiểu mục:** T13-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Mean.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Mean.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Prediction=actual cho 0 km; tọa độ tham chiếu cho khoảng cách đã biết; không tính mean trên mảng rỗng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-008"></a>
## T13-008 — Median.

- **Trạng thái:** pending.
- **Nguồn:** 13.1 Track Error; dòng [905](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:905).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.1 Track Error.
- **Task trước trong tiểu mục:** T13-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Median.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Median.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Prediction=actual cho 0 km; tọa độ tham chiếu cho khoảng cách đã biết; không tính mean trên mảng rỗng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-009"></a>
## T13-009 — RMSE/percentile nếu phù hợp.

- **Trạng thái:** pending.
- **Nguồn:** 13.1 Track Error; dòng [906](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:906).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.1 Track Error.
- **Task trước trong tiểu mục:** T13-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: RMSE/percentile nếu phù hợp.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “RMSE/percentile nếu phù hợp.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Prediction=actual cho 0 km; tọa độ tham chiếu cho khoảng cách đã biết; không tính mean trên mảng rỗng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-010"></a>
## T13-010 — Xác định reference track.

- **Trạng thái:** pending.
- **Nguồn:** 13.2 Along/Cross Track; dòng [909](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:909).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.2 Along/Cross Track.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Xác định reference track.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xác định reference track.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Đường chuẩn hướng bắc/đông; sai lệch dọc/ngang biết dấu; xử lý actual đứng yên không tạo NaN.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-011"></a>
## T13-011 — Tính along-track error.

- **Trạng thái:** pending.
- **Nguồn:** 13.2 Along/Cross Track; dòng [910](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:910).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.2 Along/Cross Track.
- **Task trước trong tiểu mục:** T13-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Tính along-track error.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính along-track error.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Đường chuẩn hướng bắc/đông; sai lệch dọc/ngang biết dấu; xử lý actual đứng yên không tạo NaN.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-012"></a>
## T13-012 — Tính cross-track error.

- **Trạng thái:** pending.
- **Nguồn:** 13.2 Along/Cross Track; dòng [911](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:911).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.2 Along/Cross Track.
- **Task trước trong tiểu mục:** T13-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Tính cross-track error.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính cross-track error.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Đường chuẩn hướng bắc/đông; sai lệch dọc/ngang biết dấu; xử lý actual đứng yên không tạo NaN.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-013"></a>
## T13-013 — Kiểm tra đơn vị km.

- **Trạng thái:** pending.
- **Nguồn:** 13.2 Along/Cross Track; dòng [912](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:912).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.2 Along/Cross Track.
- **Task trước trong tiểu mục:** T13-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Kiểm tra đơn vị km.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra đơn vị km.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Đường chuẩn hướng bắc/đông; sai lệch dọc/ngang biết dấu; xử lý actual đứng yên không tạo NaN.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-014"></a>
## T13-014 — MAE wind.

- **Trạng thái:** pending.
- **Nguồn:** 13.3 Intensity; dòng [915](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:915).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.3 Intensity.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: MAE wind.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “MAE wind.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Dùng mask nhãn thật; báo support từng lớp, macro-F1 và MAE theo đơn vị; không tính unknown như nhãn đúng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-015"></a>
## T13-015 — MAE pressure.

- **Trạng thái:** pending.
- **Nguồn:** 13.3 Intensity; dòng [916](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:916).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.3 Intensity.
- **Task trước trong tiểu mục:** T13-014; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: MAE pressure.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “MAE pressure.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Dùng mask nhãn thật; báo support từng lớp, macro-F1 và MAE theo đơn vị; không tính unknown như nhãn đúng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-016"></a>
## T13-016 — Accuracy/F1 category nếu có nhãn.

- **Trạng thái:** pending.
- **Nguồn:** 13.3 Intensity; dòng [917](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:917).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.3 Intensity.
- **Task trước trong tiểu mục:** T13-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Accuracy/F1 category nếu có nhãn.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Accuracy/F1 category nếu có nhãn.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Dùng mask nhãn thật; báo support từng lớp, macro-F1 và MAE theo đơn vị; không tính unknown như nhãn đúng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-017"></a>
## T13-017 — Chọn storms test.

- **Trạng thái:** pending.
- **Nguồn:** 13.4 Backtest; dòng [920](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:920).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.4 Backtest.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Chọn storms test.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chọn storms test.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Mọi issue_time chỉ dùng lịch sử đến thời điểm đó; giữ ID/dataset/checkpoint; Damrey/Molave/Noru/Yagi cần dữ liệu thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-018"></a>
## T13-018 — Không train bằng test storms.

- **Trạng thái:** pending.
- **Nguồn:** 13.4 Backtest; dòng [921](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:921).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.4 Backtest.
- **Task trước trong tiểu mục:** T13-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Không train bằng test storms.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Không train bằng test storms.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Mọi issue_time chỉ dùng lịch sử đến thời điểm đó; giữ ID/dataset/checkpoint; Damrey/Molave/Noru/Yagi cần dữ liệu thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-019"></a>
## T13-019 — Chạy forecast từng mốc.

- **Trạng thái:** pending.
- **Nguồn:** 13.4 Backtest; dòng [922](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:922).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.4 Backtest.
- **Task trước trong tiểu mục:** T13-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Chạy forecast từng mốc.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chạy forecast từng mốc.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mọi issue_time chỉ dùng lịch sử đến thời điểm đó; giữ ID/dataset/checkpoint; Damrey/Molave/Noru/Yagi cần dữ liệu thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-020"></a>
## T13-020 — So actual/predicted.

- **Trạng thái:** pending.
- **Nguồn:** 13.4 Backtest; dòng [923](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:923).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.4 Backtest.
- **Task trước trong tiểu mục:** T13-019; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: So actual/predicted.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-020.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “So actual/predicted.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mọi issue_time chỉ dùng lịch sử đến thời điểm đó; giữ ID/dataset/checkpoint; Damrey/Molave/Noru/Yagi cần dữ liệu thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-021"></a>
## T13-021 — Sinh biểu đồ.

- **Trạng thái:** pending.
- **Nguồn:** 13.4 Backtest; dòng [924](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:924).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.4 Backtest.
- **Task trước trong tiểu mục:** T13-020; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Sinh biểu đồ.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-021.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Sinh biểu đồ.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mọi issue_time chỉ dùng lịch sử đến thời điểm đó; giữ ID/dataset/checkpoint; Damrey/Molave/Noru/Yagi cần dữ liệu thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-022"></a>
## T13-022 — Tạo bảng metric.

- **Trạng thái:** pending.
- **Nguồn:** 13.4 Backtest; dòng [925](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:925).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.4 Backtest.
- **Task trước trong tiểu mục:** T13-021; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Tạo bảng metric.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-022.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo bảng metric.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Mọi issue_time chỉ dùng lịch sử đến thời điểm đó; giữ ID/dataset/checkpoint; Damrey/Molave/Noru/Yagi cần dữ liệu thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-023"></a>
## T13-023 — Phân tích case tốt.

- **Trạng thái:** pending.
- **Nguồn:** 13.4 Backtest; dòng [926](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:926).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.4 Backtest.
- **Task trước trong tiểu mục:** T13-022; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Phân tích case tốt.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-023.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Phân tích case tốt.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mọi issue_time chỉ dùng lịch sử đến thời điểm đó; giữ ID/dataset/checkpoint; Damrey/Molave/Noru/Yagi cần dữ liệu thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t13-024"></a>
## T13-024 — Phân tích case xấu.

- **Trạng thái:** pending.
- **Nguồn:** 13.4 Backtest; dòng [927](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:927).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G07, G12; contract/fixture của tiểu mục 13.4 Backtest.
- **Task trước trong tiểu mục:** T13-023; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Checkpoint, split IDs, targets vật lý, predictions có issue_time; yêu cầu riêng: Phân tích case xấu.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/evaluation/metrics.py; src/typhoon_vn/evaluation/backtest.py; tests/test_evaluation.py; reports/evaluation/; evidence tại evidence/T13-024.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Phân tích case xấu.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G13, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mọi issue_time chỉ dùng lịch sử đến thời điểm đó; giữ ID/dataset/checkpoint; Damrey/Molave/Noru/Yagi cần dữ liệu thực.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
