# G22 — Alert engine và kênh tích hợp

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có rule/draft chưa test; chưa có channel adapters hoặc quản lý người nhận.
- Đầu vào: Forecast hợp lệ, subscription có quyền sở hữu và quy tắc radius/lead time.
- Gate phụ thuộc: G19, G21.
- Vùng file dự kiến: src/typhoon_vn/operations/worker.py; src/typhoon_vn/alerts/; tests/test_alerts.py; docs/alerts.md.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Boundary radius/lead được test; throttle bền vững, không gửi trùng; draft mặc định; adapter gửi thử bằng fake transport.

<a id="gate-g22"></a>
## Gate G22

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t22-001"></a>
## T22-001 — Thiết kế alert rule.

- **Trạng thái:** pending.
- **Nguồn:** 22. ALERT ENGINE; dòng [1128](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1128).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21; contract/fixture của tiểu mục 22. ALERT ENGINE.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Forecast hợp lệ, subscription có quyền sở hữu và quy tắc radius/lead time; yêu cầu riêng: Thiết kế alert rule.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/alerts/; tests/test_alerts.py; docs/alerts.md; evidence tại evidence/T22-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Thiết kế alert rule.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G22, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Boundary radius/lead được test; throttle bền vững, không gửi trùng; draft mặc định; adapter gửi thử bằng fake transport.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t22-002"></a>
## T22-002 — Distance threshold.

- **Trạng thái:** pending.
- **Nguồn:** 22. ALERT ENGINE; dòng [1129](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1129).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21; contract/fixture của tiểu mục 22. ALERT ENGINE.
- **Task trước trong tiểu mục:** T22-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast hợp lệ, subscription có quyền sở hữu và quy tắc radius/lead time; yêu cầu riêng: Distance threshold.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/alerts/; tests/test_alerts.py; docs/alerts.md; evidence tại evidence/T22-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Distance threshold.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G22, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Điểm trùng cho 0 km; cặp điểm chuẩn khớp dung sai; wrap longitude không tạo khoảng cách vòng trái đất.
- **Kịch bản tiểu mục:** Boundary radius/lead được test; throttle bền vững, không gửi trùng; draft mặc định; adapter gửi thử bằng fake transport.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t22-003"></a>
## T22-003 — Time threshold.

- **Trạng thái:** pending.
- **Nguồn:** 22. ALERT ENGINE; dòng [1130](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1130).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21; contract/fixture của tiểu mục 22. ALERT ENGINE.
- **Task trước trong tiểu mục:** T22-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast hợp lệ, subscription có quyền sở hữu và quy tắc radius/lead time; yêu cầu riêng: Time threshold.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/alerts/; tests/test_alerts.py; docs/alerts.md; evidence tại evidence/T22-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Time threshold.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G22, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Boundary radius/lead được test; throttle bền vững, không gửi trùng; draft mặc định; adapter gửi thử bằng fake transport.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t22-004"></a>
## T22-004 — Severity.

- **Trạng thái:** pending.
- **Nguồn:** 22. ALERT ENGINE; dòng [1131](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1131).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21; contract/fixture của tiểu mục 22. ALERT ENGINE.
- **Task trước trong tiểu mục:** T22-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast hợp lệ, subscription có quyền sở hữu và quy tắc radius/lead time; yêu cầu riêng: Severity.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/alerts/; tests/test_alerts.py; docs/alerts.md; evidence tại evidence/T22-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Severity.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G22, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Boundary radius/lead được test; throttle bền vững, không gửi trùng; draft mặc định; adapter gửi thử bằng fake transport.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t22-005"></a>
## T22-005 — Subscription area.

- **Trạng thái:** pending.
- **Nguồn:** 22. ALERT ENGINE; dòng [1132](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1132).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21; contract/fixture của tiểu mục 22. ALERT ENGINE.
- **Task trước trong tiểu mục:** T22-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast hợp lệ, subscription có quyền sở hữu và quy tắc radius/lead time; yêu cầu riêng: Subscription area.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/alerts/; tests/test_alerts.py; docs/alerts.md; evidence tại evidence/T22-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Subscription area.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G22, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Boundary radius/lead được test; throttle bền vững, không gửi trùng; draft mặc định; adapter gửi thử bằng fake transport.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t22-006"></a>
## T22-006 — Generate message.

- **Trạng thái:** pending.
- **Nguồn:** 22. ALERT ENGINE; dòng [1133](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1133).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21; contract/fixture của tiểu mục 22. ALERT ENGINE.
- **Task trước trong tiểu mục:** T22-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast hợp lệ, subscription có quyền sở hữu và quy tắc radius/lead time; yêu cầu riêng: Generate message.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/alerts/; tests/test_alerts.py; docs/alerts.md; evidence tại evidence/T22-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Generate message.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G22, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Boundary radius/lead được test; throttle bền vững, không gửi trùng; draft mặc định; adapter gửi thử bằng fake transport.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t22-007"></a>
## T22-007 — Add source.

