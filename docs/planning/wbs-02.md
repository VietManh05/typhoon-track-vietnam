# G02 — Dữ liệu không gian

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có adapter; chưa xác minh dữ liệu ranh giới/đường bờ thật.
- Đầu vào: Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS.
- Gate phụ thuộc: G00.
- Vùng file dự kiến: src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: WGS84 nhất quán; khoảng cách theo km; polygon hợp lệ; giữ provenance và attribution.

<a id="gate-g02"></a>
## Gate G02

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t02-001"></a>
## T02-001 — Chọn nguồn coastline.

- **Trạng thái:** pending.
- **Nguồn:** 2.1 Coastline; dòng [557](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:557).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.1 Coastline.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Chọn nguồn coastline.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chọn nguồn coastline.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Đường bờ dạng segment, không chỉ nearest vertex; test điểm nằm trên bờ và ngoài biển; CRS/SRID được ghi vào metadata.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-002"></a>
## T02-002 — Tải dữ liệu.

- **Trạng thái:** pending.
- **Nguồn:** 2.1 Coastline; dòng [558](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:558).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.1 Coastline.
- **Task trước trong tiểu mục:** T02-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Tải dữ liệu.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tải dữ liệu.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Mock bytes xác định và HTTP failure; checksum/raw giữ nguyên; lần tải thật phải có nguồn hợp lệ và evidence riêng.
- **Kịch bản tiểu mục:** Đường bờ dạng segment, không chỉ nearest vertex; test điểm nằm trên bờ và ngoài biển; CRS/SRID được ghi vào metadata.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-003"></a>
## T02-003 — Kiểm tra CRS.

- **Trạng thái:** pending.
- **Nguồn:** 2.1 Coastline; dòng [559](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:559).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.1 Coastline.
- **Task trước trong tiểu mục:** T02-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Kiểm tra CRS.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra CRS.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Đường bờ dạng segment, không chỉ nearest vertex; test điểm nằm trên bờ và ngoài biển; CRS/SRID được ghi vào metadata.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-004"></a>
## T02-004 — Chuẩn hóa CRS.

- **Trạng thái:** pending.
- **Nguồn:** 2.1 Coastline; dòng [560](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:560).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.1 Coastline.
- **Task trước trong tiểu mục:** T02-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Chuẩn hóa CRS.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chuẩn hóa CRS.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Đường bờ dạng segment, không chỉ nearest vertex; test điểm nằm trên bờ và ngoài biển; CRS/SRID được ghi vào metadata.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-005"></a>
## T02-005 — Simplify cho frontend nếu cần.

- **Trạng thái:** pending.
- **Nguồn:** 2.1 Coastline; dòng [561](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:561).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.1 Coastline.
- **Task trước trong tiểu mục:** T02-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Simplify cho frontend nếu cần.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Simplify cho frontend nếu cần.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Đường bờ dạng segment, không chỉ nearest vertex; test điểm nằm trên bờ và ngoài biển; CRS/SRID được ghi vào metadata.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-006"></a>
## T02-006 — Tạo spatial index.

- **Trạng thái:** pending.
- **Nguồn:** 2.1 Coastline; dòng [562](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:562).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.1 Coastline.
- **Task trước trong tiểu mục:** T02-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Tạo spatial index.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo spatial index.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** DB trống và DB có dữ liệu upgrade được; invalid records bị constraints reject; GiST test trên PostGIS thật.
- **Kịch bản tiểu mục:** Đường bờ dạng segment, không chỉ nearest vertex; test điểm nằm trên bờ và ngoài biển; CRS/SRID được ghi vào metadata.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-007"></a>
## T02-007 — Test khoảng cách tới bờ.

- **Trạng thái:** pending.
- **Nguồn:** 2.1 Coastline; dòng [563](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:563).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.1 Coastline.
- **Task trước trong tiểu mục:** T02-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Test khoảng cách tới bờ.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test khoảng cách tới bờ.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Điểm trùng cho 0 km; cặp điểm chuẩn khớp dung sai; wrap longitude không tạo khoảng cách vòng trái đất.
- **Kịch bản tiểu mục:** Đường bờ dạng segment, không chỉ nearest vertex; test điểm nằm trên bờ và ngoài biển; CRS/SRID được ghi vào metadata.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-008"></a>
## T02-008 — Tải ranh giới tỉnh/thành.

- **Trạng thái:** pending.
- **Nguồn:** 2.2 Administrative Boundary; dòng [566](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:566).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.2 Administrative Boundary.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Tải ranh giới tỉnh/thành.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tải ranh giới tỉnh/thành.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Mock bytes xác định và HTTP failure; checksum/raw giữ nguyên; lần tải thật phải có nguồn hợp lệ và evidence riêng.
- **Kịch bản tiểu mục:** Ranh giới có ngày hiệu lực và mã tỉnh; test điểm trong/ngoài/trên biên và MultiPolygon; dữ liệu rút gọn phải giữ topology.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-009"></a>
## T02-009 — Kiểm tra CRS.

- **Trạng thái:** pending.
- **Nguồn:** 2.2 Administrative Boundary; dòng [567](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:567).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.2 Administrative Boundary.
- **Task trước trong tiểu mục:** T02-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Kiểm tra CRS.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra CRS.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Ranh giới có ngày hiệu lực và mã tỉnh; test điểm trong/ngoài/trên biên và MultiPolygon; dữ liệu rút gọn phải giữ topology.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-010"></a>
## T02-010 — Chuẩn hóa tên tỉnh.

