# G21 — Frontend và bản đồ

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Chưa có dashboard; static mount trong API chưa phải frontend.
- Đầu vào: API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực.
- Gate phụ thuộc: G02, G17.
- Vùng file dự kiến: viz/frontend/; tests/frontend/; docs/frontend.md.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: React/TypeScript + Leaflet là phương án dự kiến; actual/forecast/cone rõ; mobile/a11y; nguồn/thời gian/disclaimer luôn hiện.

<a id="gate-g21"></a>
## Gate G21

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t21-001"></a>
## T21-001 — Tạo React/Next.js.

- **Trạng thái:** pending.
- **Nguồn:** 21.1 Setup; dòng [1074](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1074).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.1 Setup.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Tạo React/Next.js.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo React/Next.js.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** React+TypeScript+Leaflet dự kiến; build reproducible, route, API client typed, loading/error/empty state; không nhúng API key admin vào JS.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-002"></a>
## T21-002 — Router.

- **Trạng thái:** pending.
- **Nguồn:** 21.1 Setup; dòng [1075](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1075).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.1 Setup.
- **Task trước trong tiểu mục:** T21-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Router.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Router.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** React+TypeScript+Leaflet dự kiến; build reproducible, route, API client typed, loading/error/empty state; không nhúng API key admin vào JS.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-003"></a>
## T21-003 — API client.

- **Trạng thái:** pending.
- **Nguồn:** 21.1 Setup; dòng [1076](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1076).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.1 Setup.
- **Task trước trong tiểu mục:** T21-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: API client.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “API client.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** React+TypeScript+Leaflet dự kiến; build reproducible, route, API client typed, loading/error/empty state; không nhúng API key admin vào JS.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-004"></a>
## T21-004 — State management.

- **Trạng thái:** pending.
- **Nguồn:** 21.1 Setup; dòng [1077](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1077).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.1 Setup.
- **Task trước trong tiểu mục:** T21-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: State management.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “State management.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** React+TypeScript+Leaflet dự kiến; build reproducible, route, API client typed, loading/error/empty state; không nhúng API key admin vào JS.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-005"></a>
## T21-005 — CSS/theme.

- **Trạng thái:** pending.
- **Nguồn:** 21.1 Setup; dòng [1078](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1078).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.1 Setup.
- **Task trước trong tiểu mục:** T21-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: CSS/theme.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “CSS/theme.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** React+TypeScript+Leaflet dự kiến; build reproducible, route, API client typed, loading/error/empty state; không nhúng API key admin vào JS.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-006"></a>
## T21-006 — Environment config.

- **Trạng thái:** pending.
- **Nguồn:** 21.1 Setup; dòng [1079](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1079).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.1 Setup.
- **Task trước trong tiểu mục:** T21-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Environment config.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Environment config.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** React+TypeScript+Leaflet dự kiến; build reproducible, route, API client typed, loading/error/empty state; không nhúng API key admin vào JS.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-007"></a>
## T21-007 — Leaflet.

- **Trạng thái:** pending.
- **Nguồn:** 21.2 Map; dòng [1082](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1082).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.2 Map.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Leaflet.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Leaflet.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** GeoJSON [lon,lat]; actual nét liền, forecast nét đứt, cone có chú giải; attribution tile; lỗi tải map có thông báo.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-008"></a>
## T21-008 — Vietnam boundary.

- **Trạng thái:** pending.
- **Nguồn:** 21.2 Map; dòng [1083](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1083).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.2 Map.
- **Task trước trong tiểu mục:** T21-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Vietnam boundary.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Vietnam boundary.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** GeoJSON [lon,lat]; actual nét liền, forecast nét đứt, cone có chú giải; attribution tile; lỗi tải map có thông báo.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-009"></a>
## T21-009 — Coastline.

- **Trạng thái:** pending.
- **Nguồn:** 21.2 Map; dòng [1084](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1084).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.2 Map.
- **Task trước trong tiểu mục:** T21-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Coastline.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Coastline.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** GeoJSON [lon,lat]; actual nét liền, forecast nét đứt, cone có chú giải; attribution tile; lỗi tải map có thông báo.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-010"></a>
## T21-010 — Storm marker.

- **Trạng thái:** pending.
- **Nguồn:** 21.2 Map; dòng [1085](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1085).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.2 Map.
- **Task trước trong tiểu mục:** T21-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Storm marker.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Storm marker.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** GeoJSON [lon,lat]; actual nét liền, forecast nét đứt, cone có chú giải; attribution tile; lỗi tải map có thông báo.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-011"></a>
## T21-011 — Historical track.

