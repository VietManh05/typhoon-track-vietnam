# G03 — Làm sạch và thời gian

- Trạng thái: complete; nghiệm thu tại [G03-cleaning.md](evidence/G03-cleaning.md).
- Hiện trạng: Có pipeline; cần kiểm thử leakage và thời gian.
- Đầu vào: Canonical observations và quy tắc ưu tiên nguồn.
- Gate phụ thuộc: G01.
- Vùng file dự kiến: src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Không sửa raw; không nội suy qua cơn bão; không dùng tương lai cho feature phục vụ inference; báo cáo số dòng thay đổi.

<a id="gate-g03"></a>
## Gate G03

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t03-001"></a>
## T03-001 — `parse()`.

- **Trạng thái:** complete.
- **Nguồn:** 3.1 Pipeline; dòng [586](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:586).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.1 Pipeline.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: `parse()`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`parse()`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Pipeline chạy lại cùng input cho cùng output; reconcile provenance không bị mất qua bridge/export; raw không bị ghi đè.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-001.md](evidence/T03-001.md).

<a id="t03-002"></a>
## T03-002 — `validate()`.

- **Trạng thái:** complete.
- **Nguồn:** 3.1 Pipeline; dòng [587](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:587).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.1 Pipeline.
- **Task trước trong tiểu mục:** T03-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: `validate()`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`validate()`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Pipeline chạy lại cùng input cho cùng output; reconcile provenance không bị mất qua bridge/export; raw không bị ghi đè.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-002.md](evidence/T03-002.md).

<a id="t03-003"></a>
## T03-003 — `deduplicate()`.

- **Trạng thái:** complete.
- **Nguồn:** 3.1 Pipeline; dòng [588](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:588).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.1 Pipeline.
- **Task trước trong tiểu mục:** T03-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: `deduplicate()`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`deduplicate()`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Pipeline chạy lại cùng input cho cùng output; reconcile provenance không bị mất qua bridge/export; raw không bị ghi đè.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-003.md](evidence/T03-003.md).

<a id="t03-004"></a>
## T03-004 — `merge()`.

- **Trạng thái:** complete.
- **Nguồn:** 3.1 Pipeline; dòng [589](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:589).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.1 Pipeline.
- **Task trước trong tiểu mục:** T03-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: `merge()`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`merge()`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Pipeline chạy lại cùng input cho cùng output; reconcile provenance không bị mất qua bridge/export; raw không bị ghi đè.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-004.md](evidence/T03-004.md).

<a id="t03-005"></a>
## T03-005 — `sort()`.

- **Trạng thái:** complete.
- **Nguồn:** 3.1 Pipeline; dòng [590](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:590).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.1 Pipeline.
- **Task trước trong tiểu mục:** T03-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: `sort()`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`sort()`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Pipeline chạy lại cùng input cho cùng output; reconcile provenance không bị mất qua bridge/export; raw không bị ghi đè.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-005.md](evidence/T03-005.md).

<a id="t03-006"></a>
## T03-006 — `interpolate()`.

- **Trạng thái:** complete.
- **Nguồn:** 3.1 Pipeline; dòng [591](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:591).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.1 Pipeline.
- **Task trước trong tiểu mục:** T03-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: `interpolate()`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`interpolate()`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Pipeline chạy lại cùng input cho cùng output; reconcile provenance không bị mất qua bridge/export; raw không bị ghi đè.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-006.md](evidence/T03-006.md).

<a id="t03-007"></a>
## T03-007 — `feature()`.

- **Trạng thái:** complete.
- **Nguồn:** 3.1 Pipeline; dòng [592](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:592).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.1 Pipeline.
- **Task trước trong tiểu mục:** T03-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: `feature()`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`feature()`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Pipeline chạy lại cùng input cho cùng output; reconcile provenance không bị mất qua bridge/export; raw không bị ghi đè.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-007.md](evidence/T03-007.md).

