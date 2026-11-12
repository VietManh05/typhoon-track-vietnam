# G20 — Redis và invalidation

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: API nháp mới setex; chưa đọc Redis, chưa invalidation tests.
- Đầu vào: Forecast/input/model revision và Redis configuration.
- Gate phụ thuộc: G17.
- Vùng file dự kiến: src/typhoon_vn/operations/cache.py; src/typhoon_vn/api/app.py; tests/test_cache.py.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Có read/write, hit/miss, TTL; observation/model mới invalidates; Redis hỏng vẫn phục vụ đúng qua DB.

<a id="gate-g20"></a>
## Gate G20

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t20-001"></a>
## T20-001 — Cache active typhoons.

- **Trạng thái:** pending.
- **Nguồn:** 20. REDIS; dòng [1062](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1062).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G17; contract/fixture của tiểu mục 20. REDIS.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Forecast/input/model revision và Redis configuration; yêu cầu riêng: Cache active typhoons.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/cache.py; src/typhoon_vn/api/app.py; tests/test_cache.py; evidence tại evidence/T20-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cache active typhoons.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G20, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hit/miss/expiry, observation sửa/model đổi và outage; cache key bao gồm input+model revision.
- **Kịch bản tiểu mục:** Có read/write, hit/miss, TTL; observation/model mới invalidates; Redis hỏng vẫn phục vụ đúng qua DB.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t20-002"></a>
## T20-002 — Cache latest forecast.

- **Trạng thái:** pending.
- **Nguồn:** 20. REDIS; dòng [1063](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1063).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G17; contract/fixture của tiểu mục 20. REDIS.
- **Task trước trong tiểu mục:** T20-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast/input/model revision và Redis configuration; yêu cầu riêng: Cache latest forecast.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/cache.py; src/typhoon_vn/api/app.py; tests/test_cache.py; evidence tại evidence/T20-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cache latest forecast.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G20, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hit/miss/expiry, observation sửa/model đổi và outage; cache key bao gồm input+model revision.
- **Kịch bản tiểu mục:** Có read/write, hit/miss, TTL; observation/model mới invalidates; Redis hỏng vẫn phục vụ đúng qua DB.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t20-003"></a>
## T20-003 — Cache API response.

- **Trạng thái:** pending.
- **Nguồn:** 20. REDIS; dòng [1064](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1064).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G17; contract/fixture của tiểu mục 20. REDIS.
- **Task trước trong tiểu mục:** T20-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast/input/model revision và Redis configuration; yêu cầu riêng: Cache API response.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/cache.py; src/typhoon_vn/api/app.py; tests/test_cache.py; evidence tại evidence/T20-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cache API response.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G20, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hit/miss/expiry, observation sửa/model đổi và outage; cache key bao gồm input+model revision.
- **Kịch bản tiểu mục:** Có read/write, hit/miss, TTL; observation/model mới invalidates; Redis hỏng vẫn phục vụ đúng qua DB.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t20-004"></a>
## T20-004 — TTL.

- **Trạng thái:** pending.
- **Nguồn:** 20. REDIS; dòng [1065](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1065).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G17; contract/fixture của tiểu mục 20. REDIS.
- **Task trước trong tiểu mục:** T20-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast/input/model revision và Redis configuration; yêu cầu riêng: TTL.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/cache.py; src/typhoon_vn/api/app.py; tests/test_cache.py; evidence tại evidence/T20-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “TTL.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G20, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hit/miss/expiry, observation sửa/model đổi và outage; cache key bao gồm input+model revision.
- **Kịch bản tiểu mục:** Có read/write, hit/miss, TTL; observation/model mới invalidates; Redis hỏng vẫn phục vụ đúng qua DB.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t20-005"></a>
## T20-005 — Cache invalidation.

- **Trạng thái:** pending.
- **Nguồn:** 20. REDIS; dòng [1066](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1066).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G17; contract/fixture của tiểu mục 20. REDIS.
- **Task trước trong tiểu mục:** T20-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast/input/model revision và Redis configuration; yêu cầu riêng: Cache invalidation.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/cache.py; src/typhoon_vn/api/app.py; tests/test_cache.py; evidence tại evidence/T20-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cache invalidation.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G20, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hit/miss/expiry, observation sửa/model đổi và outage; cache key bao gồm input+model revision.
- **Kịch bản tiểu mục:** Có read/write, hit/miss, TTL; observation/model mới invalidates; Redis hỏng vẫn phục vụ đúng qua DB.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t20-006"></a>
## T20-006 — Test cache hit/miss.

- **Trạng thái:** pending.
- **Nguồn:** 20. REDIS; dòng [1067](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1067).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G17; contract/fixture của tiểu mục 20. REDIS.
- **Task trước trong tiểu mục:** T20-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Forecast/input/model revision và Redis configuration; yêu cầu riêng: Test cache hit/miss.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/cache.py; src/typhoon_vn/api/app.py; tests/test_cache.py; evidence tại evidence/T20-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test cache hit/miss.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G20, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hit/miss/expiry, observation sửa/model đổi và outage; cache key bao gồm input+model revision.
- **Kịch bản tiểu mục:** Có read/write, hit/miss, TTL; observation/model mới invalidates; Redis hỏng vẫn phục vụ đúng qua DB.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
