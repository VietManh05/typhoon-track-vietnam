# G01 — Ingestion và nguồn gốc dữ liệu

- Trạng thái: complete; nghiệm thu tại [G01-data-ingestion.md](evidence/G01-data-ingestion.md).
- Hiện trạng: Có downloader/parser/merge; chưa xác nhận hoạt động với tất cả nguồn thật.
- Đầu vào: Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến.
- Gate phụ thuộc: G00.
- Vùng file dự kiến: src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Raw → canonical giữ source, checksum, đơn vị gốc, UTC; dữ liệu lỗi có lý do; retry hữu hạn.

<a id="gate-g01"></a>
## Gate G01

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t01-001"></a>
## T01-001 — Xác định URL/source.

- **Trạng thái:** complete.
- **Nguồn:** 1.1 CMA; dòng [448](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:448).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.1 CMA.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Xác định URL/source.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xác định URL/source.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Mock HTTP 200/404/429/timeout và file rỗng; SHA-256 đúng bytes; retry có giới hạn; chạy lại không nhân bản raw object.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-001.md](evidence/T01-001.md).

<a id="t01-002"></a>
## T01-002 — Viết downloader.

- **Trạng thái:** complete.
- **Nguồn:** 1.1 CMA; dòng [449](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:449).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.1 CMA.
- **Task trước trong tiểu mục:** T01-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Viết downloader.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Viết downloader.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mock HTTP 200/404/429/timeout và file rỗng; SHA-256 đúng bytes; retry có giới hạn; chạy lại không nhân bản raw object.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-002.md](evidence/T01-002.md).

<a id="t01-003"></a>
## T01-003 — Tạo thư mục raw CMA.

- **Trạng thái:** complete.
- **Nguồn:** 1.1 CMA; dòng [450](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:450).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.1 CMA.
- **Task trước trong tiểu mục:** T01-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Tạo thư mục raw CMA.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo thư mục raw CMA.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mock HTTP 200/404/429/timeout và file rỗng; SHA-256 đúng bytes; retry có giới hạn; chạy lại không nhân bản raw object.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-003.md](evidence/T01-003.md).

<a id="t01-004"></a>
## T01-004 — Download một file mẫu.

- **Trạng thái:** complete.
- **Nguồn:** 1.1 CMA; dòng [451](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:451).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.1 CMA.
- **Task trước trong tiểu mục:** T01-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Download một file mẫu.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Download một file mẫu.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Mock bytes xác định và HTTP failure; checksum/raw giữ nguyên; lần tải thật phải có nguồn hợp lệ và evidence riêng.
- **Kịch bản tiểu mục:** Mock HTTP 200/404/429/timeout và file rỗng; SHA-256 đúng bytes; retry có giới hạn; chạy lại không nhân bản raw object.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-004.md](evidence/T01-004.md).

<a id="t01-005"></a>
## T01-005 — Kiểm tra HTTP status.

- **Trạng thái:** complete.
- **Nguồn:** 1.1 CMA; dòng [452](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:452).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.1 CMA.
- **Task trước trong tiểu mục:** T01-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Kiểm tra HTTP status.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra HTTP status.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Mock HTTP 200/404/429/timeout và file rỗng; SHA-256 đúng bytes; retry có giới hạn; chạy lại không nhân bản raw object.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-005.md](evidence/T01-005.md).

<a id="t01-006"></a>
## T01-006 — Retry request.

- **Trạng thái:** complete.
- **Nguồn:** 1.1 CMA; dòng [453](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:453).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.1 CMA.
- **Task trước trong tiểu mục:** T01-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Retry request.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Retry request.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fake transport lỗi rồi thành công; số lần thử/timeout theo cấu hình; hết retry có trạng thái thất bại và log.
- **Kịch bản tiểu mục:** Mock HTTP 200/404/429/timeout và file rỗng; SHA-256 đúng bytes; retry có giới hạn; chạy lại không nhân bản raw object.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-006.md](evidence/T01-006.md).

<a id="t01-007"></a>
## T01-007 — Timeout request.

- **Trạng thái:** complete.
- **Nguồn:** 1.1 CMA; dòng [454](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:454).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.1 CMA.
- **Task trước trong tiểu mục:** T01-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Timeout request.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Timeout request.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fake transport lỗi rồi thành công; số lần thử/timeout theo cấu hình; hết retry có trạng thái thất bại và log.
- **Kịch bản tiểu mục:** Mock HTTP 200/404/429/timeout và file rỗng; SHA-256 đúng bytes; retry có giới hạn; chạy lại không nhân bản raw object.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-007.md](evidence/T01-007.md).

<a id="t01-008"></a>
## T01-008 — Kiểm tra file rỗng.

- **Trạng thái:** complete.
- **Nguồn:** 1.1 CMA; dòng [455](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:455).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.1 CMA.
- **Task trước trong tiểu mục:** T01-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Kiểm tra file rỗng.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra file rỗng.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Mock HTTP 200/404/429/timeout và file rỗng; SHA-256 đúng bytes; retry có giới hạn; chạy lại không nhân bản raw object.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-008.md](evidence/T01-008.md).

<a id="t01-009"></a>
## T01-009 — Tính checksum.

- **Trạng thái:** complete.
- **Nguồn:** 1.1 CMA; dòng [456](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:456).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.1 CMA.
- **Task trước trong tiểu mục:** T01-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Tính checksum.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính checksum.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Cùng bytes cho cùng SHA-256; đổi một byte làm đổi digest; digest gắn với input version.
- **Kịch bản tiểu mục:** Mock HTTP 200/404/429/timeout và file rỗng; SHA-256 đúng bytes; retry có giới hạn; chạy lại không nhân bản raw object.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-009.md](evidence/T01-009.md).

<a id="t01-010"></a>
## T01-010 — Ghi metadata download.

