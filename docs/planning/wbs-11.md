# G11 — Bất định và cone

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có uncertainty helper; API baseline dùng radius minh họa.
- Đầu vào: Model đã chọn bằng validation; bộ calibration độc lập với final test.
- Gate phụ thuộc: G13, G14.
- Vùng file dự kiến: src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Phân biệt độ phân tán và coverage; cone GeoJSON hợp lệ; không nhận radius minh họa là xác suất đã hiệu chuẩn.

<a id="gate-g11"></a>
## Gate G11

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t11-001"></a>
## T11-001 — Giữ dropout khi inference.

- **Trạng thái:** pending.
- **Nguồn:** 11.1 Monte Carlo Dropout; dòng [847](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:847).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.1 Monte Carlo Dropout.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Giữ dropout khi inference.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Giữ dropout khi inference.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Chỉ bật dropout, giữ các layer khác ở eval; restore mode sau inference; n_samples>=2; không đổi state giữa request.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-002"></a>
## T11-002 — Chạy nhiều sample.

- **Trạng thái:** pending.
- **Nguồn:** 11.1 Monte Carlo Dropout; dòng [848](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:848).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.1 Monte Carlo Dropout.
- **Task trước trong tiểu mục:** T11-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Chạy nhiều sample.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chạy nhiều sample.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Chỉ bật dropout, giữ các layer khác ở eval; restore mode sau inference; n_samples>=2; không đổi state giữa request.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-003"></a>
## T11-003 — Lưu trajectories.

- **Trạng thái:** pending.
- **Nguồn:** 11.1 Monte Carlo Dropout; dòng [849](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:849).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.1 Monte Carlo Dropout.
- **Task trước trong tiểu mục:** T11-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Lưu trajectories.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu trajectories.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Chỉ bật dropout, giữ các layer khác ở eval; restore mode sau inference; n_samples>=2; không đổi state giữa request.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-004"></a>
## T11-004 — Tính mean trajectory.

- **Trạng thái:** pending.
- **Nguồn:** 11.1 Monte Carlo Dropout; dòng [850](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:850).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.1 Monte Carlo Dropout.
- **Task trước trong tiểu mục:** T11-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Tính mean trajectory.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính mean trajectory.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Chỉ bật dropout, giữ các layer khác ở eval; restore mode sau inference; n_samples>=2; không đổi state giữa request.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-005"></a>
## T11-005 — Tính quantile.

- **Trạng thái:** pending.
- **Nguồn:** 11.1 Monte Carlo Dropout; dòng [851](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:851).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.1 Monte Carlo Dropout.
- **Task trước trong tiểu mục:** T11-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Tính quantile.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính quantile.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Chỉ bật dropout, giữ các layer khác ở eval; restore mode sau inference; n_samples>=2; không đổi state giữa request.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-006"></a>
## T11-006 — Tính radius.

- **Trạng thái:** pending.
- **Nguồn:** 11.1 Monte Carlo Dropout; dòng [852](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:852).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.1 Monte Carlo Dropout.
- **Task trước trong tiểu mục:** T11-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Tính radius.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính radius.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Chỉ bật dropout, giữ các layer khác ở eval; restore mode sau inference; n_samples>=2; không đổi state giữa request.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-007"></a>
## T11-007 — Train model seed 1.

- **Trạng thái:** pending.
- **Nguồn:** 11.2 Ensemble; dòng [855](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:855).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.2 Ensemble.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Train model seed 1.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Train model seed 1.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Lưu seed Python/NumPy/Torch/backend; cùng môi trường CPU/seed tái lập; khác seed thành run khác.
- **Kịch bản tiểu mục:** Ít nhất 3 seed độc lập, cùng split và feature contract; lưu member versions; test ensemble thiếu/mismatch member.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-008"></a>
## T11-008 — Train seed 2.

- **Trạng thái:** pending.
- **Nguồn:** 11.2 Ensemble; dòng [856](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:856).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.2 Ensemble.
- **Task trước trong tiểu mục:** T11-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Train seed 2.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Train seed 2.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Lưu seed Python/NumPy/Torch/backend; cùng môi trường CPU/seed tái lập; khác seed thành run khác.
- **Kịch bản tiểu mục:** Ít nhất 3 seed độc lập, cùng split và feature contract; lưu member versions; test ensemble thiếu/mismatch member.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-009"></a>
## T11-009 — Train seed 3.

