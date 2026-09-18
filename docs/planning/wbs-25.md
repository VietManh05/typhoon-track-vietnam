# G25 — CI/CD và phát hành

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Chưa thấy CI; chưa có remote/hosting được cấu hình.
- Đầu vào: Tests/lint/build tái lập và hosting được người dùng chọn.
- Gate phụ thuộc: G24.
- Vùng file dự kiến:  .github/workflows/; infra/deploy/; docs/deployment.md.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: PR có checks; model-evaluation gate; staging smoke; rollback; production deploy cần credentials và release scope rõ.

<a id="gate-g25"></a>
## Gate G25

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t25-001"></a>
## T25-001 — GitHub Actions.

- **Trạng thái:** pending.
- **Nguồn:** 25. CI/CD; dòng [1205](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1205).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục 25. CI/CD.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Tests/lint/build tái lập và hosting được người dùng chọn; yêu cầu riêng: GitHub Actions.
- **File/đầu ra:** thay đổi nhỏ trong  .github/workflows/; infra/deploy/; docs/deployment.md; evidence tại evidence/T25-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “GitHub Actions.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G25, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** PR có checks; model-evaluation gate; staging smoke; rollback; production deploy cần credentials và release scope rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t25-002"></a>
## T25-002 — Install dependencies.

- **Trạng thái:** pending.
- **Nguồn:** 25. CI/CD; dòng [1206](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1206).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục 25. CI/CD.
- **Task trước trong tiểu mục:** T25-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tests/lint/build tái lập và hosting được người dùng chọn; yêu cầu riêng: Install dependencies.
- **File/đầu ra:** thay đổi nhỏ trong  .github/workflows/; infra/deploy/; docs/deployment.md; evidence tại evidence/T25-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Install dependencies.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G25, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** PR có checks; model-evaluation gate; staging smoke; rollback; production deploy cần credentials và release scope rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t25-003"></a>
## T25-003 — Lint.

- **Trạng thái:** pending.
- **Nguồn:** 25. CI/CD; dòng [1207](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1207).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục 25. CI/CD.
- **Task trước trong tiểu mục:** T25-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tests/lint/build tái lập và hosting được người dùng chọn; yêu cầu riêng: Lint.
- **File/đầu ra:** thay đổi nhỏ trong  .github/workflows/; infra/deploy/; docs/deployment.md; evidence tại evidence/T25-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lint.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G25, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** PR có checks; model-evaluation gate; staging smoke; rollback; production deploy cần credentials và release scope rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t25-004"></a>
## T25-004 — Unit test.

- **Trạng thái:** pending.
- **Nguồn:** 25. CI/CD; dòng [1208](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1208).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục 25. CI/CD.
- **Task trước trong tiểu mục:** T25-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tests/lint/build tái lập và hosting được người dùng chọn; yêu cầu riêng: Unit test.
- **File/đầu ra:** thay đổi nhỏ trong  .github/workflows/; infra/deploy/; docs/deployment.md; evidence tại evidence/T25-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Unit test.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G25, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** PR có checks; model-evaluation gate; staging smoke; rollback; production deploy cần credentials và release scope rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t25-005"></a>
## T25-005 — Integration test.

- **Trạng thái:** pending.
- **Nguồn:** 25. CI/CD; dòng [1209](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1209).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục 25. CI/CD.
- **Task trước trong tiểu mục:** T25-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tests/lint/build tái lập và hosting được người dùng chọn; yêu cầu riêng: Integration test.
- **File/đầu ra:** thay đổi nhỏ trong  .github/workflows/; infra/deploy/; docs/deployment.md; evidence tại evidence/T25-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Integration test.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G25, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** PR có checks; model-evaluation gate; staging smoke; rollback; production deploy cần credentials và release scope rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t25-006"></a>
## T25-006 — Build backend.

- **Trạng thái:** pending.
- **Nguồn:** 25. CI/CD; dòng [1210](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1210).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục 25. CI/CD.
- **Task trước trong tiểu mục:** T25-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tests/lint/build tái lập và hosting được người dùng chọn; yêu cầu riêng: Build backend.
- **File/đầu ra:** thay đổi nhỏ trong  .github/workflows/; infra/deploy/; docs/deployment.md; evidence tại evidence/T25-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Build backend.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G25, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Build/config exit 0; smoke service; secrets/raw/checkpoints ngoài build context trừ artifact được chọn.
- **Kịch bản tiểu mục:** PR có checks; model-evaluation gate; staging smoke; rollback; production deploy cần credentials và release scope rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t25-007"></a>
## T25-007 — Build frontend.

