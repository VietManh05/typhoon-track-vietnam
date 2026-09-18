# G00 — Nền tảng repository và môi trường

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Có phần nền tảng; CLI vẫn placeholder; toàn bộ cây làm việc untracked.
- Đầu vào: Cấu trúc hiện có, Python 3.11.9 và quy ước dự án.
- Gate phụ thuộc: Không.
- Vùng file dự kiến: .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Môi trường tái tạo được; lệnh thật có exit code đúng; không đưa dữ liệu, secrets, checkpoint vào Git.

<a id="gate-g00"></a>
## Gate G00

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t00-001"></a>
## T00-001 — Tạo repository `typhoon-vn-forecast-system`.

- **Trạng thái:** pending.
- **Nguồn:** 0.1 Repository; dòng [387](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:387).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.1 Repository.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo repository `typhoon-vn-forecast-system`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo repository `typhoon-vn-forecast-system`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Kiểm tra Git status trước/sau; không add hàng loạt cây untracked; kiểm tra ignore bằng file fixture; remote/branch/push chỉ khi task thực sự cần.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-002"></a>
## T00-002 — Tạo `main`, `develop`.

- **Trạng thái:** pending.
- **Nguồn:** 0.1 Repository; dòng [388](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:388).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.1 Repository.
- **Task trước trong tiểu mục:** T00-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `main`, `develop`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `main`, `develop`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Kiểm tra Git status trước/sau; không add hàng loạt cây untracked; kiểm tra ignore bằng file fixture; remote/branch/push chỉ khi task thực sự cần.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-003"></a>
## T00-003 — Tạo branch theo feature.

- **Trạng thái:** pending.
- **Nguồn:** 0.1 Repository; dòng [389](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:389).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.1 Repository.
- **Task trước trong tiểu mục:** T00-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo branch theo feature.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo branch theo feature.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Kiểm tra Git status trước/sau; không add hàng loạt cây untracked; kiểm tra ignore bằng file fixture; remote/branch/push chỉ khi task thực sự cần.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-004"></a>
## T00-004 — Thiết lập `.gitignore`.

- **Trạng thái:** pending.
- **Nguồn:** 0.1 Repository; dòng [390](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:390).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.1 Repository.
- **Task trước trong tiểu mục:** T00-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Thiết lập `.gitignore`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Thiết lập `.gitignore`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Kiểm tra Git status trước/sau; không add hàng loạt cây untracked; kiểm tra ignore bằng file fixture; remote/branch/push chỉ khi task thực sự cần.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-005"></a>
## T00-005 — Tạo `README.md`.

- **Trạng thái:** pending.
- **Nguồn:** 0.1 Repository; dòng [391](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:391).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.1 Repository.
- **Task trước trong tiểu mục:** T00-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `README.md`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `README.md`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Nội dung khớp implementation đã kiểm chứng; ví dụ chạy được; link đúng; phân biệt demo/thực nghiệm/vận hành.
- **Kịch bản tiểu mục:** Kiểm tra Git status trước/sau; không add hàng loạt cây untracked; kiểm tra ignore bằng file fixture; remote/branch/push chỉ khi task thực sự cần.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-006"></a>
## T00-006 — Tạo `LICENSE`.

- **Trạng thái:** pending.
- **Nguồn:** 0.1 Repository; dòng [392](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:392).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.1 Repository.
- **Task trước trong tiểu mục:** T00-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `LICENSE`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `LICENSE`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Kiểm tra Git status trước/sau; không add hàng loạt cây untracked; kiểm tra ignore bằng file fixture; remote/branch/push chỉ khi task thực sự cần.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-007"></a>
## T00-007 — Tạo `CONTRIBUTING.md`.

- **Trạng thái:** pending.
- **Nguồn:** 0.1 Repository; dòng [393](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:393).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.1 Repository.
- **Task trước trong tiểu mục:** T00-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `CONTRIBUTING.md`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `CONTRIBUTING.md`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Kiểm tra Git status trước/sau; không add hàng loạt cây untracked; kiểm tra ignore bằng file fixture; remote/branch/push chỉ khi task thực sự cần.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-008"></a>
## T00-008 — Thiết lập Conventional Commits.