- **Trạng thái:** pending.
- **Nguồn:** 11.2 Ensemble; dòng [857](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:857).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.2 Ensemble.
- **Task trước trong tiểu mục:** T11-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Train seed 3.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Train seed 3.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Lưu seed Python/NumPy/Torch/backend; cùng môi trường CPU/seed tái lập; khác seed thành run khác.
- **Kịch bản tiểu mục:** Ít nhất 3 seed độc lập, cùng split và feature contract; lưu member versions; test ensemble thiếu/mismatch member.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-010"></a>
## T11-010 — Gom predictions.

- **Trạng thái:** pending.
- **Nguồn:** 11.2 Ensemble; dòng [858](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:858).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.2 Ensemble.
- **Task trước trong tiểu mục:** T11-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Gom predictions.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Gom predictions.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Ít nhất 3 seed độc lập, cùng split và feature contract; lưu member versions; test ensemble thiếu/mismatch member.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-011"></a>
## T11-011 — Tính mean.

- **Trạng thái:** pending.
- **Nguồn:** 11.2 Ensemble; dòng [859](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:859).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.2 Ensemble.
- **Task trước trong tiểu mục:** T11-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Tính mean.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính mean.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Ít nhất 3 seed độc lập, cùng split và feature contract; lưu member versions; test ensemble thiếu/mismatch member.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-012"></a>
## T11-012 — Tính dispersion.

- **Trạng thái:** pending.
- **Nguồn:** 11.2 Ensemble; dòng [860](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:860).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.2 Ensemble.
- **Task trước trong tiểu mục:** T11-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Tính dispersion.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính dispersion.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Ít nhất 3 seed độc lập, cùng split và feature contract; lưu member versions; test ensemble thiếu/mismatch member.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-013"></a>
## T11-013 — Xác định radius theo horizon.

- **Trạng thái:** pending.
- **Nguồn:** 11.3 Cone; dòng [863](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:863).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.3 Cone.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Xác định radius theo horizon.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xác định radius theo horizon.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** GeoJSON thứ tự [lon,lat], ring đóng, hợp lệ qua dateline; coverage đo trên calibration, khác uncertainty minh họa.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-014"></a>
## T11-014 — Tạo polygon.

- **Trạng thái:** pending.
- **Nguồn:** 11.3 Cone; dòng [864](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:864).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.3 Cone.
- **Task trước trong tiểu mục:** T11-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Tạo polygon.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo polygon.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** GeoJSON [lon,lat], ring đóng/topology hợp lệ; dateline có xử lý; coverage thực nghiệm khác radius minh họa.
- **Kịch bản tiểu mục:** GeoJSON thứ tự [lon,lat], ring đóng, hợp lệ qua dateline; coverage đo trên calibration, khác uncertainty minh họa.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-015"></a>
## T11-015 — Kiểm tra polygon hợp lệ.

- **Trạng thái:** pending.
- **Nguồn:** 11.3 Cone; dòng [865](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:865).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.3 Cone.
- **Task trước trong tiểu mục:** T11-014; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Kiểm tra polygon hợp lệ.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra polygon hợp lệ.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** GeoJSON [lon,lat], ring đóng/topology hợp lệ; dateline có xử lý; coverage thực nghiệm khác radius minh họa.
- **Kịch bản tiểu mục:** GeoJSON thứ tự [lon,lat], ring đóng, hợp lệ qua dateline; coverage đo trên calibration, khác uncertainty minh họa.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-016"></a>
## T11-016 — Xuất GeoJSON.

- **Trạng thái:** pending.
- **Nguồn:** 11.3 Cone; dòng [866](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:866).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.3 Cone.
- **Task trước trong tiểu mục:** T11-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Xuất GeoJSON.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xuất GeoJSON.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** GeoJSON [lon,lat], ring đóng/topology hợp lệ; dateline có xử lý; coverage thực nghiệm khác radius minh họa.
- **Kịch bản tiểu mục:** GeoJSON thứ tự [lon,lat], ring đóng, hợp lệ qua dateline; coverage đo trên calibration, khác uncertainty minh họa.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t11-017"></a>
## T11-017 — Hiển thị trên map.

- **Trạng thái:** pending.
- **Nguồn:** 11.3 Cone; dòng [867](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:867).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G13, G14; contract/fixture của tiểu mục 11.3 Cone.
- **Task trước trong tiểu mục:** T11-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model đã chọn bằng validation; bộ calibration độc lập với final test; yêu cầu riêng: Hiển thị trên map.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/uncertainty.py; src/typhoon_vn/inference/service.py; tests/test_uncertainty.py; evidence tại evidence/T11-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Hiển thị trên map.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G11, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** GeoJSON thứ tự [lon,lat], ring đóng, hợp lệ qua dateline; coverage đo trên calibration, khác uncertainty minh họa.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