- **Trạng thái:** complete.
- **Nguồn:** 1.1 CMA; dòng [457](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:457).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.1 CMA.
- **Task trước trong tiểu mục:** T01-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Ghi metadata download.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Ghi metadata download.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Mock HTTP 200/404/429/timeout và file rỗng; SHA-256 đúng bytes; retry có giới hạn; chạy lại không nhân bản raw object.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-010.md](evidence/T01-010.md).

<a id="t01-011"></a>
## T01-011 — Download toàn bộ lịch sử.

- **Trạng thái:** complete.
- **Nguồn:** 1.1 CMA; dòng [458](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:458).
- **Loại:** chuẩn bị/test cục bộ trước; chạy thật cần nguồn, credentials và phạm vi vận hành phù hợp.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.1 CMA.
- **Task trước trong tiểu mục:** T01-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Download toàn bộ lịch sử.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Download toàn bộ lịch sử.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Mock bytes xác định và HTTP failure; checksum/raw giữ nguyên; lần tải thật phải có nguồn hợp lệ và evidence riêng.
- **Kịch bản tiểu mục:** Mock HTTP 200/404/429/timeout và file rỗng; SHA-256 đúng bytes; retry có giới hạn; chạy lại không nhân bản raw object.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-011.md](evidence/T01-011.md).

<a id="t01-012"></a>
## T01-012 — Log lỗi từng file.

- **Trạng thái:** complete.
- **Nguồn:** 1.1 CMA; dòng [459](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:459).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.1 CMA.
- **Task trước trong tiểu mục:** T01-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Log lỗi từng file.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Log lỗi từng file.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Mock HTTP 200/404/429/timeout và file rỗng; SHA-256 đúng bytes; retry có giới hạn; chạy lại không nhân bản raw object.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-012.md](evidence/T01-012.md).

<a id="t01-013"></a>
## T01-013 — Đọc file raw.

- **Trạng thái:** complete.
- **Nguồn:** 1.2 CMA Parser; dòng [464](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:464).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.2 CMA Parser.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Đọc file raw.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Đọc file raw.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture CMA gồm header, nhiều cơn bão, tọa độ theo đơn vị nguồn, missing sentinel và dòng lỗi; expected rows/units được viết độc lập.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-013.md](evidence/T01-013.md).

<a id="t01-014"></a>
## T01-014 — Nhận diện storm ID.

- **Trạng thái:** complete.
- **Nguồn:** 1.2 CMA Parser; dòng [465](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:465).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.2 CMA Parser.
- **Task trước trong tiểu mục:** T01-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Nhận diện storm ID.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Nhận diện storm ID.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture CMA gồm header, nhiều cơn bão, tọa độ theo đơn vị nguồn, missing sentinel và dòng lỗi; expected rows/units được viết độc lập.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-014.md](evidence/T01-014.md).

<a id="t01-015"></a>
## T01-015 — Parse timestamp.

- **Trạng thái:** complete.
- **Nguồn:** 1.2 CMA Parser; dòng [466](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:466).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.2 CMA Parser.
- **Task trước trong tiểu mục:** T01-014; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Parse timestamp.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Parse timestamp.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt.
- **Kịch bản tiểu mục:** Fixture CMA gồm header, nhiều cơn bão, tọa độ theo đơn vị nguồn, missing sentinel và dòng lỗi; expected rows/units được viết độc lập.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-015.md](evidence/T01-015.md).

<a id="t01-016"></a>
## T01-016 — Parse latitude.

- **Trạng thái:** complete.
- **Nguồn:** 1.2 CMA Parser; dòng [467](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:467).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.2 CMA Parser.
- **Task trước trong tiểu mục:** T01-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Parse latitude.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Parse latitude.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hợp lệ/ngoài biên/NaN/Inf và wrap longitude; output giữ đúng đơn vị tọa độ.
- **Kịch bản tiểu mục:** Fixture CMA gồm header, nhiều cơn bão, tọa độ theo đơn vị nguồn, missing sentinel và dòng lỗi; expected rows/units được viết độc lập.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-016.md](evidence/T01-016.md).

<a id="t01-017"></a>
## T01-017 — Parse longitude.

- **Trạng thái:** complete.
- **Nguồn:** 1.2 CMA Parser; dòng [468](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:468).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.2 CMA Parser.
- **Task trước trong tiểu mục:** T01-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Parse longitude.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Parse longitude.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hợp lệ/ngoài biên/NaN/Inf và wrap longitude; output giữ đúng đơn vị tọa độ.
- **Kịch bản tiểu mục:** Fixture CMA gồm header, nhiều cơn bão, tọa độ theo đơn vị nguồn, missing sentinel và dòng lỗi; expected rows/units được viết độc lập.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-017.md](evidence/T01-017.md).

<a id="t01-018"></a>
## T01-018 — Parse wind.

- **Trạng thái:** complete.
- **Nguồn:** 1.2 CMA Parser; dòng [469](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:469).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.2 CMA Parser.
- **Task trước trong tiểu mục:** T01-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Parse wind.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Parse wind.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Fixture CMA gồm header, nhiều cơn bão, tọa độ theo đơn vị nguồn, missing sentinel và dòng lỗi; expected rows/units được viết độc lập.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-018.md](evidence/T01-018.md).

<a id="t01-019"></a>
## T01-019 — Parse pressure nếu có.

- **Trạng thái:** complete.
- **Nguồn:** 1.2 CMA Parser; dòng [470](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:470).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.2 CMA Parser.
- **Task trước trong tiểu mục:** T01-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Parse pressure nếu có.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Parse pressure nếu có.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Fixture CMA gồm header, nhiều cơn bão, tọa độ theo đơn vị nguồn, missing sentinel và dòng lỗi; expected rows/units được viết độc lập.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-019.md](evidence/T01-019.md).

<a id="t01-020"></a>
## T01-020 — Chuẩn hóa đơn vị.