- **Trạng thái:** pending.
- **Nguồn:** 0.1 Repository; dòng [394](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:394).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.1 Repository.
- **Task trước trong tiểu mục:** T00-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Thiết lập Conventional Commits.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Thiết lập Conventional Commits.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Kiểm tra Git status trước/sau; không add hàng loạt cây untracked; kiểm tra ignore bằng file fixture; remote/branch/push chỉ khi task thực sự cần.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-009"></a>
## T00-009 — Thiết lập pre-commit.

- **Trạng thái:** pending.
- **Nguồn:** 0.1 Repository; dòng [395](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:395).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.1 Repository.
- **Task trước trong tiểu mục:** T00-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Thiết lập pre-commit.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Thiết lập pre-commit.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Kiểm tra Git status trước/sau; không add hàng loạt cây untracked; kiểm tra ignore bằng file fixture; remote/branch/push chỉ khi task thực sự cần.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-010"></a>
## T00-010 — Chạy lint lần đầu.

- **Trạng thái:** pending.
- **Nguồn:** 0.1 Repository; dòng [396](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:396).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.1 Repository.
- **Task trước trong tiểu mục:** T00-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Chạy lint lần đầu.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chạy lint lần đầu.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Kiểm tra Git status trước/sau; không add hàng loạt cây untracked; kiểm tra ignore bằng file fixture; remote/branch/push chỉ khi task thực sự cần.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-011"></a>
## T00-011 — Commit cấu trúc ban đầu.

- **Trạng thái:** pending.
- **Nguồn:** 0.1 Repository; dòng [397](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:397).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.1 Repository.
- **Task trước trong tiểu mục:** T00-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Commit cấu trúc ban đầu.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Commit cấu trúc ban đầu.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Kiểm tra Git status trước/sau; không add hàng loạt cây untracked; kiểm tra ignore bằng file fixture; remote/branch/push chỉ khi task thực sự cần.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-012"></a>
## T00-012 — Tạo `data/raw`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [402](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:402).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `data/raw`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `data/raw`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-013"></a>
## T00-013 — Tạo `data/interim`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [403](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:403).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `data/interim`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `data/interim`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-014"></a>
## T00-014 — Tạo `data/processed`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [404](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:404).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `data/processed`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `data/processed`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-015"></a>
## T00-015 — Tạo `data/external`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [405](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:405).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-014; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `data/external`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `data/external`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-016"></a>
## T00-016 — Tạo `src/ingestion`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [406](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:406).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `src/ingestion`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `src/ingestion`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-017"></a>
## T00-017 — Tạo `src/preprocessing`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [407](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:407).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `src/preprocessing`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `src/preprocessing`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-018"></a>
## T00-018 — Tạo `src/features`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [408](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:408).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-017; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `src/features`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-018.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `src/features`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-019"></a>
## T00-019 — Tạo `src/datasets`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [409](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:409).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-018; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `src/datasets`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-019.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `src/datasets`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-020"></a>
## T00-020 — Tạo `src/models`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [410](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:410).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-019; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `src/models`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-020.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `src/models`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-021"></a>
## T00-021 — Tạo `src/training`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [411](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:411).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-020; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `src/training`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-021.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `src/training`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-022"></a>
## T00-022 — Tạo `src/inference`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [412](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:412).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-021; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `src/inference`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-022.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `src/inference`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-023"></a>
## T00-023 — Tạo `src/evaluation`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [413](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:413).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-022; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `src/evaluation`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-023.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `src/evaluation`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-024"></a>
## T00-024 — Tạo `src/alerts`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [414](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:414).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-023; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `src/alerts`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-024.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `src/alerts`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-025"></a>
## T00-025 — Tạo `api`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [415](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:415).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-024; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `api`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-025.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `api`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-026"></a>
## T00-026 — Tạo `frontend`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [416](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:416).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-025; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `frontend`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-026.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `frontend`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-027"></a>
## T00-027 — Tạo `tests/unit`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [417](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:417).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-026; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `tests/unit`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-027.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `tests/unit`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đổi đơn vị đúng một lần; missing bị mask; shear tính từ vector 850/200hPa; áp suất đầu ra hPa.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-028"></a>
## T00-028 — Tạo `tests/integration`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [418](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:418).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-027; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `tests/integration`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-028.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `tests/integration`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-029"></a>
## T00-029 — Tạo `tests/model`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [419](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:419).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-028; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `tests/model`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-029.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `tests/model`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-030"></a>
## T00-030 — Tạo `configs`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [420](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:420).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-029; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `configs`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-030.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `configs`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-031"></a>
## T00-031 — Tạo `docs`.

