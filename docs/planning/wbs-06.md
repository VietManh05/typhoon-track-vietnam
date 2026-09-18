# G06 — Dataset và phân chia tập

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có dataset; chọn feature trước khi tạo feature và split storm qua năm cần sửa.
- Đầu vào: Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian.
- Gate phụ thuộc: G03, G04.
- Vùng file dự kiến: src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Storm không giao nhau; target đúng issue_time+horizon; thiếu mốc không lấy hàng kế tiếp thay thế; mask/shape/dtype đúng.

<a id="gate-g06"></a>
## Gate G06

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t06-001"></a>
## T06-001 — Chọn sequence length.

- **Trạng thái:** pending.
- **Nguồn:** 6.1 Window; dòng [706](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:706).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.1 Window.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Chọn sequence length.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chọn sequence length.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test B=1/4, T=4/6/8; shape/dtype đúng; thay padding không đổi output hợp lệ; không qua storm boundary.
- **Kịch bản tiểu mục:** Fixture 1 bão ngắn và 2 bão nối nhau; không có window vượt storm boundary; input_len không hợp lệ bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-002"></a>
## T06-002 — Hỗ trợ cấu hình sequence length.

- **Trạng thái:** pending.
- **Nguồn:** 6.1 Window; dòng [707](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:707).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.1 Window.
- **Task trước trong tiểu mục:** T06-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Hỗ trợ cấu hình sequence length.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Hỗ trợ cấu hình sequence length.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test B=1/4, T=4/6/8; shape/dtype đúng; thay padding không đổi output hợp lệ; không qua storm boundary.
- **Kịch bản tiểu mục:** Fixture 1 bão ngắn và 2 bão nối nhau; không có window vượt storm boundary; input_len không hợp lệ bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-003"></a>
## T06-003 — Tạo sliding window.

- **Trạng thái:** pending.
- **Nguồn:** 6.1 Window; dòng [708](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:708).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.1 Window.
- **Task trước trong tiểu mục:** T06-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Tạo sliding window.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo sliding window.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Cửa sổ chỉ chứa một storm, input_len đúng; fixture ngắn hơn window không tạo sample; timestamps không đảo hoặc trùng.
- **Kịch bản tiểu mục:** Fixture 1 bão ngắn và 2 bão nối nhau; không có window vượt storm boundary; input_len không hợp lệ bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-004"></a>
## T06-004 — Tạo input tensor.

- **Trạng thái:** pending.
- **Nguồn:** 6.1 Window; dòng [709](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:709).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.1 Window.
- **Task trước trong tiểu mục:** T06-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Tạo input tensor.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo input tensor.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test B=1/4, T=4/6/8; shape/dtype đúng; thay padding không đổi output hợp lệ; không qua storm boundary.
- **Kịch bản tiểu mục:** Fixture 1 bão ngắn và 2 bão nối nhau; không có window vượt storm boundary; input_len không hợp lệ bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-005"></a>
## T06-005 — Tạo target tensor.

- **Trạng thái:** pending.
- **Nguồn:** 6.1 Window; dòng [710](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:710).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.1 Window.
- **Task trước trong tiểu mục:** T06-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Tạo target tensor.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo target tensor.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Fixture 1 bão ngắn và 2 bão nối nhau; không có window vượt storm boundary; input_len không hợp lệ bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-006"></a>
## T06-006 — Kiểm tra boundary từng storm.

- **Trạng thái:** pending.
- **Nguồn:** 6.1 Window; dòng [711](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:711).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.1 Window.
- **Task trước trong tiểu mục:** T06-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Kiểm tra boundary từng storm.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra boundary từng storm.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Fixture 1 bão ngắn và 2 bão nối nhau; không có window vượt storm boundary; input_len không hợp lệ bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-007"></a>
## T06-007 — 6h.

- **Trạng thái:** pending.
- **Nguồn:** 6.2 Horizons; dòng [714](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:714).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.2 Horizons.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: 6h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “6h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Issue 00:00 UTC phải lấy target ở +6,+12,+24,+48,+72 giờ; bỏ mốc +12 không được lấy +18 thay thế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-008"></a>
## T06-008 — 12h.

- **Trạng thái:** pending.
- **Nguồn:** 6.2 Horizons; dòng [715](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:715).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.2 Horizons.
- **Task trước trong tiểu mục:** T06-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: 12h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “12h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Issue 00:00 UTC phải lấy target ở +6,+12,+24,+48,+72 giờ; bỏ mốc +12 không được lấy +18 thay thế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-009"></a>
## T06-009 — 24h.

- **Trạng thái:** pending.
- **Nguồn:** 6.2 Horizons; dòng [716](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:716).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.2 Horizons.
- **Task trước trong tiểu mục:** T06-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: 24h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “24h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Issue 00:00 UTC phải lấy target ở +6,+12,+24,+48,+72 giờ; bỏ mốc +12 không được lấy +18 thay thế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-010"></a>
## T06-010 — 48h.