- **Trạng thái:** complete.
- **Nguồn:** 1.2 CMA Parser; dòng [471](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:471).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.2 CMA Parser.
- **Task trước trong tiểu mục:** T01-019; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Chuẩn hóa đơn vị.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-020.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chuẩn hóa đơn vị.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Fixture CMA gồm header, nhiều cơn bão, tọa độ theo đơn vị nguồn, missing sentinel và dòng lỗi; expected rows/units được viết độc lập.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-020.md](evidence/T01-020.md).

<a id="t01-021"></a>
## T01-021 — Xử lý missing.

- **Trạng thái:** complete.
- **Nguồn:** 1.2 CMA Parser; dòng [472](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:472).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.2 CMA Parser.
- **Task trước trong tiểu mục:** T01-020; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Xử lý missing.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-021.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xử lý missing.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Fixture CMA gồm header, nhiều cơn bão, tọa độ theo đơn vị nguồn, missing sentinel và dòng lỗi; expected rows/units được viết độc lập.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-021.md](evidence/T01-021.md).

<a id="t01-022"></a>
## T01-022 — Xuất DataFrame chuẩn.

- **Trạng thái:** complete.
- **Nguồn:** 1.2 CMA Parser; dòng [473](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:473).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.2 CMA Parser.
- **Task trước trong tiểu mục:** T01-021; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Xuất DataFrame chuẩn.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-022.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xuất DataFrame chuẩn.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture CMA gồm header, nhiều cơn bão, tọa độ theo đơn vị nguồn, missing sentinel và dòng lỗi; expected rows/units được viết độc lập.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-022.md](evidence/T01-022.md).

<a id="t01-023"></a>
## T01-023 — Xuất Parquet.

- **Trạng thái:** complete.
- **Nguồn:** 1.2 CMA Parser; dòng [474](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:474).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.2 CMA Parser.
- **Task trước trong tiểu mục:** T01-022; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Xuất Parquet.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-023.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xuất Parquet.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture CMA gồm header, nhiều cơn bão, tọa độ theo đơn vị nguồn, missing sentinel và dòng lỗi; expected rows/units được viết độc lập.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-023.md](evidence/T01-023.md).

<a id="t01-024"></a>
## T01-024 — Viết test parser.

- **Trạng thái:** complete.
- **Nguồn:** 1.2 CMA Parser; dòng [475](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:475).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.2 CMA Parser.
- **Task trước trong tiểu mục:** T01-023; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Viết test parser.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-024.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Viết test parser.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Fixture CMA gồm header, nhiều cơn bão, tọa độ theo đơn vị nguồn, missing sentinel và dòng lỗi; expected rows/units được viết độc lập.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-024.md](evidence/T01-024.md).

<a id="t01-025"></a>
## T01-025 — Tạo downloader.

- **Trạng thái:** complete.
- **Nguồn:** 1.3 IBTrACS; dòng [480](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:480).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.3 IBTrACS.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Tạo downloader.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-025.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo downloader.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture IBTrACS nhiều agency, SID, ATCF ID, missing và dòng units; không gộp sai bão khi thiếu khóa quốc tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-025.md](evidence/T01-025.md).

<a id="t01-026"></a>
## T01-026 — Cache file.

- **Trạng thái:** complete.
- **Nguồn:** 1.3 IBTrACS; dòng [481](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:481).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.3 IBTrACS.
- **Task trước trong tiểu mục:** T01-025; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Cache file.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-026.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cache file.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hit/miss/expiry, observation sửa/model đổi và outage; cache key bao gồm input+model revision.
- **Kịch bản tiểu mục:** Fixture IBTrACS nhiều agency, SID, ATCF ID, missing và dòng units; không gộp sai bão khi thiếu khóa quốc tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-026.md](evidence/T01-026.md).

<a id="t01-027"></a>
## T01-027 — Tạo parser.

- **Trạng thái:** complete.
- **Nguồn:** 1.3 IBTrACS; dòng [482](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:482).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.3 IBTrACS.
- **Task trước trong tiểu mục:** T01-026; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Tạo parser.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-027.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo parser.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture IBTrACS nhiều agency, SID, ATCF ID, missing và dòng units; không gộp sai bão khi thiếu khóa quốc tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-027.md](evidence/T01-027.md).

<a id="t01-028"></a>
## T01-028 — Chọn agency fields.

- **Trạng thái:** complete.
- **Nguồn:** 1.3 IBTrACS; dòng [483](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:483).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.3 IBTrACS.
- **Task trước trong tiểu mục:** T01-027; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Chọn agency fields.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-028.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chọn agency fields.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture IBTrACS nhiều agency, SID, ATCF ID, missing và dòng units; không gộp sai bão khi thiếu khóa quốc tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-028.md](evidence/T01-028.md).

<a id="t01-029"></a>
## T01-029 — Chuẩn hóa storm ID.

- **Trạng thái:** complete.
- **Nguồn:** 1.3 IBTrACS; dòng [484](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:484).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.3 IBTrACS.
- **Task trước trong tiểu mục:** T01-028; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Chuẩn hóa storm ID.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-029.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chuẩn hóa storm ID.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture IBTrACS nhiều agency, SID, ATCF ID, missing và dòng units; không gộp sai bão khi thiếu khóa quốc tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-029.md](evidence/T01-029.md).

<a id="t01-030"></a>
## T01-030 — Chuẩn hóa timestamp.

- **Trạng thái:** complete.
- **Nguồn:** 1.3 IBTrACS; dòng [485](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:485).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.3 IBTrACS.
- **Task trước trong tiểu mục:** T01-029; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Chuẩn hóa timestamp.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-030.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chuẩn hóa timestamp.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt.
- **Kịch bản tiểu mục:** Fixture IBTrACS nhiều agency, SID, ATCF ID, missing và dòng units; không gộp sai bão khi thiếu khóa quốc tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-030.md](evidence/T01-030.md).

