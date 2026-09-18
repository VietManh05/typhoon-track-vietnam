# G09 — Seq2Seq, attention và Transformer

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có kiến trúc; chưa có bằng chứng tốt hơn baseline.
- Đầu vào: LSTM baseline đã có validation report và ngân sách thử nghiệm.
- Gate phụ thuộc: G12, G13.
- Vùng file dự kiến: src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Chạy cùng split/scaler; mask không ảnh hưởng bởi padding; teacher forcing chỉ khi train; lựa chọn dựa validation.

<a id="gate-g09"></a>
## Gate G09

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t09-001"></a>
## T09-001 — Encoder.

- **Trạng thái:** pending.
- **Nguồn:** 9.1 Seq2Seq; dòng [802](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:802).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.1 Seq2Seq.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Encoder.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Encoder.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Train teacher forcing có target hợp lệ, eval không đọc target; horizon không đều không bị hiểu thành các bước 6h liên tiếp.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-002"></a>
## T09-002 — Decoder.

- **Trạng thái:** pending.
- **Nguồn:** 9.1 Seq2Seq; dòng [803](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:803).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.1 Seq2Seq.
- **Task trước trong tiểu mục:** T09-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Decoder.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Decoder.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Train teacher forcing có target hợp lệ, eval không đọc target; horizon không đều không bị hiểu thành các bước 6h liên tiếp.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-003"></a>
## T09-003 — Hidden state.

- **Trạng thái:** pending.
- **Nguồn:** 9.1 Seq2Seq; dòng [804](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:804).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.1 Seq2Seq.
- **Task trước trong tiểu mục:** T09-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Hidden state.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Hidden state.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Train teacher forcing có target hợp lệ, eval không đọc target; horizon không đều không bị hiểu thành các bước 6h liên tiếp.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-004"></a>
## T09-004 — Multi-step output.

- **Trạng thái:** pending.
- **Nguồn:** 9.1 Seq2Seq; dòng [805](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:805).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.1 Seq2Seq.
- **Task trước trong tiểu mục:** T09-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Multi-step output.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Multi-step output.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Train teacher forcing có target hợp lệ, eval không đọc target; horizon không đều không bị hiểu thành các bước 6h liên tiếp.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-005"></a>
## T09-005 — Teacher forcing nếu sử dụng.

- **Trạng thái:** pending.
- **Nguồn:** 9.1 Seq2Seq; dòng [806](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:806).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.1 Seq2Seq.
- **Task trước trong tiểu mục:** T09-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Teacher forcing nếu sử dụng.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Teacher forcing nếu sử dụng.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Train teacher forcing có target hợp lệ, eval không đọc target; horizon không đều không bị hiểu thành các bước 6h liên tiếp.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-006"></a>
## T09-006 — Test inference.

- **Trạng thái:** pending.
- **Nguồn:** 9.1 Seq2Seq; dòng [807](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:807).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.1 Seq2Seq.
- **Task trước trong tiểu mục:** T09-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Test inference.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test inference.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Train teacher forcing có target hợp lệ, eval không đọc target; horizon không đều không bị hiểu thành các bước 6h liên tiếp.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-007"></a>
## T09-007 — Tạo attention layer.

- **Trạng thái:** pending.
- **Nguồn:** 9.2 Attention; dòng [810](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:810).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.2 Attention.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Tạo attention layer.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo attention layer.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Attention weights tổng 1 trên vị trí hợp lệ; padding weights bằng 0; toàn bộ masked bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-008"></a>
## T09-008 — Tính attention score.

- **Trạng thái:** pending.
- **Nguồn:** 9.2 Attention; dòng [811](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:811).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.2 Attention.
- **Task trước trong tiểu mục:** T09-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Tính attention score.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính attention score.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Attention weights tổng 1 trên vị trí hợp lệ; padding weights bằng 0; toàn bộ masked bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-009"></a>
## T09-009 — Softmax.

- **Trạng thái:** pending.
- **Nguồn:** 9.2 Attention; dòng [812](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:812).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.2 Attention.
- **Task trước trong tiểu mục:** T09-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Softmax.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Softmax.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Attention weights tổng 1 trên vị trí hợp lệ; padding weights bằng 0; toàn bộ masked bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-010"></a>
## T09-010 — Context vector.