- **Trạng thái:** pending.
- **Nguồn:** 22. ALERT ENGINE; dòng [1134](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1134).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21; contract/fixture của tiểu mục 22. ALERT ENGINE.
- **Task trước trong tiểu mục:** T22-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast hợp lệ, subscription có quyền sở hữu và quy tắc radius/lead time; yêu cầu riêng: Add source.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/alerts/; tests/test_alerts.py; docs/alerts.md; evidence tại evidence/T22-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Add source.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G22, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Boundary radius/lead được test; throttle bền vững, không gửi trùng; draft mặc định; adapter gửi thử bằng fake transport.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t22-008"></a>
## T22-008 — Add issue time.

- **Trạng thái:** pending.
- **Nguồn:** 22. ALERT ENGINE; dòng [1135](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1135).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21; contract/fixture của tiểu mục 22. ALERT ENGINE.
- **Task trước trong tiểu mục:** T22-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast hợp lệ, subscription có quyền sở hữu và quy tắc radius/lead time; yêu cầu riêng: Add issue time.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/alerts/; tests/test_alerts.py; docs/alerts.md; evidence tại evidence/T22-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Add issue time.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G22, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Boundary radius/lead được test; throttle bền vững, không gửi trùng; draft mặc định; adapter gửi thử bằng fake transport.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t22-009"></a>
## T22-009 — Add disclaimer.

- **Trạng thái:** pending.
- **Nguồn:** 22. ALERT ENGINE; dòng [1136](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1136).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21; contract/fixture của tiểu mục 22. ALERT ENGINE.
- **Task trước trong tiểu mục:** T22-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast hợp lệ, subscription có quyền sở hữu và quy tắc radius/lead time; yêu cầu riêng: Add disclaimer.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/alerts/; tests/test_alerts.py; docs/alerts.md; evidence tại evidence/T22-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Add disclaimer.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G22, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Nội dung khớp implementation đã kiểm chứng; ví dụ chạy được; link đúng; phân biệt demo/thực nghiệm/vận hành.
- **Kịch bản tiểu mục:** Boundary radius/lead được test; throttle bền vững, không gửi trùng; draft mặc định; adapter gửi thử bằng fake transport.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t22-010"></a>
## T22-010 — Send channel.

- **Trạng thái:** pending.
- **Nguồn:** 22. ALERT ENGINE; dòng [1137](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1137).
- **Loại:** chuẩn bị/test cục bộ trước; chạy thật cần nguồn, credentials và phạm vi vận hành phù hợp.
- **Phụ thuộc:** G19, G21; contract/fixture của tiểu mục 22. ALERT ENGINE.
- **Task trước trong tiểu mục:** T22-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast hợp lệ, subscription có quyền sở hữu và quy tắc radius/lead time; yêu cầu riêng: Send channel.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/alerts/; tests/test_alerts.py; docs/alerts.md; evidence tại evidence/T22-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Send channel.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G22, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fake transport không gửi trùng event qua restart/redelivery; cooldown đúng biên; không gửi tin thật trong test.
- **Kịch bản tiểu mục:** Boundary radius/lead được test; throttle bền vững, không gửi trùng; draft mặc định; adapter gửi thử bằng fake transport.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t22-011"></a>
## T22-011 — Retry.

- **Trạng thái:** pending.
- **Nguồn:** 22. ALERT ENGINE; dòng [1138](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1138).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21; contract/fixture của tiểu mục 22. ALERT ENGINE.
- **Task trước trong tiểu mục:** T22-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast hợp lệ, subscription có quyền sở hữu và quy tắc radius/lead time; yêu cầu riêng: Retry.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/alerts/; tests/test_alerts.py; docs/alerts.md; evidence tại evidence/T22-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Retry.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G22, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fake transport lỗi rồi thành công; số lần thử/timeout theo cấu hình; hết retry có trạng thái thất bại và log.
- **Kịch bản tiểu mục:** Boundary radius/lead được test; throttle bền vững, không gửi trùng; draft mặc định; adapter gửi thử bằng fake transport.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t22-012"></a>
## T22-012 — Throttle.

- **Trạng thái:** pending.
- **Nguồn:** 22. ALERT ENGINE; dòng [1139](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1139).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21; contract/fixture của tiểu mục 22. ALERT ENGINE.
- **Task trước trong tiểu mục:** T22-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast hợp lệ, subscription có quyền sở hữu và quy tắc radius/lead time; yêu cầu riêng: Throttle.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/alerts/; tests/test_alerts.py; docs/alerts.md; evidence tại evidence/T22-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Throttle.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G22, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fake transport không gửi trùng event qua restart/redelivery; cooldown đúng biên; không gửi tin thật trong test.
- **Kịch bản tiểu mục:** Boundary radius/lead được test; throttle bền vững, không gửi trùng; draft mặc định; adapter gửi thử bằng fake transport.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t22-013"></a>
## T22-013 — Alert history.

- **Trạng thái:** pending.
- **Nguồn:** 22. ALERT ENGINE; dòng [1140](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1140).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G19, G21; contract/fixture của tiểu mục 22. ALERT ENGINE.
- **Task trước trong tiểu mục:** T22-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast hợp lệ, subscription có quyền sở hữu và quy tắc radius/lead time; yêu cầu riêng: Alert history.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/worker.py; src/typhoon_vn/alerts/; tests/test_alerts.py; docs/alerts.md; evidence tại evidence/T22-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Alert history.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G22, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Boundary radius/lead được test; throttle bền vững, không gửi trùng; draft mặc định; adapter gửi thử bằng fake transport.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