<a id="t01-031"></a>
## T01-031 — Chuẩn hóa lat/lon.

- **Trạng thái:** complete.
- **Nguồn:** 1.3 IBTrACS; dòng [486](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:486).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.3 IBTrACS.
- **Task trước trong tiểu mục:** T01-030; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Chuẩn hóa lat/lon.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-031.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chuẩn hóa lat/lon.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hợp lệ/ngoài biên/NaN/Inf và wrap longitude; output giữ đúng đơn vị tọa độ.
- **Kịch bản tiểu mục:** Fixture IBTrACS nhiều agency, SID, ATCF ID, missing và dòng units; không gộp sai bão khi thiếu khóa quốc tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-031.md](evidence/T01-031.md).

<a id="t01-032"></a>
## T01-032 — Chuẩn hóa wind/pressure.

- **Trạng thái:** complete.
- **Nguồn:** 1.3 IBTrACS; dòng [487](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:487).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.3 IBTrACS.
- **Task trước trong tiểu mục:** T01-031; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Chuẩn hóa wind/pressure.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-032.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chuẩn hóa wind/pressure.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Fixture IBTrACS nhiều agency, SID, ATCF ID, missing và dòng units; không gộp sai bão khi thiếu khóa quốc tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-032.md](evidence/T01-032.md).

<a id="t01-033"></a>
## T01-033 — Lưu source agency.

- **Trạng thái:** complete.
- **Nguồn:** 1.3 IBTrACS; dòng [488](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:488).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.3 IBTrACS.
- **Task trước trong tiểu mục:** T01-032; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Lưu source agency.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-033.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu source agency.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Fixture IBTrACS nhiều agency, SID, ATCF ID, missing và dòng units; không gộp sai bão khi thiếu khóa quốc tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-033.md](evidence/T01-033.md).

<a id="t01-034"></a>
## T01-034 — Validate dữ liệu.

- **Trạng thái:** complete.
- **Nguồn:** 1.3 IBTrACS; dòng [489](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:489).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.3 IBTrACS.
- **Task trước trong tiểu mục:** T01-033; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Validate dữ liệu.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-034.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Validate dữ liệu.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Fixture IBTrACS nhiều agency, SID, ATCF ID, missing và dòng units; không gộp sai bão khi thiếu khóa quốc tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-034.md](evidence/T01-034.md).

<a id="t01-035"></a>
## T01-035 — Export Parquet.

- **Trạng thái:** complete.
- **Nguồn:** 1.3 IBTrACS; dòng [490](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:490).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.3 IBTrACS.
- **Task trước trong tiểu mục:** T01-034; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Export Parquet.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-035.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Export Parquet.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture IBTrACS nhiều agency, SID, ATCF ID, missing và dòng units; không gộp sai bão khi thiếu khóa quốc tế.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-035.md](evidence/T01-035.md).

<a id="t01-036"></a>
## T01-036 — Tạo provider.

- **Trạng thái:** complete.
- **Nguồn:** 1.4 JMA; dòng [493](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:493).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.4 JMA.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Tạo provider.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-036.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo provider.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture JMA fixed-width/grade/time và missing; mapping intensity phải căn cứ định dạng nguồn, không suy từ tên lớp.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-036.md](evidence/T01-036.md).

<a id="t01-037"></a>
## T01-037 — Downloader.

- **Trạng thái:** complete.
- **Nguồn:** 1.4 JMA; dòng [494](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:494).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.4 JMA.
- **Task trước trong tiểu mục:** T01-036; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Downloader.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-037.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Downloader.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture JMA fixed-width/grade/time và missing; mapping intensity phải căn cứ định dạng nguồn, không suy từ tên lớp.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-037.md](evidence/T01-037.md).

<a id="t01-038"></a>
## T01-038 — Parser.

- **Trạng thái:** complete.
- **Nguồn:** 1.4 JMA; dòng [495](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:495).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.4 JMA.
- **Task trước trong tiểu mục:** T01-037; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Parser.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-038.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Parser.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture JMA fixed-width/grade/time và missing; mapping intensity phải căn cứ định dạng nguồn, không suy từ tên lớp.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-038.md](evidence/T01-038.md).

<a id="t01-039"></a>
## T01-039 — Mapping schema.

- **Trạng thái:** complete.
- **Nguồn:** 1.4 JMA; dòng [496](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:496).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.4 JMA.
- **Task trước trong tiểu mục:** T01-038; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Mapping schema.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-039.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Mapping schema.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture JMA fixed-width/grade/time và missing; mapping intensity phải căn cứ định dạng nguồn, không suy từ tên lớp.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-039.md](evidence/T01-039.md).

<a id="t01-040"></a>
## T01-040 — Unit conversion.

- **Trạng thái:** complete.
- **Nguồn:** 1.4 JMA; dòng [497](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:497).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.4 JMA.
- **Task trước trong tiểu mục:** T01-039; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Unit conversion.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-040.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Unit conversion.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Fixture JMA fixed-width/grade/time và missing; mapping intensity phải căn cứ định dạng nguồn, không suy từ tên lớp.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-040.md](evidence/T01-040.md).

<a id="t01-041"></a>
## T01-041 — Validation.

- **Trạng thái:** complete.
- **Nguồn:** 1.4 JMA; dòng [498](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:498).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.4 JMA.
- **Task trước trong tiểu mục:** T01-040; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Validation.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-041.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Validation.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Fixture JMA fixed-width/grade/time và missing; mapping intensity phải căn cứ định dạng nguồn, không suy từ tên lớp.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-041.md](evidence/T01-041.md).

<a id="t01-042"></a>
## T01-042 — Export.