- **Trạng thái:** pending.
- **Nguồn:** 9.2 Attention; dòng [813](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:813).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.2 Attention.
- **Task trước trong tiểu mục:** T09-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Context vector.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Context vector.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Attention weights tổng 1 trên vị trí hợp lệ; padding weights bằng 0; toàn bộ masked bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-011"></a>
## T09-011 — Kết hợp output.

- **Trạng thái:** pending.
- **Nguồn:** 9.2 Attention; dòng [814](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:814).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.2 Attention.
- **Task trước trong tiểu mục:** T09-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Kết hợp output.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kết hợp output.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Attention weights tổng 1 trên vị trí hợp lệ; padding weights bằng 0; toàn bộ masked bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-012"></a>
## T09-012 — Visualize attention nếu cần.

- **Trạng thái:** pending.
- **Nguồn:** 9.2 Attention; dòng [815](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:815).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.2 Attention.
- **Task trước trong tiểu mục:** T09-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Visualize attention nếu cần.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Visualize attention nếu cần.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Attention weights tổng 1 trên vị trí hợp lệ; padding weights bằng 0; toàn bộ masked bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-013"></a>
## T09-013 — Positional encoding.

- **Trạng thái:** pending.
- **Nguồn:** 9.3 Transformer; dòng [818](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:818).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.3 Transformer.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Positional encoding.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Positional encoding.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mask/positional encoding hỗ trợ độ dài công bố; seed/config/budget giống baseline; so validation trước chọn model.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-014"></a>
## T09-014 — Encoder.

- **Trạng thái:** pending.
- **Nguồn:** 9.3 Transformer; dòng [819](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:819).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.3 Transformer.
- **Task trước trong tiểu mục:** T09-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Encoder.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Encoder.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mask/positional encoding hỗ trợ độ dài công bố; seed/config/budget giống baseline; so validation trước chọn model.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-015"></a>
## T09-015 — Attention.

- **Trạng thái:** pending.
- **Nguồn:** 9.3 Transformer; dòng [820](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:820).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.3 Transformer.
- **Task trước trong tiểu mục:** T09-014; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Attention.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Attention.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mask/positional encoding hỗ trợ độ dài công bố; seed/config/budget giống baseline; so validation trước chọn model.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-016"></a>
## T09-016 — Feed-forward.

- **Trạng thái:** pending.
- **Nguồn:** 9.3 Transformer; dòng [821](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:821).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.3 Transformer.
- **Task trước trong tiểu mục:** T09-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Feed-forward.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Feed-forward.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mask/positional encoding hỗ trợ độ dài công bố; seed/config/budget giống baseline; so validation trước chọn model.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-017"></a>
## T09-017 — Output head.

- **Trạng thái:** pending.
- **Nguồn:** 9.3 Transformer; dòng [822](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:822).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.3 Transformer.
- **Task trước trong tiểu mục:** T09-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Output head.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Output head.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mask/positional encoding hỗ trợ độ dài công bố; seed/config/budget giống baseline; so validation trước chọn model.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-018"></a>
## T09-018 — Train baseline.

- **Trạng thái:** pending.
- **Nguồn:** 9.3 Transformer; dòng [823](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:823).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.3 Transformer.
- **Task trước trong tiểu mục:** T09-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Train baseline.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Train baseline.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mask/positional encoding hỗ trợ độ dài công bố; seed/config/budget giống baseline; so validation trước chọn model.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t09-019"></a>
## T09-019 — Compare với LSTM.

- **Trạng thái:** pending.
- **Nguồn:** 9.3 Transformer; dòng [824](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:824).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G12, G13; contract/fixture của tiểu mục 9.3 Transformer.
- **Task trước trong tiểu mục:** T09-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** LSTM baseline đã có validation report và ngân sách thử nghiệm; yêu cầu riêng: Compare với LSTM.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/models/lstm.py; src/typhoon_vn/models/transformer.py; tests/test_models.py; configs/; evidence tại evidence/T09-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Compare với LSTM.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G09, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mask/positional encoding hỗ trợ độ dài công bố; seed/config/budget giống baseline; so validation trước chọn model.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
