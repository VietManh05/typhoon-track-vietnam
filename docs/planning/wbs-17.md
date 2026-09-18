# G17 — FastAPI

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Vừa viết endpoints, auth, rate limit; chưa chạy test mới.
- Đầu vào: Inference đã test và repository dữ liệu vận hành.
- Gate phụ thuộc: G16, G18.
- Vùng file dự kiến: src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.

<a id="gate-g17"></a>
## Gate G17

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t17-001"></a>
## T17-001 — Tạo FastAPI app.

- **Trạng thái:** pending.
- **Nguồn:** 17. FASTAPI; dòng [997](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:997).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G16, G18; contract/fixture của tiểu mục 17. FASTAPI.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Inference đã test và repository dữ liệu vận hành; yêu cầu riêng: Tạo FastAPI app.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py; evidence tại evidence/T17-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo FastAPI app.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G17, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t17-002"></a>
## T17-002 — `/health`.

- **Trạng thái:** pending.
- **Nguồn:** 17. FASTAPI; dòng [998](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:998).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G16, G18; contract/fixture của tiểu mục 17. FASTAPI.
- **Task trước trong tiểu mục:** T17-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Inference đã test và repository dữ liệu vận hành; yêu cầu riêng: `/health`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py; evidence tại evidence/T17-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`/health`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G17, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** TestClient kiểm tra valid/invalid input, status/schema/provenance và lỗi service; response không NaN.
- **Kịch bản tiểu mục:** Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t17-003"></a>
## T17-003 — `/version`.

- **Trạng thái:** pending.
- **Nguồn:** 17. FASTAPI; dòng [999](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:999).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G16, G18; contract/fixture của tiểu mục 17. FASTAPI.
- **Task trước trong tiểu mục:** T17-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Inference đã test và repository dữ liệu vận hành; yêu cầu riêng: `/version`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py; evidence tại evidence/T17-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`/version`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G17, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** TestClient kiểm tra valid/invalid input, status/schema/provenance và lỗi service; response không NaN.
- **Kịch bản tiểu mục:** Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t17-004"></a>
## T17-004 — `/forecast`.

- **Trạng thái:** pending.
- **Nguồn:** 17. FASTAPI; dòng [1000](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1000).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G16, G18; contract/fixture của tiểu mục 17. FASTAPI.
- **Task trước trong tiểu mục:** T17-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Inference đã test và repository dữ liệu vận hành; yêu cầu riêng: `/forecast`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py; evidence tại evidence/T17-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`/forecast`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G17, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** TestClient kiểm tra valid/invalid input, status/schema/provenance và lỗi service; response không NaN.
- **Kịch bản tiểu mục:** Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t17-005"></a>
## T17-005 — `/typhoons/active`.

- **Trạng thái:** pending.
- **Nguồn:** 17. FASTAPI; dòng [1001](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1001).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G16, G18; contract/fixture của tiểu mục 17. FASTAPI.
- **Task trước trong tiểu mục:** T17-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Inference đã test và repository dữ liệu vận hành; yêu cầu riêng: `/typhoons/active`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py; evidence tại evidence/T17-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`/typhoons/active`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G17, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** TestClient kiểm tra valid/invalid input, status/schema/provenance và lỗi service; response không NaN.
- **Kịch bản tiểu mục:** Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t17-006"></a>
## T17-006 — `/typhoons/{id}/track`.

- **Trạng thái:** pending.
- **Nguồn:** 17. FASTAPI; dòng [1002](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1002).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G16, G18; contract/fixture của tiểu mục 17. FASTAPI.
- **Task trước trong tiểu mục:** T17-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Inference đã test và repository dữ liệu vận hành; yêu cầu riêng: `/typhoons/{id}/track`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py; evidence tại evidence/T17-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`/typhoons/{id}/track`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G17, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** TestClient kiểm tra valid/invalid input, status/schema/provenance và lỗi service; response không NaN.
- **Kịch bản tiểu mục:** Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t17-007"></a>
## T17-007 — `/typhoons/{id}/impact`.