- **Trạng thái:** complete.
- **Nguồn:** 1.4 JMA; dòng [499](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:499).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.4 JMA.
- **Task trước trong tiểu mục:** T01-041; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Export.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-042.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Export.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture JMA fixed-width/grade/time và missing; mapping intensity phải căn cứ định dạng nguồn, không suy từ tên lớp.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-042.md](evidence/T01-042.md).

<a id="t01-043"></a>
## T01-043 — Tạo provider.

- **Trạng thái:** complete.
- **Nguồn:** 1.5 JTWC; dòng [502](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:502).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.5 JTWC.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Tạo provider.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-043.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo provider.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture JTWC ATCF có N/S/E/W, advisory trùng, basin và năm; chọn đúng bản ghi quan trắc, không trộn forecast thành observed.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-043.md](evidence/T01-043.md).

<a id="t01-044"></a>
## T01-044 — Downloader.

- **Trạng thái:** complete.
- **Nguồn:** 1.5 JTWC; dòng [503](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:503).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.5 JTWC.
- **Task trước trong tiểu mục:** T01-043; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Downloader.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-044.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Downloader.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture JTWC ATCF có N/S/E/W, advisory trùng, basin và năm; chọn đúng bản ghi quan trắc, không trộn forecast thành observed.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-044.md](evidence/T01-044.md).

<a id="t01-045"></a>
## T01-045 — Parser.

- **Trạng thái:** complete.
- **Nguồn:** 1.5 JTWC; dòng [504](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:504).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.5 JTWC.
- **Task trước trong tiểu mục:** T01-044; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Parser.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-045.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Parser.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture JTWC ATCF có N/S/E/W, advisory trùng, basin và năm; chọn đúng bản ghi quan trắc, không trộn forecast thành observed.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-045.md](evidence/T01-045.md).

<a id="t01-046"></a>
## T01-046 — Mapping schema.

- **Trạng thái:** complete.
- **Nguồn:** 1.5 JTWC; dòng [505](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:505).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.5 JTWC.
- **Task trước trong tiểu mục:** T01-045; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Mapping schema.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-046.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Mapping schema.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture JTWC ATCF có N/S/E/W, advisory trùng, basin và năm; chọn đúng bản ghi quan trắc, không trộn forecast thành observed.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-046.md](evidence/T01-046.md).

<a id="t01-047"></a>
## T01-047 — Unit conversion.

- **Trạng thái:** complete.
- **Nguồn:** 1.5 JTWC; dòng [506](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:506).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.5 JTWC.
- **Task trước trong tiểu mục:** T01-046; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Unit conversion.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-047.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Unit conversion.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Fixture JTWC ATCF có N/S/E/W, advisory trùng, basin và năm; chọn đúng bản ghi quan trắc, không trộn forecast thành observed.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-047.md](evidence/T01-047.md).

<a id="t01-048"></a>
## T01-048 — Validation.

- **Trạng thái:** complete.
- **Nguồn:** 1.5 JTWC; dòng [507](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:507).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.5 JTWC.
- **Task trước trong tiểu mục:** T01-047; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Validation.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-048.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Validation.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Fixture JTWC ATCF có N/S/E/W, advisory trùng, basin và năm; chọn đúng bản ghi quan trắc, không trộn forecast thành observed.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-048.md](evidence/T01-048.md).

<a id="t01-049"></a>
## T01-049 — Export.

- **Trạng thái:** complete.
- **Nguồn:** 1.5 JTWC; dòng [508](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:508).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.5 JTWC.
- **Task trước trong tiểu mục:** T01-048; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Export.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-049.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Export.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture JTWC ATCF có N/S/E/W, advisory trùng, basin và năm; chọn đúng bản ghi quan trắc, không trộn forecast thành observed.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-049.md](evidence/T01-049.md).

<a id="t01-050"></a>
## T01-050 — Xác định nguồn được phép sử dụng.

- **Trạng thái:** complete.
- **Nguồn:** 1.6 NCHMF; dòng [511](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:511).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.6 NCHMF.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Xác định nguồn được phép sử dụng.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-050.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xác định nguồn được phép sử dụng.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Tách thời điểm phát hành, valid time và thời điểm tải; chuyển VN UTC+7 đúng; lưu văn bản gốc; fixture phải đại diện nguồn được phép dùng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-050.md](evidence/T01-050.md).

<a id="t01-051"></a>
## T01-051 — Xác định format.

- **Trạng thái:** complete.
- **Nguồn:** 1.6 NCHMF; dòng [512](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:512).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.6 NCHMF.
- **Task trước trong tiểu mục:** T01-050; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Xác định format.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-051.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xác định format.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Tách thời điểm phát hành, valid time và thời điểm tải; chuyển VN UTC+7 đúng; lưu văn bản gốc; fixture phải đại diện nguồn được phép dùng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-051.md](evidence/T01-051.md).

<a id="t01-052"></a>
## T01-052 — Tạo provider interface.

- **Trạng thái:** complete.
- **Nguồn:** 1.6 NCHMF; dòng [513](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:513).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.6 NCHMF.
- **Task trước trong tiểu mục:** T01-051; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Tạo provider interface.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-052.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo provider interface.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Tách thời điểm phát hành, valid time và thời điểm tải; chuyển VN UTC+7 đúng; lưu văn bản gốc; fixture phải đại diện nguồn được phép dùng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-052.md](evidence/T01-052.md).

<a id="t01-053"></a>
## T01-053 — Viết parser tương ứng với nguồn thực tế.

- **Trạng thái:** complete.
- **Nguồn:** 1.6 NCHMF; dòng [514](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:514).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.6 NCHMF.
- **Task trước trong tiểu mục:** T01-052; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Viết parser tương ứng với nguồn thực tế.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-053.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Viết parser tương ứng với nguồn thực tế.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Tách thời điểm phát hành, valid time và thời điểm tải; chuyển VN UTC+7 đúng; lưu văn bản gốc; fixture phải đại diện nguồn được phép dùng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-053.md](evidence/T01-053.md).

