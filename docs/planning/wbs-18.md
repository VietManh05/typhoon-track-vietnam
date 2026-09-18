# G18 — Database, PostGIS và migration

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Nháp SQLAlchemy SQLite/Postgres; thiếu PostGIS geometry, Alembic và đủ bảng.
- Đầu vào: Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit.
- Gate phụ thuộc: G00, G02.
- Vùng file dự kiến: src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Migration upgrade/downgrade; FK/unique/index/spatial index; transaction; không dùng create_all thay migration production.

<a id="gate-g18"></a>
## Gate G18

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t18-001"></a>
## T18-001 — `typhoons`.

- **Trạng thái:** pending.
- **Nguồn:** 18.1 Tables; dòng [1019](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1019).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.1 Tables.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: `typhoons`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`typhoons`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** FK storm/model/run, uniqueness source+storm+valid_time+revision; geometry Point/Polygon SRID 4326; nguồn sửa quan trắc vẫn giữ audit.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-002"></a>
## T18-002 — `observations`.

- **Trạng thái:** pending.
- **Nguồn:** 18.1 Tables; dòng [1020](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1020).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.1 Tables.
- **Task trước trong tiểu mục:** T18-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: `observations`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`observations`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** FK storm/model/run, uniqueness source+storm+valid_time+revision; geometry Point/Polygon SRID 4326; nguồn sửa quan trắc vẫn giữ audit.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-003"></a>
## T18-003 — `forecasts`.

- **Trạng thái:** pending.
- **Nguồn:** 18.1 Tables; dòng [1021](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1021).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.1 Tables.
- **Task trước trong tiểu mục:** T18-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: `forecasts`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`forecasts`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** FK storm/model/run, uniqueness source+storm+valid_time+revision; geometry Point/Polygon SRID 4326; nguồn sửa quan trắc vẫn giữ audit.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-004"></a>
## T18-004 — `forecast_points`.

- **Trạng thái:** pending.
- **Nguồn:** 18.1 Tables; dòng [1022](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1022).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.1 Tables.
- **Task trước trong tiểu mục:** T18-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: `forecast_points`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`forecast_points`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** FK storm/model/run, uniqueness source+storm+valid_time+revision; geometry Point/Polygon SRID 4326; nguồn sửa quan trắc vẫn giữ audit.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-005"></a>
## T18-005 — `alerts`.

- **Trạng thái:** pending.
- **Nguồn:** 18.1 Tables; dòng [1023](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1023).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.1 Tables.
- **Task trước trong tiểu mục:** T18-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: `alerts`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`alerts`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** FK storm/model/run, uniqueness source+storm+valid_time+revision; geometry Point/Polygon SRID 4326; nguồn sửa quan trắc vẫn giữ audit.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-006"></a>
## T18-006 — `model_versions`.

- **Trạng thái:** pending.
- **Nguồn:** 18.1 Tables; dòng [1024](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1024).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.1 Tables.
- **Task trước trong tiểu mục:** T18-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: `model_versions`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`model_versions`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** FK storm/model/run, uniqueness source+storm+valid_time+revision; geometry Point/Polygon SRID 4326; nguồn sửa quan trắc vẫn giữ audit.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-007"></a>
## T18-007 — `users`.

- **Trạng thái:** pending.
- **Nguồn:** 18.1 Tables; dòng [1025](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1025).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.1 Tables.
- **Task trước trong tiểu mục:** T18-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: `users`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`users`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** FK storm/model/run, uniqueness source+storm+valid_time+revision; geometry Point/Polygon SRID 4326; nguồn sửa quan trắc vẫn giữ audit.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-008"></a>
## T18-008 — `subscriptions`.

- **Trạng thái:** pending.
- **Nguồn:** 18.1 Tables; dòng [1026](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1026).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.1 Tables.
- **Task trước trong tiểu mục:** T18-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: `subscriptions`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`subscriptions`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** FK storm/model/run, uniqueness source+storm+valid_time+revision; geometry Point/Polygon SRID 4326; nguồn sửa quan trắc vẫn giữ audit.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-009"></a>
## T18-009 — Alembic init.

- **Trạng thái:** pending.
- **Nguồn:** 18.2 Migration; dòng [1029](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1029).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.2 Migration.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: Alembic init.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Alembic init.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** DB trống và DB có dữ liệu upgrade được; invalid records bị constraints reject; GiST test trên PostGIS thật.
- **Kịch bản tiểu mục:** DB trống upgrade→head; upgrade dữ liệu cũ; downgrade trong môi trường test; kiểm tra GiST index và constraints trên PostGIS thật.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-010"></a>
## T18-010 — Initial migration.