<a id="t03-008"></a>
## T03-008 — `export()`.

- **Trạng thái:** complete.
- **Nguồn:** 3.1 Pipeline; dòng [593](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:593).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.1 Pipeline.
- **Task trước trong tiểu mục:** T03-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: `export()`.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “`export()`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Pipeline chạy lại cùng input cho cùng output; reconcile provenance không bị mất qua bridge/export; raw không bị ghi đè.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-008.md](evidence/T03-008.md).

<a id="t03-009"></a>
## T03-009 — Thống kê missing.

- **Trạng thái:** complete.
- **Nguồn:** 3.2 Missing Values; dòng [596](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:596).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.2 Missing Values.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: Thống kê missing.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Thống kê missing.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Fixture hai bão xen kẽ, gap đầu/cuối và gap dài; chỉ dùng policy đã công bố; feature tại t không đọc observation sau t.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-009.md](evidence/T03-009.md).

<a id="t03-010"></a>
## T03-010 — Phân biệt missing thật và giá trị không hợp lệ.

- **Trạng thái:** complete.
- **Nguồn:** 3.2 Missing Values; dòng [597](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:597).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.2 Missing Values.
- **Task trước trong tiểu mục:** T03-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: Phân biệt missing thật và giá trị không hợp lệ.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Phân biệt missing thật và giá trị không hợp lệ.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Fixture hai bão xen kẽ, gap đầu/cuối và gap dài; chỉ dùng policy đã công bố; feature tại t không đọc observation sau t.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-010.md](evidence/T03-010.md).

<a id="t03-011"></a>
## T03-011 — Nội suy theo từng storm.

- **Trạng thái:** complete.
- **Nguồn:** 3.2 Missing Values; dòng [598](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:598).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.2 Missing Values.
- **Task trước trong tiểu mục:** T03-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: Nội suy theo từng storm.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Nội suy theo từng storm.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Fixture hai bão xen kẽ, gap đầu/cuối và gap dài; chỉ dùng policy đã công bố; feature tại t không đọc observation sau t.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-011.md](evidence/T03-011.md).

<a id="t03-012"></a>
## T03-012 — Không dùng 0 mặc định cho dữ liệu chưa biết.

- **Trạng thái:** complete.
- **Nguồn:** 3.2 Missing Values; dòng [599](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:599).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.2 Missing Values.
- **Task trước trong tiểu mục:** T03-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: Không dùng 0 mặc định cho dữ liệu chưa biết.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Không dùng 0 mặc định cho dữ liệu chưa biết.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fixture hai bão xen kẽ, gap đầu/cuối và gap dài; chỉ dùng policy đã công bố; feature tại t không đọc observation sau t.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-012.md](evidence/T03-012.md).

<a id="t03-013"></a>
## T03-013 — Gắn cờ dữ liệu được nội suy.

- **Trạng thái:** complete.
- **Nguồn:** 3.2 Missing Values; dòng [600](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:600).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.2 Missing Values.
- **Task trước trong tiểu mục:** T03-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: Gắn cờ dữ liệu được nội suy.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Gắn cờ dữ liệu được nội suy.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Fixture hai bão xen kẽ, gap đầu/cuối và gap dài; chỉ dùng policy đã công bố; feature tại t không đọc observation sau t.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-013.md](evidence/T03-013.md).

<a id="t03-014"></a>
## T03-014 — Test interpolation.

- **Trạng thái:** complete.
- **Nguồn:** 3.2 Missing Values; dòng [601](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:601).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.2 Missing Values.
- **Task trước trong tiểu mục:** T03-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: Test interpolation.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Test interpolation.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Fixture thiếu đầu/cuối chuỗi, gap dài và hai storm; không dùng future observations; missing không tự đổi thành 0.
- **Kịch bản tiểu mục:** Fixture hai bão xen kẽ, gap đầu/cuối và gap dài; chỉ dùng policy đã công bố; feature tại t không đọc observation sau t.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-014.md](evidence/T03-014.md).