<a id="t01-054"></a>
## T01-054 — Parse thời điểm phát hành.

- **Trạng thái:** complete.
- **Nguồn:** 1.6 NCHMF; dòng [515](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:515).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.6 NCHMF.
- **Task trước trong tiểu mục:** T01-053; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Parse thời điểm phát hành.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-054.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Parse thời điểm phát hành.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt.
- **Kịch bản tiểu mục:** Tách thời điểm phát hành, valid time và thời điểm tải; chuyển VN UTC+7 đúng; lưu văn bản gốc; fixture phải đại diện nguồn được phép dùng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-054.md](evidence/T01-054.md).

<a id="t01-055"></a>
## T01-055 — Parse vị trí tâm bão.

- **Trạng thái:** complete.
- **Nguồn:** 1.6 NCHMF; dòng [516](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:516).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.6 NCHMF.
- **Task trước trong tiểu mục:** T01-054; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Parse vị trí tâm bão.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-055.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Parse vị trí tâm bão.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Tách thời điểm phát hành, valid time và thời điểm tải; chuyển VN UTC+7 đúng; lưu văn bản gốc; fixture phải đại diện nguồn được phép dùng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-055.md](evidence/T01-055.md).

<a id="t01-056"></a>
## T01-056 — Parse cường độ.

- **Trạng thái:** complete.
- **Nguồn:** 1.6 NCHMF; dòng [517](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:517).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.6 NCHMF.
- **Task trước trong tiểu mục:** T01-055; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Parse cường độ.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-056.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Parse cường độ.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Tách thời điểm phát hành, valid time và thời điểm tải; chuyển VN UTC+7 đúng; lưu văn bản gốc; fixture phải đại diện nguồn được phép dùng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-056.md](evidence/T01-056.md).

<a id="t01-057"></a>
## T01-057 — Parse dự báo nếu nguồn cung cấp.

- **Trạng thái:** complete.
- **Nguồn:** 1.6 NCHMF; dòng [518](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:518).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.6 NCHMF.
- **Task trước trong tiểu mục:** T01-056; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Parse dự báo nếu nguồn cung cấp.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-057.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Parse dự báo nếu nguồn cung cấp.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Tách thời điểm phát hành, valid time và thời điểm tải; chuyển VN UTC+7 đúng; lưu văn bản gốc; fixture phải đại diện nguồn được phép dùng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-057.md](evidence/T01-057.md).

<a id="t01-058"></a>
## T01-058 — Lưu bản gốc.

- **Trạng thái:** complete.
- **Nguồn:** 1.6 NCHMF; dòng [519](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:519).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.6 NCHMF.
- **Task trước trong tiểu mục:** T01-057; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Lưu bản gốc.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-058.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu bản gốc.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Tách thời điểm phát hành, valid time và thời điểm tải; chuyển VN UTC+7 đúng; lưu văn bản gốc; fixture phải đại diện nguồn được phép dùng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-058.md](evidence/T01-058.md).

<a id="t01-059"></a>
## T01-059 — Lưu metadata.

- **Trạng thái:** complete.
- **Nguồn:** 1.6 NCHMF; dòng [520](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:520).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.6 NCHMF.
- **Task trước trong tiểu mục:** T01-058; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Lưu metadata.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-059.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu metadata.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Tách thời điểm phát hành, valid time và thời điểm tải; chuyển VN UTC+7 đúng; lưu văn bản gốc; fixture phải đại diện nguồn được phép dùng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-059.md](evidence/T01-059.md).

<a id="t01-060"></a>
## T01-060 — Test với dữ liệu mẫu.

- **Trạng thái:** complete.
- **Nguồn:** 1.6 NCHMF; dòng [521](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:521).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.6 NCHMF.
- **Task trước trong tiểu mục:** T01-059; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Test với dữ liệu mẫu.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-060.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test với dữ liệu mẫu.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Tách thời điểm phát hành, valid time và thời điểm tải; chuyển VN UTC+7 đúng; lưu văn bản gốc; fixture phải đại diện nguồn được phép dùng.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-060.md](evidence/T01-060.md).

<a id="t01-061"></a>
## T01-061 — Chuẩn hóa tên cột.

- **Trạng thái:** complete.
- **Nguồn:** 1.7 Source Merge; dòng [526](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:526).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.7 Source Merge.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Chuẩn hóa tên cột.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-061.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chuẩn hóa tên cột.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Hai agency cùng bão/cùng giờ, xung đột vị trí và hai bão gần nhau được test riêng; giữ contributing_sources và lý do chọn nguồn.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-061.md](evidence/T01-061.md).

<a id="t01-062"></a>
## T01-062 — Chuẩn hóa timezone.

- **Trạng thái:** complete.
- **Nguồn:** 1.7 Source Merge; dòng [527](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:527).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.7 Source Merge.
- **Task trước trong tiểu mục:** T01-061; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Chuẩn hóa timezone.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-062.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chuẩn hóa timezone.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt.
- **Kịch bản tiểu mục:** Hai agency cùng bão/cùng giờ, xung đột vị trí và hai bão gần nhau được test riêng; giữ contributing_sources và lý do chọn nguồn.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-062.md](evidence/T01-062.md).

<a id="t01-063"></a>
## T01-063 — Chuẩn hóa đơn vị.

- **Trạng thái:** complete.
- **Nguồn:** 1.7 Source Merge; dòng [528](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:528).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.7 Source Merge.
- **Task trước trong tiểu mục:** T01-062; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Chuẩn hóa đơn vị.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-063.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chuẩn hóa đơn vị.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Hai agency cùng bão/cùng giờ, xung đột vị trí và hai bão gần nhau được test riêng; giữ contributing_sources và lý do chọn nguồn.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-063.md](evidence/T01-063.md).

<a id="t01-064"></a>
## T01-064 — Chuẩn hóa storm ID.

