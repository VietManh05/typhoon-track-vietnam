# G12 — Training tái lập

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Trainer có; pipeline.py và config loader chưa có; checkpoint save thiếu state.
- Đầu vào: Config hợp lệ, split manifest, scaler fit train và dataset hash.
- Gate phụ thuộc: G05, G06, G08, G10.
- Vùng file dự kiến: src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.

<a id="gate-g12"></a>
## Gate G12

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t12-001"></a>
## T12-001 — YAML config.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [875](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:875).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: YAML config.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “YAML config.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-002"></a>
## T12-002 — Seed.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [876](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:876).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Seed.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Seed.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Lưu seed Python/NumPy/Torch/backend; cùng môi trường CPU/seed tái lập; khác seed thành run khác.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-003"></a>
## T12-003 — Deterministic settings phù hợp.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [877](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:877).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Deterministic settings phù hợp.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Deterministic settings phù hợp.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Lưu seed Python/NumPy/Torch/backend; cùng môi trường CPU/seed tái lập; khác seed thành run khác.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-004"></a>
## T12-004 — Data loader.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [878](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:878).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Data loader.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Data loader.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-005"></a>
## T12-005 — Optimizer.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [879](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:879).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Optimizer.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Optimizer.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-006"></a>
## T12-006 — Scheduler.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [880](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:880).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Scheduler.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Scheduler.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-007"></a>
## T12-007 — Training loop.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [881](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:881).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Training loop.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Training loop.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-008"></a>
## T12-008 — Validation loop.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [882](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:882).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Validation loop.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Validation loop.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-009"></a>
## T12-009 — Early stopping.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [883](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:883).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Early stopping.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Early stopping.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-010"></a>
## T12-010 — Gradient clipping.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [884](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:884).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Gradient clipping.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Gradient clipping.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Loss/gradient hữu hạn với fixture đúng; NaN/empty phải fail rõ và không lưu best checkpoint giả.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-011"></a>
## T12-011 — Best checkpoint.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [885](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:885).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Best checkpoint.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Best checkpoint.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Reload đủ state; resume so với chạy liên tục; epoch/history/LR nhất quán; checkpoint mới không đè artifact khác.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-012"></a>
## T12-012 — Last checkpoint.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [886](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:886).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Last checkpoint.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Last checkpoint.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Reload đủ state; resume so với chạy liên tục; epoch/history/LR nhất quán; checkpoint mới không đè artifact khác.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-013"></a>
## T12-013 — Resume training.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [887](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:887).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Resume training.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Resume training.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Reload đủ state; resume so với chạy liên tục; epoch/history/LR nhất quán; checkpoint mới không đè artifact khác.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-014"></a>
## T12-014 — Log metrics.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [888](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:888).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-013; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Log metrics.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-014.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Log metrics.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-015"></a>
## T12-015 — Log artifacts.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [889](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:889).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-014; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Log artifacts.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-015.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Log artifacts.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-016"></a>
## T12-016 — Log config.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [890](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:890).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-015; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Log config.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-016.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Log config.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t12-017"></a>
## T12-017 — Log dataset version.

- **Trạng thái:** pending.
- **Nguồn:** 12. TRAINING PIPELINE; dòng [891](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:891).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G05, G06, G08, G10; contract/fixture của tiểu mục 12. TRAINING PIPELINE.
- **Task trước trong tiểu mục:** T12-016; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Config hợp lệ, split manifest, scaler fit train và dataset hash; yêu cầu riêng: Log dataset version.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/trainer.py; src/typhoon_vn/training/pipeline.py; configs/phase3_lstm.yaml; src/typhoon_vn/cli.py; tests/test_training.py; evidence tại evidence/T12-017.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Log dataset version.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G12, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Output có giá trị/đơn vị/sample count/run ID/dataset/model version; expected được tính độc lập; không dùng test để tune.
- **Kịch bản tiểu mục:** Lệnh train chạy thật; 1 epoch smoke; best/last khác mục đích; resume đủ optimizer/scheduler/RNG/history; log provenance.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
