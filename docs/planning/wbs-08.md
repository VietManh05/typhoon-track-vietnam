# G08 — LSTM cơ sở

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có model và test cũ; chưa chạy lại.
- Đầu vào: Tensor contract, feature schema, target schema và vocabulary cố định.
- Gate phụ thuộc: G05, G06.
- Vùng file dự kiến: src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Forward B×H×2; logits đúng số lớp; gradients hữu hạn; save/load giữ kết quả; batch/sequence linh hoạt.

<a id="gate-g08"></a>
## Gate G08

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t08-001"></a>
## T08-001 — Tạo BaseModel.

- **Trạng thái:** pending.
- **Nguồn:** 8.1 Architecture; dòng [766](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:766).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.1 Architecture.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Tạo BaseModel.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo BaseModel.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Input B×T×F với B=1/4 và T=4/6/8; cấu hình sai bị báo lỗi rõ; không hardcode kích thước batch.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-002"></a>
## T08-002 — Xác định input size.

- **Trạng thái:** pending.
- **Nguồn:** 8.1 Architecture; dòng [767](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:767).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.1 Architecture.
- **Task trước trong tiểu mục:** T08-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Xác định input size.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xác định input size.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Input B×T×F với B=1/4 và T=4/6/8; cấu hình sai bị báo lỗi rõ; không hardcode kích thước batch.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-003"></a>
## T08-003 — Xác định hidden size.

- **Trạng thái:** pending.
- **Nguồn:** 8.1 Architecture; dòng [768](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:768).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.1 Architecture.
- **Task trước trong tiểu mục:** T08-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Xác định hidden size.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xác định hidden size.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Input B×T×F với B=1/4 và T=4/6/8; cấu hình sai bị báo lỗi rõ; không hardcode kích thước batch.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-004"></a>
## T08-004 — Xác định number of layers.

- **Trạng thái:** pending.
- **Nguồn:** 8.1 Architecture; dòng [769](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:769).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.1 Architecture.
- **Task trước trong tiểu mục:** T08-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Xác định number of layers.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xác định number of layers.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Input B×T×F với B=1/4 và T=4/6/8; cấu hình sai bị báo lỗi rõ; không hardcode kích thước batch.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-005"></a>
## T08-005 — Xác định dropout.

- **Trạng thái:** pending.
- **Nguồn:** 8.1 Architecture; dòng [770](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:770).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.1 Architecture.
- **Task trước trong tiểu mục:** T08-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Xác định dropout.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xác định dropout.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Input B×T×F với B=1/4 và T=4/6/8; cấu hình sai bị báo lỗi rõ; không hardcode kích thước batch.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-006"></a>
## T08-006 — Tạo LSTM.

- **Trạng thái:** pending.
- **Nguồn:** 8.1 Architecture; dòng [771](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:771).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.1 Architecture.
- **Task trước trong tiểu mục:** T08-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Tạo LSTM.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo LSTM.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Input B×T×F với B=1/4 và T=4/6/8; cấu hình sai bị báo lỗi rõ; không hardcode kích thước batch.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-007"></a>
## T08-007 — Tạo output head.

- **Trạng thái:** pending.
- **Nguồn:** 8.1 Architecture; dòng [772](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:772).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.1 Architecture.
- **Task trước trong tiểu mục:** T08-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Tạo output head.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo output head.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Input B×T×F với B=1/4 và T=4/6/8; cấu hình sai bị báo lỗi rõ; không hardcode kích thước batch.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-008"></a>
## T08-008 — Viết forward.

- **Trạng thái:** pending.
- **Nguồn:** 8.1 Architecture; dòng [773](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:773).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.1 Architecture.
- **Task trước trong tiểu mục:** T08-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Viết forward.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Viết forward.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Input B×T×F với B=1/4 và T=4/6/8; cấu hình sai bị báo lỗi rõ; không hardcode kích thước batch.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-009"></a>
## T08-009 — Kiểm tra tensor shape.