- **Trạng thái:** complete.
- **Nguồn:** 1.7 Source Merge; dòng [529](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:529).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.7 Source Merge.
- **Task trước trong tiểu mục:** T01-063; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Chuẩn hóa storm ID.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-064.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chuẩn hóa storm ID.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Hai agency cùng bão/cùng giờ, xung đột vị trí và hai bão gần nhau được test riêng; giữ contributing_sources và lý do chọn nguồn.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-064.md](evidence/T01-064.md).

<a id="t01-065"></a>
## T01-065 — Match storm giữa các nguồn.

- **Trạng thái:** complete.
- **Nguồn:** 1.7 Source Merge; dòng [530](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:530).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.7 Source Merge.
- **Task trước trong tiểu mục:** T01-064; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Match storm giữa các nguồn.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-065.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Match storm giữa các nguồn.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Hai agency cùng bão/cùng giờ, xung đột vị trí và hai bão gần nhau được test riêng; giữ contributing_sources và lý do chọn nguồn.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-065.md](evidence/T01-065.md).

<a id="t01-066"></a>
## T01-066 — Match timestamp.

- **Trạng thái:** complete.
- **Nguồn:** 1.7 Source Merge; dòng [531](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:531).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.7 Source Merge.
- **Task trước trong tiểu mục:** T01-065; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Match timestamp.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-066.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Match timestamp.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt.
- **Kịch bản tiểu mục:** Hai agency cùng bão/cùng giờ, xung đột vị trí và hai bão gần nhau được test riêng; giữ contributing_sources và lý do chọn nguồn.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-066.md](evidence/T01-066.md).

<a id="t01-067"></a>
## T01-067 — Tính khoảng cách giữa các vị trí.

- **Trạng thái:** complete.
- **Nguồn:** 1.7 Source Merge; dòng [532](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:532).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.7 Source Merge.
- **Task trước trong tiểu mục:** T01-066; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Tính khoảng cách giữa các vị trí.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-067.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tính khoảng cách giữa các vị trí.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Điểm trùng cho 0 km; cặp điểm chuẩn khớp dung sai; wrap longitude không tạo khoảng cách vòng trái đất.
- **Kịch bản tiểu mục:** Hai agency cùng bão/cùng giờ, xung đột vị trí và hai bão gần nhau được test riêng; giữ contributing_sources và lý do chọn nguồn.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-067.md](evidence/T01-067.md).

<a id="t01-068"></a>
## T01-068 — Phát hiện duplicate.

- **Trạng thái:** complete.
- **Nguồn:** 1.7 Source Merge; dòng [533](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:533).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.7 Source Merge.
- **Task trước trong tiểu mục:** T01-067; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Phát hiện duplicate.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-068.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Phát hiện duplicate.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Hai agency cùng bão/cùng giờ, xung đột vị trí và hai bão gần nhau được test riêng; giữ contributing_sources và lý do chọn nguồn.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-068.md](evidence/T01-068.md).

<a id="t01-069"></a>
## T01-069 — Đánh dấu conflict.

- **Trạng thái:** complete.
- **Nguồn:** 1.7 Source Merge; dòng [534](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:534).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.7 Source Merge.
- **Task trước trong tiểu mục:** T01-068; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Đánh dấu conflict.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-069.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Đánh dấu conflict.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Hai agency cùng bão/cùng giờ, xung đột vị trí và hai bão gần nhau được test riêng; giữ contributing_sources và lý do chọn nguồn.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-069.md](evidence/T01-069.md).

<a id="t01-070"></a>
## T01-070 — Xác định priority source.

- **Trạng thái:** complete.
- **Nguồn:** 1.7 Source Merge; dòng [535](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:535).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.7 Source Merge.
- **Task trước trong tiểu mục:** T01-069; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Xác định priority source.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-070.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Xác định priority source.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Hai agency cùng bão/cùng giờ, xung đột vị trí và hai bão gần nhau được test riêng; giữ contributing_sources và lý do chọn nguồn.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-070.md](evidence/T01-070.md).

<a id="t01-071"></a>
## T01-071 — Tạo master dataset.

- **Trạng thái:** complete.
- **Nguồn:** 1.7 Source Merge; dòng [536](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:536).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.7 Source Merge.
- **Task trước trong tiểu mục:** T01-070; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Tạo master dataset.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-071.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo master dataset.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Hai agency cùng bão/cùng giờ, xung đột vị trí và hai bão gần nhau được test riêng; giữ contributing_sources và lý do chọn nguồn.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-071.md](evidence/T01-071.md).

<a id="t01-072"></a>
## T01-072 — Lưu provenance.

- **Trạng thái:** complete.
- **Nguồn:** 1.7 Source Merge; dòng [537](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:537).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.7 Source Merge.
- **Task trước trong tiểu mục:** T01-071; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Lưu provenance.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-072.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu provenance.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Hai agency cùng bão/cùng giờ, xung đột vị trí và hai bão gần nhau được test riêng; giữ contributing_sources và lý do chọn nguồn.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-072.md](evidence/T01-072.md).

<a id="t01-073"></a>
## T01-073 — Validate latitude.

- **Trạng thái:** complete.
- **Nguồn:** 1.8 Data Validation; dòng [540](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:540).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.8 Data Validation.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Validate latitude.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-073.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Validate latitude.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hợp lệ/ngoài biên/NaN/Inf và wrap longitude; output giữ đúng đơn vị tọa độ.
- **Kịch bản tiểu mục:** Test đúng biên và ngoài biên, NaN/Inf, timestamp thiếu múi giờ, duplicate và bước nhảy lớn; báo cáo reject/flag có reason code.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-073.md](evidence/T01-073.md).

<a id="t01-074"></a>
## T01-074 — Validate longitude.