- **Trạng thái:** pending.
- **Nguồn:** 0.2 Cấu trúc thư mục; dòng [421](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:421).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.2 Cấu trúc thư mục.
- **Task trước trong tiểu mục:** T00-030; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `docs`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-031.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `docs`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Giữ namespace src/typhoon_vn hiện có; kiểm tra imports và đóng gói; thư mục tương đương được ghi mapping thay vì tạo hai implementation.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-032"></a>
## T00-032 — Khóa Python version.

- **Trạng thái:** pending.
- **Nguồn:** 0.3 Environment; dòng [426](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:426).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.3 Environment.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Khóa Python version.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-032.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Khóa Python version.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Dùng .venv Python 3.11; chạy import smoke trong môi trường sạch; lỗi cấu hình phải fail-fast, không lặng lẽ dùng default sai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-033"></a>
## T00-033 — Tạo `pyproject.toml`.

- **Trạng thái:** pending.
- **Nguồn:** 0.3 Environment; dòng [427](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:427).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.3 Environment.
- **Task trước trong tiểu mục:** T00-032; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `pyproject.toml`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-033.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `pyproject.toml`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Dùng .venv Python 3.11; chạy import smoke trong môi trường sạch; lỗi cấu hình phải fail-fast, không lặng lẽ dùng default sai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-034"></a>
## T00-034 — Tạo environment.

- **Trạng thái:** pending.
- **Nguồn:** 0.3 Environment; dòng [428](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:428).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.3 Environment.
- **Task trước trong tiểu mục:** T00-033; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo environment.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-034.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo environment.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Dùng .venv Python 3.11; chạy import smoke trong môi trường sạch; lỗi cấu hình phải fail-fast, không lặng lẽ dùng default sai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-035"></a>
## T00-035 — Cài PyTorch.

- **Trạng thái:** pending.
- **Nguồn:** 0.3 Environment; dòng [429](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:429).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.3 Environment.
- **Task trước trong tiểu mục:** T00-034; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Cài PyTorch.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-035.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cài PyTorch.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Dùng .venv Python 3.11; chạy import smoke trong môi trường sạch; lỗi cấu hình phải fail-fast, không lặng lẽ dùng default sai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-036"></a>
## T00-036 — Cài Pandas/NumPy.

- **Trạng thái:** pending.
- **Nguồn:** 0.3 Environment; dòng [430](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:430).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.3 Environment.
- **Task trước trong tiểu mục:** T00-035; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Cài Pandas/NumPy.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-036.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cài Pandas/NumPy.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Dùng .venv Python 3.11; chạy import smoke trong môi trường sạch; lỗi cấu hình phải fail-fast, không lặng lẽ dùng default sai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-037"></a>
## T00-037 — Cài Scikit-learn.

- **Trạng thái:** pending.
- **Nguồn:** 0.3 Environment; dòng [431](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:431).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.3 Environment.
- **Task trước trong tiểu mục:** T00-036; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Cài Scikit-learn.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-037.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cài Scikit-learn.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Dùng .venv Python 3.11; chạy import smoke trong môi trường sạch; lỗi cấu hình phải fail-fast, không lặng lẽ dùng default sai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-038"></a>
## T00-038 — Cài FastAPI/Uvicorn.

- **Trạng thái:** pending.
- **Nguồn:** 0.3 Environment; dòng [432](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:432).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.3 Environment.
- **Task trước trong tiểu mục:** T00-037; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Cài FastAPI/Uvicorn.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-038.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cài FastAPI/Uvicorn.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Dùng .venv Python 3.11; chạy import smoke trong môi trường sạch; lỗi cấu hình phải fail-fast, không lặng lẽ dùng default sai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-039"></a>
## T00-039 — Cài SQLAlchemy/Alembic.