- **Trạng thái:** pending.
- **Nguồn:** 2.2 Administrative Boundary; dòng [568](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:568).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.2 Administrative Boundary.
- **Task trước trong tiểu mục:** T02-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Chuẩn hóa tên tỉnh.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chuẩn hóa tên tỉnh.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Ranh giới có ngày hiệu lực và mã tỉnh; test điểm trong/ngoài/trên biên và MultiPolygon; dữ liệu rút gọn phải giữ topology.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-011"></a>
## T02-011 — Tạo GeoJSON.

- **Trạng thái:** pending.
- **Nguồn:** 2.2 Administrative Boundary; dòng [569](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:569).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.2 Administrative Boundary.
- **Task trước trong tiểu mục:** T02-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Tạo GeoJSON.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo GeoJSON.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** GeoJSON [lon,lat], ring đóng/topology hợp lệ; dateline có xử lý; coverage thực nghiệm khác radius minh họa.
- **Kịch bản tiểu mục:** Ranh giới có ngày hiệu lực và mã tỉnh; test điểm trong/ngoài/trên biên và MultiPolygon; dữ liệu rút gọn phải giữ topology.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-012"></a>
## T02-012 — Tạo spatial index.

- **Trạng thái:** pending.
- **Nguồn:** 2.2 Administrative Boundary; dòng [570](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:570).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.2 Administrative Boundary.
- **Task trước trong tiểu mục:** T02-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Tạo spatial index.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo spatial index.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** DB trống và DB có dữ liệu upgrade được; invalid records bị constraints reject; GiST test trên PostGIS thật.
- **Kịch bản tiểu mục:** Ranh giới có ngày hiệu lực và mã tỉnh; test điểm trong/ngoài/trên biên và MultiPolygon; dữ liệu rút gọn phải giữ topology.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-013"></a>
## T02-013 — Test point-in-polygon.

- **Trạng thái:** pending.
- **Nguồn:** 2.2 Administrative Boundary; dòng [571](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:571).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.2 Administrative Boundary.
- **Task trước trong tiểu mục:** T02-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Test point-in-polygon.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test point-in-polygon.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** GeoJSON [lon,lat], ring đóng/topology hợp lệ; dateline có xử lý; coverage thực nghiệm khác radius minh họa.
- **Kịch bản tiểu mục:** Ranh giới có ngày hiệu lực và mã tỉnh; test điểm trong/ngoài/trên biên và MultiPolygon; dữ liệu rút gọn phải giữ topology.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-014"></a>
## T02-014 — Test nearest province.

- **Trạng thái:** pending.
- **Nguồn:** 2.2 Administrative Boundary; dòng [572](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:572).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.2 Administrative Boundary.
- **Task trước trong tiểu mục:** T02-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Test nearest province.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test nearest province.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Ranh giới có ngày hiệu lực và mã tỉnh; test điểm trong/ngoài/trên biên và MultiPolygon; dữ liệu rút gọn phải giữ topology.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-015"></a>
## T02-015 — Tạo danh sách các mốc cần theo dõi.

- **Trạng thái:** pending.
- **Nguồn:** 2.3 Special Locations; dòng [575](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:575).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.3 Special Locations.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Tạo danh sách các mốc cần theo dõi.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo danh sách các mốc cần theo dõi.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mỗi địa điểm có ID ổn định và nguồn tọa độ; test duplicate ID, tọa độ sai, distance 0 và khoảng cách tham chiếu.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-016"></a>
## T02-016 — Lưu latitude/longitude.

- **Trạng thái:** pending.
- **Nguồn:** 2.3 Special Locations; dòng [576](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:576).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.3 Special Locations.
- **Task trước trong tiểu mục:** T02-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Lưu latitude/longitude.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu latitude/longitude.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test hợp lệ/ngoài biên/NaN/Inf và wrap longitude; output giữ đúng đơn vị tọa độ.
- **Kịch bản tiểu mục:** Mỗi địa điểm có ID ổn định và nguồn tọa độ; test duplicate ID, tọa độ sai, distance 0 và khoảng cách tham chiếu.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-017"></a>
## T02-017 — Tạo ID duy nhất.

- **Trạng thái:** pending.
- **Nguồn:** 2.3 Special Locations; dòng [577](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:577).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.3 Special Locations.
- **Task trước trong tiểu mục:** T02-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Tạo ID duy nhất.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo ID duy nhất.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Mỗi địa điểm có ID ổn định và nguồn tọa độ; test duplicate ID, tọa độ sai, distance 0 và khoảng cách tham chiếu.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-018"></a>
## T02-018 — Tạo hàm khoảng cách.

- **Trạng thái:** pending.
- **Nguồn:** 2.3 Special Locations; dòng [578](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:578).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.3 Special Locations.
- **Task trước trong tiểu mục:** T02-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Tạo hàm khoảng cách.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo hàm khoảng cách.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Điểm trùng cho 0 km; cặp điểm chuẩn khớp dung sai; wrap longitude không tạo khoảng cách vòng trái đất.
- **Kịch bản tiểu mục:** Mỗi địa điểm có ID ổn định và nguồn tọa độ; test duplicate ID, tọa độ sai, distance 0 và khoảng cách tham chiếu.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t02-019"></a>
## T02-019 — Test kết quả.

- **Trạng thái:** pending.
- **Nguồn:** 2.3 Special Locations; dòng [579](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:579).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G00; contract/fixture của tiểu mục 2.3 Special Locations.
- **Task trước trong tiểu mục:** T02-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Coastline/ranh giới có phiên bản, ngày hiệu lực, giấy phép và CRS; yêu cầu riêng: Test kết quả.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/ingestion/providers/geospatial.py; src/typhoon_vn/features/geo.py; data/external/; tests/test_geospatial.py; evidence tại evidence/T02-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test kết quả.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G02, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Mỗi địa điểm có ID ổn định và nguồn tọa độ; test duplicate ID, tọa độ sai, distance 0 và khoảng cách tham chiếu.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
