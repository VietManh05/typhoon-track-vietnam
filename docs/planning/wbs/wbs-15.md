# G15 — Model registry và promotion

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Chưa có registry/bundle loader; code inference đang tham chiếu module thiếu.
- Đầu vào: Model/feature/scaler/config/checksum, validation/calibration metrics và dataset version.
- Gate phụ thuộc: G11, G14.
- Vùng file dự kiến: src/typhoon_vn/training/registry.py; src/typhoon_vn/training/pipeline.py; tests/test_registry.py; docs/model-registry.md.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Bundle có version và checksum; promotion có gate; artifact lỗi bị từ chối; rollback trở về cùng model/scaler/schema.

<a id="gate-g15"></a>
## Gate G15

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t15-001"></a>
## T15-001 — Cài MLflow.

- **Trạng thái:** pending.
- **Nguồn:** 15. MODEL REGISTRY; dòng [951](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:951).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G11, G14; contract/fixture của tiểu mục 15. MODEL REGISTRY.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Model/feature/scaler/config/checksum, validation/calibration metrics và dataset version; yêu cầu riêng: Cài MLflow.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/registry.py; src/typhoon_vn/training/pipeline.py; tests/test_registry.py; docs/model-registry.md; evidence tại evidence/T15-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cài MLflow.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G15, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Bundle có version và checksum; promotion có gate; artifact lỗi bị từ chối; rollback trở về cùng model/scaler/schema.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t15-002"></a>
## T15-002 — Log model.

- **Trạng thái:** pending.
- **Nguồn:** 15. MODEL REGISTRY; dòng [952](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:952).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G11, G14; contract/fixture của tiểu mục 15. MODEL REGISTRY.
- **Task trước trong tiểu mục:** T15-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model/feature/scaler/config/checksum, validation/calibration metrics và dataset version; yêu cầu riêng: Log model.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/registry.py; src/typhoon_vn/training/pipeline.py; tests/test_registry.py; docs/model-registry.md; evidence tại evidence/T15-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Log model.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G15, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Bundle có version và checksum; promotion có gate; artifact lỗi bị từ chối; rollback trở về cùng model/scaler/schema.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t15-003"></a>
## T15-003 — Log metrics.

- **Trạng thái:** pending.
- **Nguồn:** 15. MODEL REGISTRY; dòng [953](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:953).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G11, G14; contract/fixture của tiểu mục 15. MODEL REGISTRY.
- **Task trước trong tiểu mục:** T15-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model/feature/scaler/config/checksum, validation/calibration metrics và dataset version; yêu cầu riêng: Log metrics.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/registry.py; src/typhoon_vn/training/pipeline.py; tests/test_registry.py; docs/model-registry.md; evidence tại evidence/T15-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Log metrics.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G15, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Bundle có version và checksum; promotion có gate; artifact lỗi bị từ chối; rollback trở về cùng model/scaler/schema.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t15-004"></a>
## T15-004 — Log params.

- **Trạng thái:** pending.
- **Nguồn:** 15. MODEL REGISTRY; dòng [954](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:954).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G11, G14; contract/fixture của tiểu mục 15. MODEL REGISTRY.
- **Task trước trong tiểu mục:** T15-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model/feature/scaler/config/checksum, validation/calibration metrics và dataset version; yêu cầu riêng: Log params.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/registry.py; src/typhoon_vn/training/pipeline.py; tests/test_registry.py; docs/model-registry.md; evidence tại evidence/T15-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Log params.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G15, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Bundle có version và checksum; promotion có gate; artifact lỗi bị từ chối; rollback trở về cùng model/scaler/schema.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t15-005"></a>
## T15-005 — Log dataset version.

- **Trạng thái:** pending.
- **Nguồn:** 15. MODEL REGISTRY; dòng [955](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:955).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G11, G14; contract/fixture của tiểu mục 15. MODEL REGISTRY.
- **Task trước trong tiểu mục:** T15-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model/feature/scaler/config/checksum, validation/calibration metrics và dataset version; yêu cầu riêng: Log dataset version.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/registry.py; src/typhoon_vn/training/pipeline.py; tests/test_registry.py; docs/model-registry.md; evidence tại evidence/T15-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Log dataset version.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G15, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Bundle có version và checksum; promotion có gate; artifact lỗi bị từ chối; rollback trở về cùng model/scaler/schema.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t15-006"></a>
## T15-006 — Tạo model registry.