- **Trạng thái:** pending.
- **Nguồn:** 6.2 Horizons; dòng [717](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:717).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.2 Horizons.
- **Task trước trong tiểu mục:** T06-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: 48h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “48h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Issue 00:00 UTC phải lấy target ở +6,+12,+24,+48,+72 giờ; bỏ mốc +12 không được lấy +18 thay thế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-011"></a>
## T06-011 — 72h.

- **Trạng thái:** pending.
- **Nguồn:** 6.2 Horizons; dòng [718](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:718).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.2 Horizons.
- **Task trước trong tiểu mục:** T06-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: 72h.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “72h.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Issue 00:00 UTC phải lấy target ở +6,+12,+24,+48,+72 giờ; bỏ mốc +12 không được lấy +18 thay thế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-012"></a>
## T06-012 — Kiểm tra target tồn tại.

- **Trạng thái:** pending.
- **Nguồn:** 6.2 Horizons; dòng [719](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:719).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.2 Horizons.
- **Task trước trong tiểu mục:** T06-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Kiểm tra target tồn tại.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra target tồn tại.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Issue 00:00 UTC phải lấy target ở +6,+12,+24,+48,+72 giờ; bỏ mốc +12 không được lấy +18 thay thế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-013"></a>
## T06-013 — Bỏ sample không đủ target.

- **Trạng thái:** pending.
- **Nguồn:** 6.2 Horizons; dòng [720](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:720).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.2 Horizons.
- **Task trước trong tiểu mục:** T06-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Bỏ sample không đủ target.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Bỏ sample không đủ target.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Issue 00:00 UTC phải lấy target ở +6,+12,+24,+48,+72 giờ; bỏ mốc +12 không được lấy +18 thay thế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-014"></a>
## T06-014 — Split theo storm ID.

- **Trạng thái:** pending.
- **Nguồn:** 6.3 Split; dòng [723](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:723).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.3 Split.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Split theo storm ID.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Split theo storm ID.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Storm không giao train/val/test kể cả qua năm; ratio=0 đúng nghĩa; split IDs/seed được lưu.
- **Kịch bản tiểu mục:** Test bão qua 31/12→01/01; train/val/test không giao storm; ratio=0 tạo tập rỗng đúng; tổng tỷ lệ sai bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-015"></a>
## T06-015 — Kiểm tra không overlap storm.

- **Trạng thái:** pending.
- **Nguồn:** 6.3 Split; dòng [724](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:724).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.3 Split.
- **Task trước trong tiểu mục:** T06-014; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Kiểm tra không overlap storm.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra không overlap storm.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Storm không giao train/val/test kể cả qua năm; ratio=0 đúng nghĩa; split IDs/seed được lưu.
- **Kịch bản tiểu mục:** Test bão qua 31/12→01/01; train/val/test không giao storm; ratio=0 tạo tập rỗng đúng; tổng tỷ lệ sai bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-016"></a>
## T06-016 — Có tùy chọn split theo năm.

- **Trạng thái:** pending.
- **Nguồn:** 6.3 Split; dòng [725](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:725).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.3 Split.
- **Task trước trong tiểu mục:** T06-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Có tùy chọn split theo năm.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Có tùy chọn split theo năm.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Storm không giao train/val/test kể cả qua năm; ratio=0 đúng nghĩa; split IDs/seed được lưu.
- **Kịch bản tiểu mục:** Test bão qua 31/12→01/01; train/val/test không giao storm; ratio=0 tạo tập rỗng đúng; tổng tỷ lệ sai bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-017"></a>
## T06-017 — Lưu danh sách train IDs.

- **Trạng thái:** pending.
- **Nguồn:** 6.3 Split; dòng [726](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:726).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.3 Split.
- **Task trước trong tiểu mục:** T06-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Lưu danh sách train IDs.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu danh sách train IDs.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Storm không giao train/val/test kể cả qua năm; ratio=0 đúng nghĩa; split IDs/seed được lưu.
- **Kịch bản tiểu mục:** Test bão qua 31/12→01/01; train/val/test không giao storm; ratio=0 tạo tập rỗng đúng; tổng tỷ lệ sai bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-018"></a>
## T06-018 — Lưu validation IDs.

- **Trạng thái:** pending.
- **Nguồn:** 6.3 Split; dòng [727](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:727).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.3 Split.
- **Task trước trong tiểu mục:** T06-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Lưu validation IDs.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu validation IDs.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Storm không giao train/val/test kể cả qua năm; ratio=0 đúng nghĩa; split IDs/seed được lưu.
- **Kịch bản tiểu mục:** Test bão qua 31/12→01/01; train/val/test không giao storm; ratio=0 tạo tập rỗng đúng; tổng tỷ lệ sai bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-019"></a>
## T06-019 — Lưu test IDs.

