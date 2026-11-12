# G26 — Monitoring, drift và backup

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có counters đơn giản nháp; thiếu latency, drift, dashboard và restore.
- Đầu vào: Metrics endpoints, baseline feature distribution và kho backup.
- Gate phụ thuộc: G24.
- Vùng file dự kiến: infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.

<a id="gate-g26"></a>
## Gate G26

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t26-001"></a>
## T26-001 — API uptime.

- **Trạng thái:** pending.
- **Nguồn:** System; dòng [1224](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1224).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục System.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: API uptime.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “API uptime.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-002"></a>
## T26-002 — API latency.

- **Trạng thái:** pending.
- **Nguồn:** System; dòng [1225](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1225).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục System.
- **Task trước trong tiểu mục:** T26-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: API latency.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “API latency.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-003"></a>
## T26-003 — Error rate.

- **Trạng thái:** pending.
- **Nguồn:** System; dòng [1226](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1226).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục System.
- **Task trước trong tiểu mục:** T26-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Error rate.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Error rate.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-004"></a>
## T26-004 — Worker status.

- **Trạng thái:** pending.
- **Nguồn:** System; dòng [1227](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1227).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục System.
- **Task trước trong tiểu mục:** T26-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Worker status.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Worker status.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-005"></a>
## T26-005 — Database status.

- **Trạng thái:** pending.
- **Nguồn:** System; dòng [1228](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1228).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục System.
- **Task trước trong tiểu mục:** T26-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Database status.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Database status.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-006"></a>
## T26-006 — Redis status.

- **Trạng thái:** pending.
- **Nguồn:** System; dòng [1229](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1229).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục System.
- **Task trước trong tiểu mục:** T26-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Redis status.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Redis status.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hit/miss/expiry, observation sửa/model đổi và outage; cache key bao gồm input+model revision.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-007"></a>
## T26-007 — CPU.

- **Trạng thái:** pending.
- **Nguồn:** System; dòng [1230](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1230).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục System.
- **Task trước trong tiểu mục:** T26-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: CPU.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “CPU.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-008"></a>
## T26-008 — RAM.

- **Trạng thái:** pending.
- **Nguồn:** System; dòng [1231](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1231).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục System.
- **Task trước trong tiểu mục:** T26-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: RAM.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “RAM.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-009"></a>
## T26-009 — Disk.

- **Trạng thái:** pending.
- **Nguồn:** System; dòng [1232](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1232).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục System.
- **Task trước trong tiểu mục:** T26-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Disk.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Disk.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-010"></a>
## T26-010 — Last update timestamp.

- **Trạng thái:** pending.
- **Nguồn:** Data; dòng [1235](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1235).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục Data.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Last update timestamp.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Last update timestamp.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-011"></a>
## T26-011 — Missing rate.

- **Trạng thái:** pending.
- **Nguồn:** Data; dòng [1236](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1236).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục Data.
- **Task trước trong tiểu mục:** T26-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Missing rate.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Missing rate.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-012"></a>
## T26-012 — Schema drift.

- **Trạng thái:** pending.
- **Nguồn:** Data; dòng [1237](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1237).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục Data.
- **Task trước trong tiểu mục:** T26-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Schema drift.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Schema drift.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-013"></a>
## T26-013 — Source failure.

- **Trạng thái:** pending.
- **Nguồn:** Data; dòng [1238](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1238).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục Data.
- **Task trước trong tiểu mục:** T26-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Source failure.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Source failure.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-014"></a>
## T26-014 — Data delay.

- **Trạng thái:** pending.
- **Nguồn:** Data; dòng [1239](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1239).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục Data.
- **Task trước trong tiểu mục:** T26-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Data delay.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Data delay.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-015"></a>
## T26-015 — Input distribution.

- **Trạng thái:** pending.
- **Nguồn:** Model; dòng [1242](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1242).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục Model.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Input distribution.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Input distribution.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-016"></a>
## T26-016 — Feature drift.

- **Trạng thái:** pending.
- **Nguồn:** Model; dòng [1243](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1243).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục Model.
- **Task trước trong tiểu mục:** T26-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Feature drift.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Feature drift.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-017"></a>
## T26-017 — Prediction distribution.

- **Trạng thái:** pending.
- **Nguồn:** Model; dòng [1244](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1244).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục Model.
- **Task trước trong tiểu mục:** T26-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Prediction distribution.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Prediction distribution.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-018"></a>
## T26-018 — Error after actual track arrives.

- **Trạng thái:** pending.
- **Nguồn:** Model; dòng [1245](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1245).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục Model.
- **Task trước trong tiểu mục:** T26-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Error after actual track arrives.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Error after actual track arrives.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t26-019"></a>
## T26-019 — Model version.

- **Trạng thái:** pending.
- **Nguồn:** Model; dòng [1246](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1246).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục Model.
- **Task trước trong tiểu mục:** T26-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Metrics endpoints, baseline feature distribution và kho backup; yêu cầu riêng: Model version.
- **File/đầu ra:** thay đổi nhỏ trong infra/monitoring/; src/typhoon_vn/operations/monitoring.py; scripts/backup/; docs/runbook.md; evidence tại evidence/T26-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Model version.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G26, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Prometheus/Grafana; latency/error/worker freshness; drift đo được; backup có restore drill; không log secrets.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
