# G19 — Worker thời gian thực

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Worker hiện chỉ đọc snapshot JSON và sinh forecast; chưa có scheduler/provider live.
- Đầu vào: Provider adapter đã kiểm thử, freshness window và cấu hình lịch.
- Gate phụ thuộc: G01, G17, G20.
- Vùng file dự kiến: src/typhoon_vn/operations/worker.py; src/typhoon_vn/ingestion/; tests/test_worker.py; infra/scheduler/.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Phát hiện observation mới; idempotency; retry/backoff hữu hạn; forecast/cache cập nhật; thất bại nhìn thấy.

<a id="gate-g19"></a>
## Gate G19

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t19-001"></a>
## T19-001 — Tạo worker.

- **Trạng thái:** pending.
- **Nguồn:** 19. REAL-TIME WORKER; dòng [1047](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1047).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01, G17, G20; contract/fixture của tiểu mục 19. REAL-TIME WORKER.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Provider adapter đã kiểm thử, freshness window và cấu hình lịch; yêu cầu riêng: Tạo worker.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/ingestion/; tests/test_worker.py; infra/scheduler/; evidence tại evidence/T19-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo worker.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G19, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Phát hiện observation mới; idempotency; retry/backoff hữu hạn; forecast/cache cập nhật; thất bại nhìn thấy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t19-002"></a>
## T19-002 — Scheduler.

- **Trạng thái:** pending.
- **Nguồn:** 19. REAL-TIME WORKER; dòng [1048](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1048).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01, G17, G20; contract/fixture của tiểu mục 19. REAL-TIME WORKER.
- **Task trước trong tiểu mục:** T19-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Provider adapter đã kiểm thử, freshness window và cấu hình lịch; yêu cầu riêng: Scheduler.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/ingestion/; tests/test_worker.py; infra/scheduler/; evidence tại evidence/T19-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Scheduler.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G19, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Phát hiện observation mới; idempotency; retry/backoff hữu hạn; forecast/cache cập nhật; thất bại nhìn thấy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t19-003"></a>
## T19-003 — Fetch latest source.

- **Trạng thái:** pending.
- **Nguồn:** 19. REAL-TIME WORKER; dòng [1049](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1049).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01, G17, G20; contract/fixture của tiểu mục 19. REAL-TIME WORKER.
- **Task trước trong tiểu mục:** T19-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Provider adapter đã kiểm thử, freshness window và cấu hình lịch; yêu cầu riêng: Fetch latest source.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/ingestion/; tests/test_worker.py; infra/scheduler/; evidence tại evidence/T19-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Fetch latest source.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G19, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Phát hiện observation mới; idempotency; retry/backoff hữu hạn; forecast/cache cập nhật; thất bại nhìn thấy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t19-004"></a>
## T19-004 — Validate new records.

- **Trạng thái:** pending.
- **Nguồn:** 19. REAL-TIME WORKER; dòng [1050](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1050).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01, G17, G20; contract/fixture của tiểu mục 19. REAL-TIME WORKER.
- **Task trước trong tiểu mục:** T19-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Provider adapter đã kiểm thử, freshness window và cấu hình lịch; yêu cầu riêng: Validate new records.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/ingestion/; tests/test_worker.py; infra/scheduler/; evidence tại evidence/T19-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Validate new records.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G19, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Phát hiện observation mới; idempotency; retry/backoff hữu hạn; forecast/cache cập nhật; thất bại nhìn thấy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t19-005"></a>
## T19-005 — Detect new observation.

- **Trạng thái:** pending.
- **Nguồn:** 19. REAL-TIME WORKER; dòng [1051](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1051).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01, G17, G20; contract/fixture của tiểu mục 19. REAL-TIME WORKER.
- **Task trước trong tiểu mục:** T19-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Provider adapter đã kiểm thử, freshness window và cấu hình lịch; yêu cầu riêng: Detect new observation.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/ingestion/; tests/test_worker.py; infra/scheduler/; evidence tại evidence/T19-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Detect new observation.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G19, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Phát hiện observation mới; idempotency; retry/backoff hữu hạn; forecast/cache cập nhật; thất bại nhìn thấy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t19-006"></a>
## T19-006 — Trigger inference.

