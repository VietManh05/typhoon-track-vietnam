# G10 — Loss và tối ưu

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có loss/trainer; cần kiểm chứng case NaN và scheduler.
- Đầu vào: Target units, loss weights và model parameters.
- Gate phụ thuộc: G08.
- Vùng file dự kiến: src/typhoon_vn/training/losses.py; src/typhoon_vn/training/trainer.py; tests/test_training.py.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Loss hữu hạn; từng thành phần được log; horizon weights có hiệu lực; optimizer/scheduler có test.

<a id="gate-g10"></a>
## Gate G10

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t10-001"></a>
## T10-001 — Position loss.

- **Trạng thái:** pending.
- **Nguồn:** 10. LOSS & OPTIMIZATION; dòng [832](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:832).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G08; contract/fixture của tiểu mục 10. LOSS & OPTIMIZATION.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Target units, loss weights và model parameters; yêu cầu riêng: Position loss.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/losses.py; src/typhoon_vn/training/trainer.py; tests/test_training.py; evidence tại evidence/T10-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Position loss.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G10, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Loss/gradient hữu hạn với fixture đúng; NaN/empty phải fail rõ và không lưu best checkpoint giả.
- **Kịch bản tiểu mục:** Loss hữu hạn; từng thành phần được log; horizon weights có hiệu lực; optimizer/scheduler có test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t10-002"></a>
## T10-002 — Intensity loss.

- **Trạng thái:** pending.
- **Nguồn:** 10. LOSS & OPTIMIZATION; dòng [833](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:833).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G08; contract/fixture của tiểu mục 10. LOSS & OPTIMIZATION.
- **Task trước trong tiểu mục:** T10-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Target units, loss weights và model parameters; yêu cầu riêng: Intensity loss.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/losses.py; src/typhoon_vn/training/trainer.py; tests/test_training.py; evidence tại evidence/T10-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Intensity loss.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G10, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Loss/gradient hữu hạn với fixture đúng; NaN/empty phải fail rõ và không lưu best checkpoint giả.
- **Kịch bản tiểu mục:** Loss hữu hạn; từng thành phần được log; horizon weights có hiệu lực; optimizer/scheduler có test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t10-003"></a>
## T10-003 — Horizon weights.

- **Trạng thái:** pending.
- **Nguồn:** 10. LOSS & OPTIMIZATION; dòng [834](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:834).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G08; contract/fixture của tiểu mục 10. LOSS & OPTIMIZATION.
- **Task trước trong tiểu mục:** T10-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Target units, loss weights và model parameters; yêu cầu riêng: Horizon weights.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/losses.py; src/typhoon_vn/training/trainer.py; tests/test_training.py; evidence tại evidence/T10-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Horizon weights.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G10, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Loss hữu hạn; từng thành phần được log; horizon weights có hiệu lực; optimizer/scheduler có test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t10-004"></a>
## T10-004 — Haversine-based evaluation/loss nếu triển khai.

- **Trạng thái:** pending.
- **Nguồn:** 10. LOSS & OPTIMIZATION; dòng [835](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:835).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G08; contract/fixture của tiểu mục 10. LOSS & OPTIMIZATION.
- **Task trước trong tiểu mục:** T10-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Target units, loss weights và model parameters; yêu cầu riêng: Haversine-based evaluation/loss nếu triển khai.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/losses.py; src/typhoon_vn/training/trainer.py; tests/test_training.py; evidence tại evidence/T10-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Haversine-based evaluation/loss nếu triển khai.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G10, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Điểm trùng cho 0 km; cặp điểm chuẩn khớp dung sai; wrap longitude không tạo khoảng cách vòng trái đất.
- **Kịch bản tiểu mục:** Loss hữu hạn; từng thành phần được log; horizon weights có hiệu lực; optimizer/scheduler có test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t10-005"></a>
## T10-005 — AdamW.

- **Trạng thái:** pending.
- **Nguồn:** 10. LOSS & OPTIMIZATION; dòng [836](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:836).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G08; contract/fixture của tiểu mục 10. LOSS & OPTIMIZATION.
- **Task trước trong tiểu mục:** T10-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Target units, loss weights và model parameters; yêu cầu riêng: AdamW.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/losses.py; src/typhoon_vn/training/trainer.py; tests/test_training.py; evidence tại evidence/T10-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “AdamW.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G10, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Loss hữu hạn; từng thành phần được log; horizon weights có hiệu lực; optimizer/scheduler có test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t10-006"></a>
## T10-006 — Learning-rate scheduler.

- **Trạng thái:** pending.
- **Nguồn:** 10. LOSS & OPTIMIZATION; dòng [837](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:837).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G08; contract/fixture của tiểu mục 10. LOSS & OPTIMIZATION.
- **Task trước trong tiểu mục:** T10-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Target units, loss weights và model parameters; yêu cầu riêng: Learning-rate scheduler.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/losses.py; src/typhoon_vn/training/trainer.py; tests/test_training.py; evidence tại evidence/T10-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Learning-rate scheduler.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G10, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Loss hữu hạn; từng thành phần được log; horizon weights có hiệu lực; optimizer/scheduler có test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t10-007"></a>
## T10-007 — Gradient clipping.

- **Trạng thái:** pending.
- **Nguồn:** 10. LOSS & OPTIMIZATION; dòng [838](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:838).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G08; contract/fixture của tiểu mục 10. LOSS & OPTIMIZATION.
- **Task trước trong tiểu mục:** T10-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Target units, loss weights và model parameters; yêu cầu riêng: Gradient clipping.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/losses.py; src/typhoon_vn/training/trainer.py; tests/test_training.py; evidence tại evidence/T10-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Gradient clipping.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G10, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Loss/gradient hữu hạn với fixture đúng; NaN/empty phải fail rõ và không lưu best checkpoint giả.
- **Kịch bản tiểu mục:** Loss hữu hạn; từng thành phần được log; horizon weights có hiệu lực; optimizer/scheduler có test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t10-008"></a>
## T10-008 — Kiểm tra NaN loss.

- **Trạng thái:** pending.
- **Nguồn:** 10. LOSS & OPTIMIZATION; dòng [839](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:839).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G08; contract/fixture của tiểu mục 10. LOSS & OPTIMIZATION.
- **Task trước trong tiểu mục:** T10-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Target units, loss weights và model parameters; yêu cầu riêng: Kiểm tra NaN loss.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/losses.py; src/typhoon_vn/training/trainer.py; tests/test_training.py; evidence tại evidence/T10-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra NaN loss.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G10, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Loss/gradient hữu hạn với fixture đúng; NaN/empty phải fail rõ và không lưu best checkpoint giả.
- **Kịch bản tiểu mục:** Loss hữu hạn; từng thành phần được log; horizon weights có hiệu lực; optimizer/scheduler có test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t10-009"></a>
## T10-009 — Log từng thành phần loss.

- **Trạng thái:** pending.
- **Nguồn:** 10. LOSS & OPTIMIZATION; dòng [840](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:840).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G08; contract/fixture của tiểu mục 10. LOSS & OPTIMIZATION.
- **Task trước trong tiểu mục:** T10-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Target units, loss weights và model parameters; yêu cầu riêng: Log từng thành phần loss.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/losses.py; src/typhoon_vn/training/trainer.py; tests/test_training.py; evidence tại evidence/T10-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Log từng thành phần loss.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G10, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Loss/gradient hữu hạn với fixture đúng; NaN/empty phải fail rõ và không lưu best checkpoint giả.
- **Kịch bản tiểu mục:** Loss hữu hạn; từng thành phần được log; horizon weights có hiệu lực; optimizer/scheduler có test.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
