# G24 — Container và cấu hình production

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có Dockerfile/compose dev; chưa chạy Docker trên môi trường này.
- Đầu vào: Build backend/frontend/worker đã pass và model artifact kiểm chứng.
- Gate phụ thuộc: G23.
- Vùng file dự kiến: infra/docker/; docker-compose.yml; docker-compose.prod.yml; infra/nginx/.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Image riêng đúng extras; non-root; healthchecks; secrets ngoài image; volume/network; compose smoke.

<a id="gate-g24"></a>
## Gate G24

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t24-001"></a>
## T24-001 — Backend Dockerfile.

- **Trạng thái:** pending.
- **Nguồn:** 24. DOCKER; dòng [1189](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1189).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G23; contract/fixture của tiểu mục 24. DOCKER.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Build backend/frontend/worker đã pass và model artifact kiểm chứng; yêu cầu riêng: Backend Dockerfile.
- **File/đầu ra:** thay đổi nhỏ trong infra/docker/; docker-compose.yml; docker-compose.prod.yml; infra/nginx/; evidence tại evidence/T24-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Backend Dockerfile.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G24, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Image riêng đúng extras; non-root; healthchecks; secrets ngoài image; volume/network; compose smoke.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t24-002"></a>
## T24-002 — Worker Dockerfile.

- **Trạng thái:** pending.
- **Nguồn:** 24. DOCKER; dòng [1190](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1190).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G23; contract/fixture của tiểu mục 24. DOCKER.
- **Task trước trong tiểu mục:** T24-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Build backend/frontend/worker đã pass và model artifact kiểm chứng; yêu cầu riêng: Worker Dockerfile.
- **File/đầu ra:** thay đổi nhỏ trong infra/docker/; docker-compose.yml; docker-compose.prod.yml; infra/nginx/; evidence tại evidence/T24-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Worker Dockerfile.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G24, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Image riêng đúng extras; non-root; healthchecks; secrets ngoài image; volume/network; compose smoke.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t24-003"></a>
## T24-003 — Frontend Dockerfile.

- **Trạng thái:** pending.
- **Nguồn:** 24. DOCKER; dòng [1191](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1191).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G23; contract/fixture của tiểu mục 24. DOCKER.
- **Task trước trong tiểu mục:** T24-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Build backend/frontend/worker đã pass và model artifact kiểm chứng; yêu cầu riêng: Frontend Dockerfile.
- **File/đầu ra:** thay đổi nhỏ trong infra/docker/; docker-compose.yml; docker-compose.prod.yml; infra/nginx/; evidence tại evidence/T24-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Frontend Dockerfile.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G24, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Image riêng đúng extras; non-root; healthchecks; secrets ngoài image; volume/network; compose smoke.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t24-004"></a>
## T24-004 — Training image nếu cần.

- **Trạng thái:** pending.
- **Nguồn:** 24. DOCKER; dòng [1192](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1192).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G23; contract/fixture của tiểu mục 24. DOCKER.
- **Task trước trong tiểu mục:** T24-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Build backend/frontend/worker đã pass và model artifact kiểm chứng; yêu cầu riêng: Training image nếu cần.
- **File/đầu ra:** thay đổi nhỏ trong infra/docker/; docker-compose.yml; docker-compose.prod.yml; infra/nginx/; evidence tại evidence/T24-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Training image nếu cần.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G24, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Build/config exit 0; smoke service; secrets/raw/checkpoints ngoài build context trừ artifact được chọn.
- **Kịch bản tiểu mục:** Image riêng đúng extras; non-root; healthchecks; secrets ngoài image; volume/network; compose smoke.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t24-005"></a>
## T24-005 — Postgres service.

- **Trạng thái:** pending.
- **Nguồn:** 24. DOCKER; dòng [1193](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1193).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G23; contract/fixture của tiểu mục 24. DOCKER.
- **Task trước trong tiểu mục:** T24-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Build backend/frontend/worker đã pass và model artifact kiểm chứng; yêu cầu riêng: Postgres service.
- **File/đầu ra:** thay đổi nhỏ trong infra/docker/; docker-compose.yml; docker-compose.prod.yml; infra/nginx/; evidence tại evidence/T24-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Postgres service.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G24, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Image riêng đúng extras; non-root; healthchecks; secrets ngoài image; volume/network; compose smoke.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t24-006"></a>
## T24-006 — Redis service.