- **Trạng thái:** pending.
- **Nguồn:** 25. CI/CD; dòng [1211](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1211).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục 25. CI/CD.
- **Task trước trong tiểu mục:** T25-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tests/lint/build tái lập và hosting được người dùng chọn; yêu cầu riêng: Build frontend.
- **File/đầu ra:** thay đổi nhỏ trong  .github/workflows/; infra/deploy/; docs/deployment.md; evidence tại evidence/T25-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Build frontend.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G25, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Build/config exit 0; smoke service; secrets/raw/checkpoints ngoài build context trừ artifact được chọn.
- **Kịch bản tiểu mục:** PR có checks; model-evaluation gate; staging smoke; rollback; production deploy cần credentials và release scope rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t25-008"></a>
## T25-008 — Build Docker image.

- **Trạng thái:** pending.
- **Nguồn:** 25. CI/CD; dòng [1212](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1212).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục 25. CI/CD.
- **Task trước trong tiểu mục:** T25-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tests/lint/build tái lập và hosting được người dùng chọn; yêu cầu riêng: Build Docker image.
- **File/đầu ra:** thay đổi nhỏ trong  .github/workflows/; infra/deploy/; docs/deployment.md; evidence tại evidence/T25-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Build Docker image.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G25, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Build/config exit 0; smoke service; secrets/raw/checkpoints ngoài build context trừ artifact được chọn.
- **Kịch bản tiểu mục:** PR có checks; model-evaluation gate; staging smoke; rollback; production deploy cần credentials và release scope rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t25-009"></a>
## T25-009 — Security/basic dependency check nếu phù hợp.

- **Trạng thái:** pending.
- **Nguồn:** 25. CI/CD; dòng [1213](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1213).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục 25. CI/CD.
- **Task trước trong tiểu mục:** T25-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tests/lint/build tái lập và hosting được người dùng chọn; yêu cầu riêng: Security/basic dependency check nếu phù hợp.
- **File/đầu ra:** thay đổi nhỏ trong  .github/workflows/; infra/deploy/; docs/deployment.md; evidence tại evidence/T25-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Security/basic dependency check nếu phù hợp.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G25, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** PR có checks; model-evaluation gate; staging smoke; rollback; production deploy cần credentials và release scope rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t25-010"></a>
## T25-010 — Deploy staging.

- **Trạng thái:** pending.
- **Nguồn:** 25. CI/CD; dòng [1214](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1214).
- **Loại:** chuẩn bị/test cục bộ trước; chạy thật cần nguồn, credentials và phạm vi vận hành phù hợp.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục 25. CI/CD.
- **Task trước trong tiểu mục:** T25-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tests/lint/build tái lập và hosting được người dùng chọn; yêu cầu riêng: Deploy staging.
- **File/đầu ra:** thay đổi nhỏ trong  .github/workflows/; infra/deploy/; docs/deployment.md; evidence tại evidence/T25-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Deploy staging.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G25, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** PR có checks; model-evaluation gate; staging smoke; rollback; production deploy cần credentials và release scope rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t25-011"></a>
## T25-011 — Model evaluation gate.

- **Trạng thái:** pending.
- **Nguồn:** 25. CI/CD; dòng [1215](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1215).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục 25. CI/CD.
- **Task trước trong tiểu mục:** T25-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tests/lint/build tái lập và hosting được người dùng chọn; yêu cầu riêng: Model evaluation gate.
- **File/đầu ra:** thay đổi nhỏ trong  .github/workflows/; infra/deploy/; docs/deployment.md; evidence tại evidence/T25-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Model evaluation gate.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G25, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** PR có checks; model-evaluation gate; staging smoke; rollback; production deploy cần credentials và release scope rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t25-012"></a>
## T25-012 — Production deployment.

- **Trạng thái:** pending.
- **Nguồn:** 25. CI/CD; dòng [1216](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1216).
- **Loại:** chuẩn bị/test cục bộ trước; chạy thật cần nguồn, credentials và phạm vi vận hành phù hợp.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục 25. CI/CD.
- **Task trước trong tiểu mục:** T25-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tests/lint/build tái lập và hosting được người dùng chọn; yêu cầu riêng: Production deployment.
- **File/đầu ra:** thay đổi nhỏ trong  .github/workflows/; infra/deploy/; docs/deployment.md; evidence tại evidence/T25-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Production deployment.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G25, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** PR có checks; model-evaluation gate; staging smoke; rollback; production deploy cần credentials và release scope rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t25-013"></a>
## T25-013 — Rollback.

- **Trạng thái:** pending.
- **Nguồn:** 25. CI/CD; dòng [1217](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:1217).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G24; contract/fixture của tiểu mục 25. CI/CD.
- **Task trước trong tiểu mục:** T25-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Tests/lint/build tái lập và hosting được người dùng chọn; yêu cầu riêng: Rollback.
- **File/đầu ra:** thay đổi nhỏ trong  .github/workflows/; infra/deploy/; docs/deployment.md; evidence tại evidence/T25-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Rollback.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G25, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** PR có checks; model-evaluation gate; staging smoke; rollback; production deploy cần credentials và release scope rõ.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
