# G05 — Scaling không rò rỉ

- Trạng thái: complete; nghiệm thu tại [G05-scaling.md](evidence/G05-scaling.md).
- Hiện trạng: Có scaler; cần tích hợp artifact manifest và kiểm thử parity.
- Đầu vào: Feature schema đóng băng và split manifest theo storm.
- Gate phụ thuộc: G04, G06.
- Vùng file dự kiến: src/typhoon_vn/features/scaling.py; tests/test_scaling_contract.py.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Chỉ fit train; thống kê bất biến khi val/test thay đổi; schema mismatch bị từ chối; round-trip có dung sai định trước.

<a id="gate-g05"></a>
## Gate G05

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t05-001"></a>
## T05-001 — Chia train/validation/test trước khi fit scaler.

- **Trạng thái:** complete.
- **Nguồn:** 5. SCALING; dòng [689](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:689).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G04, G06; contract/fixture của tiểu mục 5. SCALING.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Feature schema đóng băng và split manifest theo storm; yêu cầu riêng: Chia train/validation/test trước khi fit scaler.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/scaling.py; tests/test_scaling_contract.py; evidence tại evidence/T05-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chia train/validation/test trước khi fit scaler.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G05, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fit train-only; val/test cực trị không đổi stats; save/load giữ order/fill; finite round-trip <=1e-6.
- **Kịch bản tiểu mục:** Chỉ fit train; thống kê bất biến khi val/test thay đổi; schema mismatch bị từ chối; round-trip có dung sai định trước.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T05-001.md](evidence/T05-001.md).

<a id="t05-002"></a>
## T05-002 — Fit scaler chỉ trên train.

- **Trạng thái:** complete.
- **Nguồn:** 5. SCALING; dòng [690](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:690).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G04, G06; contract/fixture của tiểu mục 5. SCALING.
- **Task trước trong tiểu mục:** T05-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Feature schema đóng băng và split manifest theo storm; yêu cầu riêng: Fit scaler chỉ trên train.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/scaling.py; tests/test_scaling_contract.py; evidence tại evidence/T05-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Fit scaler chỉ trên train.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G05, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fit train-only; val/test cực trị không đổi stats; save/load giữ order/fill; finite round-trip <=1e-6.
- **Kịch bản tiểu mục:** Chỉ fit train; thống kê bất biến khi val/test thay đổi; schema mismatch bị từ chối; round-trip có dung sai định trước.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T05-002.md](evidence/T05-002.md).

<a id="t05-003"></a>
## T05-003 — Save scaler.

- **Trạng thái:** complete.
- **Nguồn:** 5. SCALING; dòng [691](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:691).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G04, G06; contract/fixture của tiểu mục 5. SCALING.
- **Task trước trong tiểu mục:** T05-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Feature schema đóng băng và split manifest theo storm; yêu cầu riêng: Save scaler.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/scaling.py; tests/test_scaling_contract.py; evidence tại evidence/T05-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Save scaler.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G05, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fit train-only; val/test cực trị không đổi stats; save/load giữ order/fill; finite round-trip <=1e-6.
- **Kịch bản tiểu mục:** Chỉ fit train; thống kê bất biến khi val/test thay đổi; schema mismatch bị từ chối; round-trip có dung sai định trước.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T05-003.md](evidence/T05-003.md).

<a id="t05-004"></a>
## T05-004 — Load scaler khi inference.

- **Trạng thái:** complete.
- **Nguồn:** 5. SCALING; dòng [692](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:692).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G04, G06; contract/fixture của tiểu mục 5. SCALING.
- **Task trước trong tiểu mục:** T05-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Feature schema đóng băng và split manifest theo storm; yêu cầu riêng: Load scaler khi inference.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/scaling.py; tests/test_scaling_contract.py; evidence tại evidence/T05-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Load scaler khi inference.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G05, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fit train-only; val/test cực trị không đổi stats; save/load giữ order/fill; finite round-trip <=1e-6.
- **Kịch bản tiểu mục:** Chỉ fit train; thống kê bất biến khi val/test thay đổi; schema mismatch bị từ chối; round-trip có dung sai định trước.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T05-004.md](evidence/T05-004.md).