- **Trạng thái:** pending.
- **Nguồn:** 6.3 Split; dòng [728](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:728).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.3 Split.
- **Task trước trong tiểu mục:** T06-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Lưu test IDs.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu test IDs.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Storm không giao train/val/test kể cả qua năm; ratio=0 đúng nghĩa; split IDs/seed được lưu.
- **Kịch bản tiểu mục:** Test bão qua 31/12→01/01; train/val/test không giao storm; ratio=0 tạo tập rỗng đúng; tổng tỷ lệ sai bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-020"></a>
## T06-020 — Test leakage.

- **Trạng thái:** pending.
- **Nguồn:** 6.3 Split; dòng [729](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:729).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.3 Split.
- **Task trước trong tiểu mục:** T06-019; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Test leakage.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-020.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test leakage.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Storm không giao train/val/test kể cả qua năm; ratio=0 đúng nghĩa; split IDs/seed được lưu.
- **Kịch bản tiểu mục:** Test bão qua 31/12→01/01; train/val/test không giao storm; ratio=0 tạo tập rỗng đúng; tổng tỷ lệ sai bị từ chối.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-021"></a>
## T06-021 — Test shape.

- **Trạng thái:** pending.
- **Nguồn:** 6.4 Dataset Tests; dòng [732](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:732).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.4 Dataset Tests.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Test shape.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-021.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test shape.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test B=1/4, T=4/6/8; shape/dtype đúng; thay padding không đổi output hợp lệ; không qua storm boundary.
- **Kịch bản tiểu mục:** Assertions kiểm tra shape/dtype/giờ đích/ID độc lập với implementation; test padding làm thay đổi dữ liệu đệm nhưng không đổi output hợp lệ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-022"></a>
## T06-022 — Test dtype.

- **Trạng thái:** pending.
- **Nguồn:** 6.4 Dataset Tests; dòng [733](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:733).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.4 Dataset Tests.
- **Task trước trong tiểu mục:** T06-021; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Test dtype.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-022.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test dtype.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Assertions kiểm tra shape/dtype/giờ đích/ID độc lập với implementation; test padding làm thay đổi dữ liệu đệm nhưng không đổi output hợp lệ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-023"></a>
## T06-023 — Test window.

- **Trạng thái:** pending.
- **Nguồn:** 6.4 Dataset Tests; dòng [734](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:734).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.4 Dataset Tests.
- **Task trước trong tiểu mục:** T06-022; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Test window.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-023.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test window.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Cửa sổ chỉ chứa một storm, input_len đúng; fixture ngắn hơn window không tạo sample; timestamps không đảo hoặc trùng.
- **Kịch bản tiểu mục:** Assertions kiểm tra shape/dtype/giờ đích/ID độc lập với implementation; test padding làm thay đổi dữ liệu đệm nhưng không đổi output hợp lệ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-024"></a>
## T06-024 — Test horizon.

- **Trạng thái:** pending.
- **Nguồn:** 6.4 Dataset Tests; dòng [735](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:735).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.4 Dataset Tests.
- **Task trước trong tiểu mục:** T06-023; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Test horizon.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-024.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test horizon.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Assertions kiểm tra shape/dtype/giờ đích/ID độc lập với implementation; test padding làm thay đổi dữ liệu đệm nhưng không đổi output hợp lệ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-025"></a>
## T06-025 — Test mask.

- **Trạng thái:** pending.
- **Nguồn:** 6.4 Dataset Tests; dòng [736](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:736).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.4 Dataset Tests.
- **Task trước trong tiểu mục:** T06-024; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Test mask.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-025.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test mask.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test B=1/4, T=4/6/8; shape/dtype đúng; thay padding không đổi output hợp lệ; không qua storm boundary.
- **Kịch bản tiểu mục:** Assertions kiểm tra shape/dtype/giờ đích/ID độc lập với implementation; test padding làm thay đổi dữ liệu đệm nhưng không đổi output hợp lệ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t06-026"></a>
## T06-026 — Test storm boundary.

- **Trạng thái:** pending.
- **Nguồn:** 6.4 Dataset Tests; dòng [737](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:737).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G03, G04; contract/fixture của tiểu mục 6.4 Dataset Tests.
- **Task trước trong tiểu mục:** T06-025; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Dữ liệu chưa scale, storm ID đã hợp nhất, policy thời gian; yêu cầu riêng: Test storm boundary.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/datasets/typhoon_dataset.py; tests/test_dataset.py; data/processed/splits/; evidence tại evidence/T06-026.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test storm boundary.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G06, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Assertions kiểm tra shape/dtype/giờ đích/ID độc lập với implementation; test padding làm thay đổi dữ liệu đệm nhưng không đổi output hợp lệ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