- **Trạng thái:** pending.
- **Nguồn:** 17. FASTAPI; dòng [1003](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1003).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G16, G18; contract/fixture của tiểu mục 17. FASTAPI.
- **Task trước trong tiểu mục:** T17-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Inference đã test và repository dữ liệu vận hành; yêu cầu riêng: `/typhoons/{id}/impact`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py; evidence tại evidence/T17-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`/typhoons/{id}/impact`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G17, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** TestClient kiểm tra valid/invalid input, status/schema/provenance và lỗi service; response không NaN.
- **Kịch bản tiểu mục:** Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t17-008"></a>
## T17-008 — Pydantic request schemas.

- **Trạng thái:** pending.
- **Nguồn:** 17. FASTAPI; dòng [1004](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1004).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G16, G18; contract/fixture của tiểu mục 17. FASTAPI.
- **Task trước trong tiểu mục:** T17-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Inference đã test và repository dữ liệu vận hành; yêu cầu riêng: Pydantic request schemas.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py; evidence tại evidence/T17-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Pydantic request schemas.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G17, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t17-009"></a>
## T17-009 — Pydantic response schemas.

- **Trạng thái:** pending.
- **Nguồn:** 17. FASTAPI; dòng [1005](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1005).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G16, G18; contract/fixture của tiểu mục 17. FASTAPI.
- **Task trước trong tiểu mục:** T17-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Inference đã test và repository dữ liệu vận hành; yêu cầu riêng: Pydantic response schemas.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py; evidence tại evidence/T17-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Pydantic response schemas.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G17, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t17-010"></a>
## T17-010 — Error handler.

- **Trạng thái:** pending.
- **Nguồn:** 17. FASTAPI; dòng [1006](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1006).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G16, G18; contract/fixture của tiểu mục 17. FASTAPI.
- **Task trước trong tiểu mục:** T17-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Inference đã test và repository dữ liệu vận hành; yêu cầu riêng: Error handler.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py; evidence tại evidence/T17-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Error handler.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G17, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test thiếu/sai/đúng key, vượt hạn mức; status/body đúng; log không chứa secret; UI không chứa admin key.
- **Kịch bản tiểu mục:** Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t17-011"></a>
## T17-011 — Logging.

- **Trạng thái:** pending.
- **Nguồn:** 17. FASTAPI; dòng [1007](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1007).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G16, G18; contract/fixture của tiểu mục 17. FASTAPI.
- **Task trước trong tiểu mục:** T17-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Inference đã test và repository dữ liệu vận hành; yêu cầu riêng: Logging.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py; evidence tại evidence/T17-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Logging.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G17, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t17-012"></a>
## T17-012 — OpenAPI.

- **Trạng thái:** pending.
- **Nguồn:** 17. FASTAPI; dòng [1008](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1008).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G16, G18; contract/fixture của tiểu mục 17. FASTAPI.
- **Task trước trong tiểu mục:** T17-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Inference đã test và repository dữ liệu vận hành; yêu cầu riêng: OpenAPI.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py; evidence tại evidence/T17-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “OpenAPI.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G17, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t17-013"></a>
## T17-013 — API key nếu public.

- **Trạng thái:** pending.
- **Nguồn:** 17. FASTAPI; dòng [1009](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1009).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G16, G18; contract/fixture của tiểu mục 17. FASTAPI.
- **Task trước trong tiểu mục:** T17-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Inference đã test và repository dữ liệu vận hành; yêu cầu riêng: API key nếu public.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py; evidence tại evidence/T17-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “API key nếu public.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G17, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test thiếu/sai/đúng key, vượt hạn mức; status/body đúng; log không chứa secret; UI không chứa admin key.
- **Kịch bản tiểu mục:** Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t17-014"></a>
## T17-014 — Rate limit nếu public.

- **Trạng thái:** pending.
- **Nguồn:** 17. FASTAPI; dòng [1010](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1010).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G16, G18; contract/fixture của tiểu mục 17. FASTAPI.
- **Task trước trong tiểu mục:** T17-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Inference đã test và repository dữ liệu vận hành; yêu cầu riêng: Rate limit nếu public.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/api/app.py; src/typhoon_vn/api/schemas.py; tests/test_api.py; tests/test_health.py; evidence tại evidence/T17-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Rate limit nếu public.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G17, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test thiếu/sai/đúng key, vượt hạn mức; status/body đúng; log không chứa secret; UI không chứa admin key.
- **Kịch bản tiểu mục:** Contract/OpenAPI đúng; 404/422/401/429/503 có test; response có provenance, issue time, uncertainty, disclaimer.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