<a id="t05-005"></a>
## T05-005 — Transform train.

- **Trạng thái:** complete.
- **Nguồn:** 5. SCALING; dòng [693](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:693).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G04, G06; contract/fixture của tiểu mục 5. SCALING.
- **Task trước trong tiểu mục:** T05-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Feature schema đóng băng và split manifest theo storm; yêu cầu riêng: Transform train.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/scaling.py; tests/test_scaling_contract.py; evidence tại evidence/T05-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Transform train.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G05, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Chỉ fit train; thống kê bất biến khi val/test thay đổi; schema mismatch bị từ chối; round-trip có dung sai định trước.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T05-005.md](evidence/T05-005.md).

<a id="t05-006"></a>
## T05-006 — Transform validation.

- **Trạng thái:** complete.
- **Nguồn:** 5. SCALING; dòng [694](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:694).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G04, G06; contract/fixture của tiểu mục 5. SCALING.
- **Task trước trong tiểu mục:** T05-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Feature schema đóng băng và split manifest theo storm; yêu cầu riêng: Transform validation.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/scaling.py; tests/test_scaling_contract.py; evidence tại evidence/T05-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Transform validation.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G05, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Chỉ fit train; thống kê bất biến khi val/test thay đổi; schema mismatch bị từ chối; round-trip có dung sai định trước.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T05-006.md](evidence/T05-006.md).

<a id="t05-007"></a>
## T05-007 — Transform test.

- **Trạng thái:** complete.
- **Nguồn:** 5. SCALING; dòng [695](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:695).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G04, G06; contract/fixture của tiểu mục 5. SCALING.
- **Task trước trong tiểu mục:** T05-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Feature schema đóng băng và split manifest theo storm; yêu cầu riêng: Transform test.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/scaling.py; tests/test_scaling_contract.py; evidence tại evidence/T05-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Transform test.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G05, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Chỉ fit train; thống kê bất biến khi val/test thay đổi; schema mismatch bị từ chối; round-trip có dung sai định trước.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T05-007.md](evidence/T05-007.md).

<a id="t05-008"></a>
## T05-008 — Test inverse transform.

- **Trạng thái:** complete.
- **Nguồn:** 5. SCALING; dòng [696](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:696).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G04, G06; contract/fixture của tiểu mục 5. SCALING.
- **Task trước trong tiểu mục:** T05-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Feature schema đóng băng và split manifest theo storm; yêu cầu riêng: Test inverse transform.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/scaling.py; tests/test_scaling_contract.py; evidence tại evidence/T05-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test inverse transform.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G05, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fit train-only; val/test cực trị không đổi stats; save/load giữ order/fill; finite round-trip <=1e-6.
- **Kịch bản tiểu mục:** Chỉ fit train; thống kê bất biến khi val/test thay đổi; schema mismatch bị từ chối; round-trip có dung sai định trước.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T05-008.md](evidence/T05-008.md).

<a id="t05-009"></a>
## T05-009 — Test không có leakage.

- **Trạng thái:** complete.
- **Nguồn:** 5. SCALING; dòng [697](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:697).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G04, G06; contract/fixture của tiểu mục 5. SCALING.
- **Task trước trong tiểu mục:** T05-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Feature schema đóng băng và split manifest theo storm; yêu cầu riêng: Test không có leakage.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/scaling.py; tests/test_scaling_contract.py; evidence tại evidence/T05-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test không có leakage.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G05, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Storm không giao train/val/test kể cả qua năm; ratio=0 đúng nghĩa; split IDs/seed được lưu.
- **Kịch bản tiểu mục:** Chỉ fit train; thống kê bất biến khi val/test thay đổi; schema mismatch bị từ chối; round-trip có dung sai định trước.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T05-009.md](evidence/T05-009.md).