- **Trạng thái:** complete.
- **Nguồn:** 1.8 Data Validation; dòng [541](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:541).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.8 Data Validation.
- **Task trước trong tiểu mục:** T01-073; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Validate longitude.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-074.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Validate longitude.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hợp lệ/ngoài biên/NaN/Inf và wrap longitude; output giữ đúng đơn vị tọa độ.
- **Kịch bản tiểu mục:** Test đúng biên và ngoài biên, NaN/Inf, timestamp thiếu múi giờ, duplicate và bước nhảy lớn; báo cáo reject/flag có reason code.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-074.md](evidence/T01-074.md).

<a id="t01-075"></a>
## T01-075 — Validate timestamp.

- **Trạng thái:** complete.
- **Nguồn:** 1.8 Data Validation; dòng [542](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:542).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.8 Data Validation.
- **Task trước trong tiểu mục:** T01-074; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Validate timestamp.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-075.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Validate timestamp.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt.
- **Kịch bản tiểu mục:** Test đúng biên và ngoài biên, NaN/Inf, timestamp thiếu múi giờ, duplicate và bước nhảy lớn; báo cáo reject/flag có reason code.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-075.md](evidence/T01-075.md).

<a id="t01-076"></a>
## T01-076 — Validate wind.

- **Trạng thái:** complete.
- **Nguồn:** 1.8 Data Validation; dòng [543](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:543).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.8 Data Validation.
- **Task trước trong tiểu mục:** T01-075; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Validate wind.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-076.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Validate wind.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Test đúng biên và ngoài biên, NaN/Inf, timestamp thiếu múi giờ, duplicate và bước nhảy lớn; báo cáo reject/flag có reason code.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-076.md](evidence/T01-076.md).

<a id="t01-077"></a>
## T01-077 — Validate pressure.

- **Trạng thái:** complete.
- **Nguồn:** 1.8 Data Validation; dòng [544](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:544).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.8 Data Validation.
- **Task trước trong tiểu mục:** T01-076; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Validate pressure.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-077.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Validate pressure.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Test đúng biên và ngoài biên, NaN/Inf, timestamp thiếu múi giờ, duplicate và bước nhảy lớn; báo cáo reject/flag có reason code.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-077.md](evidence/T01-077.md).

<a id="t01-078"></a>
## T01-078 — Kiểm tra duplicate.

- **Trạng thái:** complete.
- **Nguồn:** 1.8 Data Validation; dòng [545](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:545).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.8 Data Validation.
- **Task trước trong tiểu mục:** T01-077; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Kiểm tra duplicate.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-078.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra duplicate.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Test đúng biên và ngoài biên, NaN/Inf, timestamp thiếu múi giờ, duplicate và bước nhảy lớn; báo cáo reject/flag có reason code.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-078.md](evidence/T01-078.md).

<a id="t01-079"></a>
## T01-079 — Kiểm tra missing.

- **Trạng thái:** complete.
- **Nguồn:** 1.8 Data Validation; dòng [546](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:546).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.8 Data Validation.
- **Task trước trong tiểu mục:** T01-078; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Kiểm tra missing.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-079.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra missing.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Test đúng biên và ngoài biên, NaN/Inf, timestamp thiếu múi giờ, duplicate và bước nhảy lớn; báo cáo reject/flag có reason code.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-079.md](evidence/T01-079.md).

<a id="t01-080"></a>
## T01-080 — Kiểm tra timestamp tăng dần.

- **Trạng thái:** complete.
- **Nguồn:** 1.8 Data Validation; dòng [547](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:547).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.8 Data Validation.
- **Task trước trong tiểu mục:** T01-079; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Kiểm tra timestamp tăng dần.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-080.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra timestamp tăng dần.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt.
- **Kịch bản tiểu mục:** Test đúng biên và ngoài biên, NaN/Inf, timestamp thiếu múi giờ, duplicate và bước nhảy lớn; báo cáo reject/flag có reason code.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-080.md](evidence/T01-080.md).

<a id="t01-081"></a>
## T01-081 — Kiểm tra vị trí nhảy bất thường.

- **Trạng thái:** complete.
- **Nguồn:** 1.8 Data Validation; dòng [548](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:548).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.8 Data Validation.
- **Task trước trong tiểu mục:** T01-080; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Kiểm tra vị trí nhảy bất thường.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-081.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra vị trí nhảy bất thường.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Test đúng biên và ngoài biên, NaN/Inf, timestamp thiếu múi giờ, duplicate và bước nhảy lớn; báo cáo reject/flag có reason code.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-081.md](evidence/T01-081.md).

<a id="t01-082"></a>
## T01-082 — Gắn cờ suspicious thay vì âm thầm xóa.

- **Trạng thái:** complete.
- **Nguồn:** 1.8 Data Validation; dòng [549](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:549).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.8 Data Validation.
- **Task trước trong tiểu mục:** T01-081; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Gắn cờ suspicious thay vì âm thầm xóa.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-082.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Gắn cờ suspicious thay vì âm thầm xóa.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Test đúng biên và ngoài biên, NaN/Inf, timestamp thiếu múi giờ, duplicate và bước nhảy lớn; báo cáo reject/flag có reason code.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-082.md](evidence/T01-082.md).

<a id="t01-083"></a>
## T01-083 — Sinh báo cáo quality.

- **Trạng thái:** complete.
- **Nguồn:** 1.8 Data Validation; dòng [550](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:550).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 1.8 Data Validation.
- **Task trước trong tiểu mục:** T01-082; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Mẫu nguồn có giấy phép/điều kiện sử dụng và dữ liệu raw bất biến; yêu cầu riêng: Sinh báo cáo quality.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/; tests/test_ingestion.py; docs/data-ingestion.md; evidence tại evidence/T01-083.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Sinh báo cáo quality.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G01, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Test đúng biên và ngoài biên, NaN/Inf, timestamp thiếu múi giờ, duplicate và bước nhảy lớn; báo cáo reject/flag có reason code.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T01-083.md](evidence/T01-083.md).