- **Trạng thái:** pending.
- **Nguồn:** 8.1 Architecture; dòng [774](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:774).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.1 Architecture.
- **Task trước trong tiểu mục:** T08-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Kiểm tra tensor shape.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra tensor shape.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test B=1/4, T=4/6/8; shape/dtype đúng; thay padding không đổi output hợp lệ; không qua storm boundary.
- **Kịch bản tiểu mục:** Input B×T×F với B=1/4 và T=4/6/8; cấu hình sai bị báo lỗi rõ; không hardcode kích thước batch.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-010"></a>
## T08-010 — Output 6h.

- **Trạng thái:** pending.
- **Nguồn:** 8.2 Output; dòng [777](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:777).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.2 Output.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Output 6h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Output 6h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Output B×5×2 gắn đúng thứ tự horizon; kiểm tra đơn vị tọa độ và denormalization trong pipeline.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-011"></a>
## T08-011 — Output 12h.

- **Trạng thái:** pending.
- **Nguồn:** 8.2 Output; dòng [778](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:778).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.2 Output.
- **Task trước trong tiểu mục:** T08-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Output 12h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Output 12h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Output B×5×2 gắn đúng thứ tự horizon; kiểm tra đơn vị tọa độ và denormalization trong pipeline.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-012"></a>
## T08-012 — Output 24h.

- **Trạng thái:** pending.
- **Nguồn:** 8.2 Output; dòng [779](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:779).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.2 Output.
- **Task trước trong tiểu mục:** T08-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Output 24h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Output 24h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Output B×5×2 gắn đúng thứ tự horizon; kiểm tra đơn vị tọa độ và denormalization trong pipeline.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-013"></a>
## T08-013 — Output 48h.

- **Trạng thái:** pending.
- **Nguồn:** 8.2 Output; dòng [780](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:780).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.2 Output.
- **Task trước trong tiểu mục:** T08-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Output 48h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Output 48h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Output B×5×2 gắn đúng thứ tự horizon; kiểm tra đơn vị tọa độ và denormalization trong pipeline.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-014"></a>
## T08-014 — Output 72h.

- **Trạng thái:** pending.
- **Nguồn:** 8.2 Output; dòng [781](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:781).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.2 Output.
- **Task trước trong tiểu mục:** T08-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Output 72h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Output 72h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Output B×5×2 gắn đúng thứ tự horizon; kiểm tra đơn vị tọa độ và denormalization trong pipeline.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-015"></a>
## T08-015 — Kiểm tra lat/lon.

- **Trạng thái:** pending.
- **Nguồn:** 8.2 Output; dòng [782](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:782).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.2 Output.
- **Task trước trong tiểu mục:** T08-014; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Kiểm tra lat/lon.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra lat/lon.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hợp lệ/ngoài biên/NaN/Inf và wrap longitude; output giữ đúng đơn vị tọa độ.
- **Kịch bản tiểu mục:** Output B×5×2 gắn đúng thứ tự horizon; kiểm tra đơn vị tọa độ và denormalization trong pipeline.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-016"></a>
## T08-016 — Tạo wind head.

- **Trạng thái:** pending.
- **Nguồn:** 8.3 Intensity Head; dòng [785](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:785).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.3 Intensity Head.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Tạo wind head.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo wind head.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Chỉ thêm wind/pressure regression heads khi có nhãn và masked loss; thiếu nhãn không được gán 0; class vocabulary cố định.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-017"></a>
## T08-017 — Tạo pressure head.

- **Trạng thái:** pending.
- **Nguồn:** 8.3 Intensity Head; dòng [786](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:786).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.3 Intensity Head.
- **Task trước trong tiểu mục:** T08-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Tạo pressure head.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo pressure head.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Chỉ thêm wind/pressure regression heads khi có nhãn và masked loss; thiếu nhãn không được gán 0; class vocabulary cố định.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-018"></a>
## T08-018 — Tạo category head nếu dữ liệu hỗ trợ.