- **Trạng thái:** pending.
- **Nguồn:** 19. REAL-TIME WORKER; dòng [1052](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1052).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01, G17, G20; contract/fixture của tiểu mục 19. REAL-TIME WORKER.
- **Task trước trong tiểu mục:** T19-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Provider adapter đã kiểm thử, freshness window và cấu hình lịch; yêu cầu riêng: Trigger inference.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/ingestion/; tests/test_worker.py; infra/scheduler/; evidence tại evidence/T19-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Trigger inference.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G19, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Phát hiện observation mới; idempotency; retry/backoff hữu hạn; forecast/cache cập nhật; thất bại nhìn thấy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t19-007"></a>
## T19-007 — Save forecast.

- **Trạng thái:** pending.
- **Nguồn:** 19. REAL-TIME WORKER; dòng [1053](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1053).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01, G17, G20; contract/fixture của tiểu mục 19. REAL-TIME WORKER.
- **Task trước trong tiểu mục:** T19-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Provider adapter đã kiểm thử, freshness window và cấu hình lịch; yêu cầu riêng: Save forecast.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/ingestion/; tests/test_worker.py; infra/scheduler/; evidence tại evidence/T19-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Save forecast.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G19, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Phát hiện observation mới; idempotency; retry/backoff hữu hạn; forecast/cache cập nhật; thất bại nhìn thấy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t19-008"></a>
## T19-008 — Update cache.

- **Trạng thái:** pending.
- **Nguồn:** 19. REAL-TIME WORKER; dòng [1054](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1054).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01, G17, G20; contract/fixture của tiểu mục 19. REAL-TIME WORKER.
- **Task trước trong tiểu mục:** T19-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Provider adapter đã kiểm thử, freshness window và cấu hình lịch; yêu cầu riêng: Update cache.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/ingestion/; tests/test_worker.py; infra/scheduler/; evidence tại evidence/T19-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Update cache.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G19, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hit/miss/expiry, observation sửa/model đổi và outage; cache key bao gồm input+model revision.
- **Kịch bản tiểu mục:** Phát hiện observation mới; idempotency; retry/backoff hữu hạn; forecast/cache cập nhật; thất bại nhìn thấy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t19-009"></a>
## T19-009 — Retry failure.

- **Trạng thái:** pending.
- **Nguồn:** 19. REAL-TIME WORKER; dòng [1055](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1055).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01, G17, G20; contract/fixture của tiểu mục 19. REAL-TIME WORKER.
- **Task trước trong tiểu mục:** T19-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Provider adapter đã kiểm thử, freshness window và cấu hình lịch; yêu cầu riêng: Retry failure.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/ingestion/; tests/test_worker.py; infra/scheduler/; evidence tại evidence/T19-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Retry failure.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G19, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fake transport lỗi rồi thành công; số lần thử/timeout theo cấu hình; hết retry có trạng thái thất bại và log.
- **Kịch bản tiểu mục:** Phát hiện observation mới; idempotency; retry/backoff hữu hạn; forecast/cache cập nhật; thất bại nhìn thấy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t19-010"></a>
## T19-010 — Log worker status.

- **Trạng thái:** pending.
- **Nguồn:** 19. REAL-TIME WORKER; dòng [1056](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1056).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01, G17, G20; contract/fixture của tiểu mục 19. REAL-TIME WORKER.
- **Task trước trong tiểu mục:** T19-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Provider adapter đã kiểm thử, freshness window và cấu hình lịch; yêu cầu riêng: Log worker status.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/ingestion/; tests/test_worker.py; infra/scheduler/; evidence tại evidence/T19-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Log worker status.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G19, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Phát hiện observation mới; idempotency; retry/backoff hữu hạn; forecast/cache cập nhật; thất bại nhìn thấy.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