- **Trạng thái:** pending.
- **Nguồn:** 24. DOCKER; dòng [1194](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1194).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G23; contract/fixture của tiểu mục 24. DOCKER.
- **Task trước trong tiểu mục:** T24-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Build backend/frontend/worker đã pass và model artifact kiểm chứng; yêu cầu riêng: Redis service.
- **File/đầu ra:** thay đổi nhỏ trong infra/docker/; docker-compose.yml; docker-compose.prod.yml; infra/nginx/; evidence tại evidence/T24-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Redis service.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G24, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hit/miss/expiry, observation sửa/model đổi và outage; cache key bao gồm input+model revision.
- **Kịch bản tiểu mục:** Image riêng đúng extras; non-root; healthchecks; secrets ngoài image; volume/network; compose smoke.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t24-007"></a>
## T24-007 — Network.

- **Trạng thái:** pending.
- **Nguồn:** 24. DOCKER; dòng [1195](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1195).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G23; contract/fixture của tiểu mục 24. DOCKER.
- **Task trước trong tiểu mục:** T24-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Build backend/frontend/worker đã pass và model artifact kiểm chứng; yêu cầu riêng: Network.
- **File/đầu ra:** thay đổi nhỏ trong infra/docker/; docker-compose.yml; docker-compose.prod.yml; infra/nginx/; evidence tại evidence/T24-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Network.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G24, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Image riêng đúng extras; non-root; healthchecks; secrets ngoài image; volume/network; compose smoke.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t24-008"></a>
## T24-008 — Volumes.

- **Trạng thái:** pending.
- **Nguồn:** 24. DOCKER; dòng [1196](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1196).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G23; contract/fixture của tiểu mục 24. DOCKER.
- **Task trước trong tiểu mục:** T24-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Build backend/frontend/worker đã pass và model artifact kiểm chứng; yêu cầu riêng: Volumes.
- **File/đầu ra:** thay đổi nhỏ trong infra/docker/; docker-compose.yml; docker-compose.prod.yml; infra/nginx/; evidence tại evidence/T24-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Volumes.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G24, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Image riêng đúng extras; non-root; healthchecks; secrets ngoài image; volume/network; compose smoke.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t24-009"></a>
## T24-009 — Environment.

- **Trạng thái:** pending.
- **Nguồn:** 24. DOCKER; dòng [1197](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1197).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G23; contract/fixture của tiểu mục 24. DOCKER.
- **Task trước trong tiểu mục:** T24-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Build backend/frontend/worker đã pass và model artifact kiểm chứng; yêu cầu riêng: Environment.
- **File/đầu ra:** thay đổi nhỏ trong infra/docker/; docker-compose.yml; docker-compose.prod.yml; infra/nginx/; evidence tại evidence/T24-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Environment.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G24, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Image riêng đúng extras; non-root; healthchecks; secrets ngoài image; volume/network; compose smoke.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t24-010"></a>
## T24-010 — Health checks.

- **Trạng thái:** pending.
- **Nguồn:** 24. DOCKER; dòng [1198](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1198).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G23; contract/fixture của tiểu mục 24. DOCKER.
- **Task trước trong tiểu mục:** T24-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Build backend/frontend/worker đã pass và model artifact kiểm chứng; yêu cầu riêng: Health checks.
- **File/đầu ra:** thay đổi nhỏ trong infra/docker/; docker-compose.yml; docker-compose.prod.yml; infra/nginx/; evidence tại evidence/T24-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Health checks.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G24, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Image riêng đúng extras; non-root; healthchecks; secrets ngoài image; volume/network; compose smoke.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t24-011"></a>
## T24-011 — Production compose.

- **Trạng thái:** pending.
- **Nguồn:** 24. DOCKER; dòng [1199](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1199).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G23; contract/fixture của tiểu mục 24. DOCKER.
- **Task trước trong tiểu mục:** T24-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Build backend/frontend/worker đã pass và model artifact kiểm chứng; yêu cầu riêng: Production compose.
- **File/đầu ra:** thay đổi nhỏ trong infra/docker/; docker-compose.yml; docker-compose.prod.yml; infra/nginx/; evidence tại evidence/T24-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Production compose.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G24, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Build/config exit 0; smoke service; secrets/raw/checkpoints ngoài build context trừ artifact được chọn.
- **Kịch bản tiểu mục:** Image riêng đúng extras; non-root; healthchecks; secrets ngoài image; volume/network; compose smoke.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