- **Trạng thái:** pending.
- **Nguồn:** 18.2 Migration; dòng [1030](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1030).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.2 Migration.
- **Task trước trong tiểu mục:** T18-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: Initial migration.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Initial migration.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** DB trống và DB có dữ liệu upgrade được; invalid records bị constraints reject; GiST test trên PostGIS thật.
- **Kịch bản tiểu mục:** DB trống upgrade→head; upgrade dữ liệu cũ; downgrade trong môi trường test; kiểm tra GiST index và constraints trên PostGIS thật.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-011"></a>
## T18-011 — Index.

- **Trạng thái:** pending.
- **Nguồn:** 18.2 Migration; dòng [1031](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1031).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.2 Migration.
- **Task trước trong tiểu mục:** T18-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: Index.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Index.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** DB trống và DB có dữ liệu upgrade được; invalid records bị constraints reject; GiST test trên PostGIS thật.
- **Kịch bản tiểu mục:** DB trống upgrade→head; upgrade dữ liệu cũ; downgrade trong môi trường test; kiểm tra GiST index và constraints trên PostGIS thật.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-012"></a>
## T18-012 — Spatial index.

- **Trạng thái:** pending.
- **Nguồn:** 18.2 Migration; dòng [1032](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1032).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.2 Migration.
- **Task trước trong tiểu mục:** T18-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: Spatial index.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Spatial index.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** DB trống và DB có dữ liệu upgrade được; invalid records bị constraints reject; GiST test trên PostGIS thật.
- **Kịch bản tiểu mục:** DB trống upgrade→head; upgrade dữ liệu cũ; downgrade trong môi trường test; kiểm tra GiST index và constraints trên PostGIS thật.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-013"></a>
## T18-013 — Foreign keys.

- **Trạng thái:** pending.
- **Nguồn:** 18.2 Migration; dòng [1033](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1033).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.2 Migration.
- **Task trước trong tiểu mục:** T18-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: Foreign keys.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Foreign keys.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** DB trống và DB có dữ liệu upgrade được; invalid records bị constraints reject; GiST test trên PostGIS thật.
- **Kịch bản tiểu mục:** DB trống upgrade→head; upgrade dữ liệu cũ; downgrade trong môi trường test; kiểm tra GiST index và constraints trên PostGIS thật.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-014"></a>
## T18-014 — Constraints.

- **Trạng thái:** pending.
- **Nguồn:** 18.2 Migration; dòng [1034](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1034).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.2 Migration.
- **Task trước trong tiểu mục:** T18-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: Constraints.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Constraints.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** DB trống upgrade→head; upgrade dữ liệu cũ; downgrade trong môi trường test; kiểm tra GiST index và constraints trên PostGIS thật.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-015"></a>
## T18-015 — Lưu thời điểm dự báo.

- **Trạng thái:** pending.
- **Nguồn:** 18.3 Audit; dòng [1037](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1037).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.3 Audit.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: Lưu thời điểm dự báo.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu thời điểm dự báo.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt.
- **Kịch bản tiểu mục:** Run ID, issue_time, generated_at, input hash, source revision, model/scaler/schema version; request cache không làm mất audit semantics.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-016"></a>
## T18-016 — Lưu model version.

- **Trạng thái:** pending.
- **Nguồn:** 18.3 Audit; dòng [1038](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1038).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.3 Audit.
- **Task trước trong tiểu mục:** T18-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: Lưu model version.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu model version.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Run ID, issue_time, generated_at, input hash, source revision, model/scaler/schema version; request cache không làm mất audit semantics.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-017"></a>
## T18-017 — Lưu input version.

- **Trạng thái:** pending.
- **Nguồn:** 18.3 Audit; dòng [1039](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1039).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.3 Audit.
- **Task trước trong tiểu mục:** T18-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: Lưu input version.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu input version.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Run ID, issue_time, generated_at, input hash, source revision, model/scaler/schema version; request cache không làm mất audit semantics.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-018"></a>
## T18-018 — Lưu output.

- **Trạng thái:** pending.
- **Nguồn:** 18.3 Audit; dòng [1040](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1040).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.3 Audit.
- **Task trước trong tiểu mục:** T18-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: Lưu output.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu output.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Run ID, issue_time, generated_at, input hash, source revision, model/scaler/schema version; request cache không làm mất audit semantics.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t18-019"></a>
## T18-019 — Lưu forecast run ID.

- **Trạng thái:** pending.
- **Nguồn:** 18.3 Audit; dòng [1041](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1041).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00, G02; contract/fixture của tiểu mục 18.3 Audit.
- **Task trước trong tiểu mục:** T18-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Logical schema quan trắc/dự báo, SRID 4326 và yêu cầu audit; yêu cầu riêng: Lưu forecast run ID.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/operations/store.py; migrations/; alembic.ini; tests/test_store.py; tests/integration/test_postgis.py; evidence tại evidence/T18-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu forecast run ID.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G18, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Run ID, issue_time, generated_at, input hash, source revision, model/scaler/schema version; request cache không làm mất audit semantics.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