- **Trạng thái:** pending.
- **Nguồn:** 21.2 Map; dòng [1086](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1086).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.2 Map.
- **Task trước trong tiểu mục:** T21-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Historical track.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Historical track.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** GeoJSON [lon,lat]; actual nét liền, forecast nét đứt, cone có chú giải; attribution tile; lỗi tải map có thông báo.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-012"></a>
## T21-012 — Forecast track.

- **Trạng thái:** pending.
- **Nguồn:** 21.2 Map; dòng [1087](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1087).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.2 Map.
- **Task trước trong tiểu mục:** T21-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Forecast track.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Forecast track.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** GeoJSON [lon,lat]; actual nét liền, forecast nét đứt, cone có chú giải; attribution tile; lỗi tải map có thông báo.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-013"></a>
## T21-013 — Cone.

- **Trạng thái:** pending.
- **Nguồn:** 21.2 Map; dòng [1088](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1088).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.2 Map.
- **Task trước trong tiểu mục:** T21-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Cone.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cone.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** GeoJSON [lon,lat], ring đóng/topology hợp lệ; dateline có xử lý; coverage thực nghiệm khác radius minh họa.
- **Kịch bản tiểu mục:** GeoJSON [lon,lat]; actual nét liền, forecast nét đứt, cone có chú giải; attribution tile; lỗi tải map có thông báo.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-014"></a>
## T21-014 — Province layer.

- **Trạng thái:** pending.
- **Nguồn:** 21.2 Map; dòng [1089](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1089).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.2 Map.
- **Task trước trong tiểu mục:** T21-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Province layer.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Province layer.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** GeoJSON [lon,lat]; actual nét liền, forecast nét đứt, cone có chú giải; attribution tile; lỗi tải map có thông báo.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-015"></a>
## T21-015 — Active storm list.

- **Trạng thái:** pending.
- **Nguồn:** 21.3 Dashboard; dòng [1092](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1092).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.3 Dashboard.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Active storm list.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Active storm list.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** Test 0/1/nhiều bão, stale source và API lỗi; không gắn nhãn active chỉ vì có bản ghi lịch sử.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-016"></a>
## T21-016 — Storm status.

- **Trạng thái:** pending.
- **Nguồn:** 21.3 Dashboard; dòng [1093](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1093).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.3 Dashboard.
- **Task trước trong tiểu mục:** T21-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Storm status.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Storm status.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** Test 0/1/nhiều bão, stale source và API lỗi; không gắn nhãn active chỉ vì có bản ghi lịch sử.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-017"></a>
## T21-017 — Map.

- **Trạng thái:** pending.
- **Nguồn:** 21.3 Dashboard; dòng [1094](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1094).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.3 Dashboard.
- **Task trước trong tiểu mục:** T21-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Map.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Map.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** Test 0/1/nhiều bão, stale source và API lỗi; không gắn nhãn active chỉ vì có bản ghi lịch sử.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-018"></a>
## T21-018 — Legend.

- **Trạng thái:** pending.
- **Nguồn:** 21.3 Dashboard; dòng [1095](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1095).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.3 Dashboard.
- **Task trước trong tiểu mục:** T21-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Legend.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Legend.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** Test 0/1/nhiều bão, stale source và API lỗi; không gắn nhãn active chỉ vì có bản ghi lịch sử.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-019"></a>
## T21-019 — Last update.

- **Trạng thái:** pending.
- **Nguồn:** 21.3 Dashboard; dòng [1096](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1096).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.3 Dashboard.
- **Task trước trong tiểu mục:** T21-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Last update.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Last update.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** Test 0/1/nhiều bão, stale source và API lỗi; không gắn nhãn active chỉ vì có bản ghi lịch sử.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-020"></a>
## T21-020 — Data source.

- **Trạng thái:** pending.
- **Nguồn:** 21.3 Dashboard; dòng [1097](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1097).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.3 Dashboard.
- **Task trước trong tiểu mục:** T21-019; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Data source.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-020.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Data source.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Test 0/1/nhiều bão, stale source và API lỗi; không gắn nhãn active chỉ vì có bản ghi lịch sử.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-021"></a>
## T21-021 — Storm name.

- **Trạng thái:** pending.
- **Nguồn:** 21.4 Storm Detail; dòng [1100](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1100).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.4 Storm Detail.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Storm name.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-021.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Storm name.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** Timeline chuyển actual/forecast không nhầm issue_time với valid_time; bảng và map đồng bộ; null không hiển thị thành 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-022"></a>
## T21-022 — Position.