- **Trạng thái:** pending.
- **Nguồn:** 15. MODEL REGISTRY; dòng [956](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:956).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G11, G14; contract/fixture của tiểu mục 15. MODEL REGISTRY.
- **Task trước trong tiểu mục:** T15-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model/feature/scaler/config/checksum, validation/calibration metrics và dataset version; yêu cầu riêng: Tạo model registry.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/registry.py; src/typhoon_vn/training/pipeline.py; tests/test_registry.py; docs/model-registry.md; evidence tại evidence/T15-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo model registry.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G15, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Bundle có version và checksum; promotion có gate; artifact lỗi bị từ chối; rollback trở về cùng model/scaler/schema.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t15-007"></a>
## T15-007 — Đặt version.

- **Trạng thái:** pending.
- **Nguồn:** 15. MODEL REGISTRY; dòng [957](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:957).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G11, G14; contract/fixture của tiểu mục 15. MODEL REGISTRY.
- **Task trước trong tiểu mục:** T15-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model/feature/scaler/config/checksum, validation/calibration metrics và dataset version; yêu cầu riêng: Đặt version.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/registry.py; src/typhoon_vn/training/pipeline.py; tests/test_registry.py; docs/model-registry.md; evidence tại evidence/T15-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Đặt version.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G15, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Bundle có version và checksum; promotion có gate; artifact lỗi bị từ chối; rollback trở về cùng model/scaler/schema.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t15-008"></a>
## T15-008 — Staging.

- **Trạng thái:** pending.
- **Nguồn:** 15. MODEL REGISTRY; dòng [958](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:958).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G11, G14; contract/fixture của tiểu mục 15. MODEL REGISTRY.
- **Task trước trong tiểu mục:** T15-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model/feature/scaler/config/checksum, validation/calibration metrics và dataset version; yêu cầu riêng: Staging.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/registry.py; src/typhoon_vn/training/pipeline.py; tests/test_registry.py; docs/model-registry.md; evidence tại evidence/T15-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Staging.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G15, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Bundle có version và checksum; promotion có gate; artifact lỗi bị từ chối; rollback trở về cùng model/scaler/schema.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t15-009"></a>
## T15-009 — Production.

- **Trạng thái:** pending.
- **Nguồn:** 15. MODEL REGISTRY; dòng [959](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:959).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G11, G14; contract/fixture của tiểu mục 15. MODEL REGISTRY.
- **Task trước trong tiểu mục:** T15-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model/feature/scaler/config/checksum, validation/calibration metrics và dataset version; yêu cầu riêng: Production.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/registry.py; src/typhoon_vn/training/pipeline.py; tests/test_registry.py; docs/model-registry.md; evidence tại evidence/T15-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Production.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G15, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Bundle có version và checksum; promotion có gate; artifact lỗi bị từ chối; rollback trở về cùng model/scaler/schema.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t15-010"></a>
## T15-010 — Quy tắc promote.

- **Trạng thái:** pending.
- **Nguồn:** 15. MODEL REGISTRY; dòng [960](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:960).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G11, G14; contract/fixture của tiểu mục 15. MODEL REGISTRY.
- **Task trước trong tiểu mục:** T15-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model/feature/scaler/config/checksum, validation/calibration metrics và dataset version; yêu cầu riêng: Quy tắc promote.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/registry.py; src/typhoon_vn/training/pipeline.py; tests/test_registry.py; docs/model-registry.md; evidence tại evidence/T15-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Quy tắc promote.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G15, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Bundle có version và checksum; promotion có gate; artifact lỗi bị từ chối; rollback trở về cùng model/scaler/schema.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t15-011"></a>
## T15-011 — Rollback model.

- **Trạng thái:** pending.
- **Nguồn:** 15. MODEL REGISTRY; dòng [961](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:961).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G11, G14; contract/fixture của tiểu mục 15. MODEL REGISTRY.
- **Task trước trong tiểu mục:** T15-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Model/feature/scaler/config/checksum, validation/calibration metrics và dataset version; yêu cầu riêng: Rollback model.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/registry.py; src/typhoon_vn/training/pipeline.py; tests/test_registry.py; docs/model-registry.md; evidence tại evidence/T15-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Rollback model.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G15, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Bundle có version và checksum; promotion có gate; artifact lỗi bị từ chối; rollback trở về cùng model/scaler/schema.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