- **Trạng thái:** pending.
- **Nguồn:** 8.3 Intensity Head; dòng [787](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:787).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.3 Intensity Head.
- **Task trước trong tiểu mục:** T08-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Tạo category head nếu dữ liệu hỗ trợ.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo category head nếu dữ liệu hỗ trợ.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Chỉ thêm wind/pressure regression heads khi có nhãn và masked loss; thiếu nhãn không được gán 0; class vocabulary cố định.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-019"></a>
## T08-019 — Kiểm tra output shape.

- **Trạng thái:** pending.
- **Nguồn:** 8.3 Intensity Head; dòng [788](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:788).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.3 Intensity Head.
- **Task trước trong tiểu mục:** T08-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Kiểm tra output shape.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra output shape.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test B=1/4, T=4/6/8; shape/dtype đúng; thay padding không đổi output hợp lệ; không qua storm boundary.
- **Kịch bản tiểu mục:** Chỉ thêm wind/pressure regression heads khi có nhãn và masked loss; thiếu nhãn không được gán 0; class vocabulary cố định.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-020"></a>
## T08-020 — Forward test.

- **Trạng thái:** pending.
- **Nguồn:** 8.4 Tests; dòng [791](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:791).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.4 Tests.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Forward test.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-020.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Forward test.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Save/load cùng input giữ output trong dung sai; gradient hữu hạn và có update; thử CPU trước GPU.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-021"></a>
## T08-021 — Batch-size test.

- **Trạng thái:** pending.
- **Nguồn:** 8.4 Tests; dòng [792](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:792).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.4 Tests.
- **Task trước trong tiểu mục:** T08-020; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Batch-size test.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-021.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Batch-size test.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test B=1/4, T=4/6/8; shape/dtype đúng; thay padding không đổi output hợp lệ; không qua storm boundary.
- **Kịch bản tiểu mục:** Save/load cùng input giữ output trong dung sai; gradient hữu hạn và có update; thử CPU trước GPU.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-022"></a>
## T08-022 — Sequence-length test.

- **Trạng thái:** pending.
- **Nguồn:** 8.4 Tests; dòng [793](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:793).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.4 Tests.
- **Task trước trong tiểu mục:** T08-021; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Sequence-length test.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-022.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Sequence-length test.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test B=1/4, T=4/6/8; shape/dtype đúng; thay padding không đổi output hợp lệ; không qua storm boundary.
- **Kịch bản tiểu mục:** Save/load cùng input giữ output trong dung sai; gradient hữu hạn và có update; thử CPU trước GPU.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-023"></a>
## T08-023 — Gradient test.

- **Trạng thái:** pending.
- **Nguồn:** 8.4 Tests; dòng [794](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:794).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.4 Tests.
- **Task trước trong tiểu mục:** T08-022; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Gradient test.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-023.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Gradient test.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Loss/gradient hữu hạn với fixture đúng; NaN/empty phải fail rõ và không lưu best checkpoint giả.
- **Kịch bản tiểu mục:** Save/load cùng input giữ output trong dung sai; gradient hữu hạn và có update; thử CPU trước GPU.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t08-024"></a>
## T08-024 — Save/load test.

- **Trạng thái:** pending.
- **Nguồn:** 8.4 Tests; dòng [795](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:795).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06; contract/fixture của tiểu mục 8.4 Tests.
- **Task trước trong tiểu mục:** T08-023; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tensor contract, feature schema, target schema và vocabulary cố định; yêu cầu riêng: Save/load test.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/base.py; src/typhoon_vn/models/lstm.py; tests/test_models.py; evidence tại evidence/T08-024.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Save/load test.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G08, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Reload đủ state; resume so với chạy liên tục; epoch/history/LR nhất quán; checkpoint mới không đè artifact khác.
- **Kịch bản tiểu mục:** Save/load cùng input giữ output trong dung sai; gradient hữu hạn và có update; thử CPU trước GPU.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