<a id="t03-015"></a>
## T03-015 — Chuẩn hóa UTC.

- **Trạng thái:** complete.
- **Nguồn:** 3.3 Time Normalization; dòng [604](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:604).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.3 Time Normalization.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: Chuẩn hóa UTC.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chuẩn hóa UTC.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt.
- **Kịch bản tiểu mục:** Test UTC+7, qua ngày/năm, duplicate và khoảng cách 6h/12h; resample có cờ, giới hạn gap và không tạo future leakage.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-015.md](evidence/T03-015.md).

<a id="t03-016"></a>
## T03-016 — Kiểm tra duplicate timestamp.

- **Trạng thái:** complete.
- **Nguồn:** 3.3 Time Normalization; dòng [605](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:605).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.3 Time Normalization.
- **Task trước trong tiểu mục:** T03-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: Kiểm tra duplicate timestamp.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra duplicate timestamp.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt.
- **Kịch bản tiểu mục:** Test UTC+7, qua ngày/năm, duplicate và khoảng cách 6h/12h; resample có cờ, giới hạn gap và không tạo future leakage.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-016.md](evidence/T03-016.md).

<a id="t03-017"></a>
## T03-017 — Sắp xếp theo thời gian.

- **Trạng thái:** complete.
- **Nguồn:** 3.3 Time Normalization; dòng [606](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:606).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.3 Time Normalization.
- **Task trước trong tiểu mục:** T03-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: Sắp xếp theo thời gian.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Sắp xếp theo thời gian.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt.
- **Kịch bản tiểu mục:** Test UTC+7, qua ngày/năm, duplicate và khoảng cách 6h/12h; resample có cờ, giới hạn gap và không tạo future leakage.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-017.md](evidence/T03-017.md).

<a id="t03-018"></a>
## T03-018 — Kiểm tra khoảng cách thời gian.

- **Trạng thái:** complete.
- **Nguồn:** 3.3 Time Normalization; dòng [607](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:607).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.3 Time Normalization.
- **Task trước trong tiểu mục:** T03-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: Kiểm tra khoảng cách thời gian.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Kiểm tra khoảng cách thời gian.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** UTC+7 và UTC cùng instant cho cùng kết quả; naive/invalid time bị reject; issue_time và valid_time tách biệt.
- **Kịch bản tiểu mục:** Test UTC+7, qua ngày/năm, duplicate và khoảng cách 6h/12h; resample có cờ, giới hạn gap và không tạo future leakage.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-018.md](evidence/T03-018.md).

<a id="t03-019"></a>
## T03-019 — Resample nếu cần.

- **Trạng thái:** complete.
- **Nguồn:** 3.3 Time Normalization; dòng [608](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:608).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.3 Time Normalization.
- **Task trước trong tiểu mục:** T03-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: Resample nếu cần.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Resample nếu cần.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Test UTC+7, qua ngày/năm, duplicate và khoảng cách 6h/12h; resample có cờ, giới hạn gap và không tạo future leakage.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-019.md](evidence/T03-019.md).

<a id="t03-020"></a>
## T03-020 — Ghi lại quy tắc resampling.

- **Trạng thái:** complete.
- **Nguồn:** 3.3 Time Normalization; dòng [609](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:609).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G01; contract/fixture của tiểu mục 3.3 Time Normalization.
- **Task trước trong tiểu mục:** T03-019; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Canonical observations và quy tắc ưu tiên nguồn; yêu cầu riêng: Ghi lại quy tắc resampling.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/features/cleaning.py; src/typhoon_vn/features/bridge.py; scripts/run_phase2.py; tests/test_features.py; evidence tại evidence/T03-020.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Ghi lại quy tắc resampling.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G03, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Test UTC+7, qua ngày/năm, duplicate và khoảng cách 6h/12h; resample có cờ, giới hạn gap và không tạo future leakage.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** [T03-020.md](evidence/T03-020.md).