- **Trạng thái:** pending.
- **Nguồn:** 21.4 Storm Detail; dòng [1101](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1101).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.4 Storm Detail.
- **Task trước trong tiểu mục:** T21-021; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Position.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-022.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Position.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** Timeline chuyển actual/forecast không nhầm issue_time với valid_time; bảng và map đồng bộ; null không hiển thị thành 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-023"></a>
## T21-023 — Wind.

- **Trạng thái:** pending.
- **Nguồn:** 21.4 Storm Detail; dòng [1102](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1102).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.4 Storm Detail.
- **Task trước trong tiểu mục:** T21-022; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Wind.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-023.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Wind.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Timeline chuyển actual/forecast không nhầm issue_time với valid_time; bảng và map đồng bộ; null không hiển thị thành 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-024"></a>
## T21-024 — Pressure.

- **Trạng thái:** pending.
- **Nguồn:** 21.4 Storm Detail; dòng [1103](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1103).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.4 Storm Detail.
- **Task trước trong tiểu mục:** T21-023; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Pressure.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-024.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Pressure.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Timeline chuyển actual/forecast không nhầm issue_time với valid_time; bảng và map đồng bộ; null không hiển thị thành 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-025"></a>
## T21-025 — Direction.

- **Trạng thái:** pending.
- **Nguồn:** 21.4 Storm Detail; dòng [1104](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1104).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.4 Storm Detail.
- **Task trước trong tiểu mục:** T21-024; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Direction.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-025.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Direction.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Hướng bắc/đông/tây đúng; 359→1 là đổi hướng nhỏ; điểm trùng có quy tắc công bố.
- **Kịch bản tiểu mục:** Timeline chuyển actual/forecast không nhầm issue_time với valid_time; bảng và map đồng bộ; null không hiển thị thành 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-026"></a>
## T21-026 — Speed.

- **Trạng thái:** pending.
- **Nguồn:** 21.4 Storm Detail; dòng [1105](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1105).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.4 Storm Detail.
- **Task trước trong tiểu mục:** T21-025; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Speed.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-026.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Speed.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** Timeline chuyển actual/forecast không nhầm issue_time với valid_time; bảng và map đồng bộ; null không hiển thị thành 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-027"></a>
## T21-027 — Forecast table.

- **Trạng thái:** pending.
- **Nguồn:** 21.4 Storm Detail; dòng [1106](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1106).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.4 Storm Detail.
- **Task trước trong tiểu mục:** T21-026; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Forecast table.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-027.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Forecast table.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** Timeline chuyển actual/forecast không nhầm issue_time với valid_time; bảng và map đồng bộ; null không hiển thị thành 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-028"></a>
## T21-028 — Timeline.

- **Trạng thái:** pending.
- **Nguồn:** 21.4 Storm Detail; dòng [1107](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1107).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.4 Storm Detail.
- **Task trước trong tiểu mục:** T21-027; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Timeline.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-028.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Timeline.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** Timeline chuyển actual/forecast không nhầm issue_time với valid_time; bảng và map đồng bộ; null không hiển thị thành 0.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-029"></a>
## T21-029 — Select province.

- **Trạng thái:** pending.
- **Nguồn:** 21.5 Province Impact; dòng [1110](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1110).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.5 Province Impact.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Select province.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-029.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Select province.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** Khoảng cách, giao polygon và ETA có phương pháp/giới hạn; không suy wind/flood impact chỉ từ cone tâm bão.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-030"></a>
## T21-030 — Calculate distance.

- **Trạng thái:** pending.
- **Nguồn:** 21.5 Province Impact; dòng [1111](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1111).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.5 Province Impact.
- **Task trước trong tiểu mục:** T21-029; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Calculate distance.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-030.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Calculate distance.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Điểm trùng cho 0 km; cặp điểm chuẩn khớp dung sai; wrap longitude không tạo khoảng cách vòng trái đất.
- **Kịch bản tiểu mục:** Khoảng cách, giao polygon và ETA có phương pháp/giới hạn; không suy wind/flood impact chỉ từ cone tâm bão.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-031"></a>
## T21-031 — Display ETA.

- **Trạng thái:** pending.
- **Nguồn:** 21.5 Province Impact; dòng [1112](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1112).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.5 Province Impact.
- **Task trước trong tiểu mục:** T21-030; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Display ETA.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-031.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Display ETA.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** Khoảng cách, giao polygon và ETA có phương pháp/giới hạn; không suy wind/flood impact chỉ từ cone tâm bão.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-032"></a>
## T21-032 — Display impact level.

- **Trạng thái:** pending.
- **Nguồn:** 21.5 Province Impact; dòng [1113](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1113).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.5 Province Impact.
- **Task trước trong tiểu mục:** T21-031; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Display impact level.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-032.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Display impact level.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** Khoảng cách, giao polygon và ETA có phương pháp/giới hạn; không suy wind/flood impact chỉ từ cone tâm bão.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-033"></a>
## T21-033 — Display uncertainty.