- **Trạng thái:** pending.
- **Nguồn:** 0.3 Environment; dòng [433](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:433).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.3 Environment.
- **Task trước trong tiểu mục:** T00-038; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Cài SQLAlchemy/Alembic.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-039.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cài SQLAlchemy/Alembic.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** DB trống và DB có dữ liệu upgrade được; invalid records bị constraints reject; GiST test trên PostGIS thật.
- **Kịch bản tiểu mục:** Dùng .venv Python 3.11; chạy import smoke trong môi trường sạch; lỗi cấu hình phải fail-fast, không lặng lẽ dùng default sai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-040"></a>
## T00-040 — Cài Pytest.

- **Trạng thái:** pending.
- **Nguồn:** 0.3 Environment; dòng [434](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:434).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.3 Environment.
- **Task trước trong tiểu mục:** T00-039; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Cài Pytest.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-040.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cài Pytest.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Dùng .venv Python 3.11; chạy import smoke trong môi trường sạch; lỗi cấu hình phải fail-fast, không lặng lẽ dùng default sai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-041"></a>
## T00-041 — Cài MLflow.

- **Trạng thái:** pending.
- **Nguồn:** 0.3 Environment; dòng [435](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:435).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.3 Environment.
- **Task trước trong tiểu mục:** T00-040; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Cài MLflow.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-041.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cài MLflow.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Dùng .venv Python 3.11; chạy import smoke trong môi trường sạch; lỗi cấu hình phải fail-fast, không lặng lẽ dùng default sai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-042"></a>
## T00-042 — Cài Optuna.

- **Trạng thái:** pending.
- **Nguồn:** 0.3 Environment; dòng [436](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:436).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.3 Environment.
- **Task trước trong tiểu mục:** T00-041; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Cài Optuna.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-042.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Cài Optuna.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Dùng .venv Python 3.11; chạy import smoke trong môi trường sạch; lỗi cấu hình phải fail-fast, không lặng lẽ dùng default sai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-043"></a>
## T00-043 — Tạo `.env.example`.

- **Trạng thái:** pending.
- **Nguồn:** 0.3 Environment; dòng [437](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:437).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.3 Environment.
- **Task trước trong tiểu mục:** T00-042; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo `.env.example`.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-043.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo `.env.example`.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Dùng .venv Python 3.11; chạy import smoke trong môi trường sạch; lỗi cấu hình phải fail-fast, không lặng lẽ dùng default sai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-044"></a>
## T00-044 — Tạo config loader.

- **Trạng thái:** pending.
- **Nguồn:** 0.3 Environment; dòng [438](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:438).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.3 Environment.
- **Task trước trong tiểu mục:** T00-043; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo config loader.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-044.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo config loader.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Dùng .venv Python 3.11; chạy import smoke trong môi trường sạch; lỗi cấu hình phải fail-fast, không lặng lẽ dùng default sai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t00-045"></a>
## T00-045 — Tạo Makefile/justfile.

- **Trạng thái:** pending.
- **Nguồn:** 0.3 Environment; dòng [439](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:439).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** Không; contract/fixture của tiểu mục 0.3 Environment.
- **Task trước trong tiểu mục:** T00-044; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Cấu trúc hiện có, Python 3.11.9 và quy ước dự án; yêu cầu riêng: Tạo Makefile/justfile.
- **File/đầu ra:** thay đổi nhỏ trong .gitignore; pyproject.toml; Makefile; src/typhoon_vn/cli.py; .pre-commit-config.yaml; evidence tại evidence/T00-045.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Tạo Makefile/justfile.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G00, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Artefact đúng vị trí/quy ước; kiểm tra ignore/import/command tương ứng; không ghi đè dữ liệu người dùng.
- **Kịch bản tiểu mục:** Dùng .venv Python 3.11; chạy import smoke trong môi trường sạch; lỗi cấu hình phải fail-fast, không lặng lẽ dùng default sai.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