- **Trạng thái:** pending.
- **Nguồn:** 21.5 Province Impact; dòng [1114](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1114).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.5 Province Impact.
- **Task trước trong tiểu mục:** T21-032; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Display uncertainty.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-033.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Display uncertainty.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UI có trạng thái 0/1/nhiều bão, loading/error/stale; tiếng Việt và keyboard hoạt động; không lỗi console.
- **Kịch bản tiểu mục:** Khoảng cách, giao polygon và ETA có phương pháp/giới hạn; không suy wind/flood impact chỉ từ cone tâm bão.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-034"></a>
## T21-034 — Show source/time.

- **Trạng thái:** pending.
- **Nguồn:** 21.5 Province Impact; dòng [1115](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1115).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.5 Province Impact.
- **Task trước trong tiểu mục:** T21-033; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Show source/time.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-034.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Show source/time.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Giữ source URL/version/checksum/time; truy ngược input; synthetic không bị gắn nguồn chính thức.
- **Kịch bản tiểu mục:** Khoảng cách, giao polygon và ETA có phương pháp/giới hạn; không suy wind/flood impact chỉ từ cone tâm bão.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-035"></a>
## T21-035 — Responsive map.

- **Trạng thái:** pending.
- **Nguồn:** 21.6 Mobile; dòng [1118](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1118).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.6 Mobile.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Responsive map.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-035.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Responsive map.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Thao tác ở 360×800,768×1024,1440×900; focus/keyboard rõ; không mất legend/disclaimer hoặc cuộn ngang.
- **Kịch bản tiểu mục:** Kiểm thử viewport 360×800, 768×1024, 1440×900; keyboard/focus/contrast; không cuộn ngang toàn trang.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-036"></a>
## T21-036 — Responsive cards.

- **Trạng thái:** pending.
- **Nguồn:** 21.6 Mobile; dòng [1119](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1119).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.6 Mobile.
- **Task trước trong tiểu mục:** T21-035; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Responsive cards.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-036.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Responsive cards.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Thao tác ở 360×800,768×1024,1440×900; focus/keyboard rõ; không mất legend/disclaimer hoặc cuộn ngang.
- **Kịch bản tiểu mục:** Kiểm thử viewport 360×800, 768×1024, 1440×900; keyboard/focus/contrast; không cuộn ngang toàn trang.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-037"></a>
## T21-037 — Responsive timeline.

- **Trạng thái:** pending.
- **Nguồn:** 21.6 Mobile; dòng [1120](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1120).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.6 Mobile.
- **Task trước trong tiểu mục:** T21-036; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Responsive timeline.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-037.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Responsive timeline.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Thao tác ở 360×800,768×1024,1440×900; focus/keyboard rõ; không mất legend/disclaimer hoặc cuộn ngang.
- **Kịch bản tiểu mục:** Kiểm thử viewport 360×800, 768×1024, 1440×900; keyboard/focus/contrast; không cuộn ngang toàn trang.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-038"></a>
## T21-038 — Test mobile width.

- **Trạng thái:** pending.
- **Nguồn:** 21.6 Mobile; dòng [1121](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1121).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.6 Mobile.
- **Task trước trong tiểu mục:** T21-037; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Test mobile width.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-038.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test mobile width.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Thao tác ở 360×800,768×1024,1440×900; focus/keyboard rõ; không mất legend/disclaimer hoặc cuộn ngang.
- **Kịch bản tiểu mục:** Kiểm thử viewport 360×800, 768×1024, 1440×900; keyboard/focus/contrast; không cuộn ngang toàn trang.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t21-039"></a>
## T21-039 — Test tablet.

- **Trạng thái:** pending.
- **Nguồn:** 21.6 Mobile; dòng [1122](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1122).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G02, G17; contract/fixture của tiểu mục 21.6 Mobile.
- **Task trước trong tiểu mục:** T21-038; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** API contract ổn định, mock có nhãn demo, GeoJSON đã xác thực; yêu cầu riêng: Test tablet.
- **File/đầu ra:** thay đổi nhỏ trong viz/frontend/; tests/frontend/; docs/frontend.md; evidence tại evidence/T21-039.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test tablet.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G21, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Thao tác ở 360×800,768×1024,1440×900; focus/keyboard rõ; không mất legend/disclaimer hoặc cuộn ngang.
- **Kịch bản tiểu mục:** Kiểm thử viewport 360×800, 768×1024, 1440×900; keyboard/focus/contrast; không cuộn ngang toàn trang.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
