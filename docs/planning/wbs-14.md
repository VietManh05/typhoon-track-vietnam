# G14 — Tuning và kiểm định theo mùa

- Trạng thái: pending; chưa nghiệm thu.
- Hiện trạng: Chưa thấy tuning pipeline.
- Đầu vào: Train/validation folds theo mùa, ngân sách trials và seed.
- Gate phụ thuộc: G09, G13.
- Vùng file dự kiến: src/typhoon_vn/training/tuning.py; configs/search-space.yaml; tests/test_tuning.py.
- Đường dẫn test/tài liệu mới là đích dự kiến, không khẳng định đã có.
- Task trong nhóm có thể đổi thứ tự theo contract/fixture; tests và tài liệu làm cùng implementation, không chờ nhóm cuối.
- DoD nhóm: Fit scaler riêng từng fold; objective dùng validation; thử seq_len 4/6/8; final test niêm phong đến model-selection freeze.

<a id="gate-g14"></a>
## Gate G14

Chỉ qua gate khi task bắt buộc có evidence. Mục tùy chọn/ngoại vi phải có quyết định và trạng thái rõ.

<a id="t14-001"></a>
## T14-001 — Chọn search space.

- **Trạng thái:** pending.
- **Nguồn:** 14. HYPERPARAMETER TUNING; dòng [933](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:933).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G09, G13; contract/fixture của tiểu mục 14. HYPERPARAMETER TUNING.
- **Task trước trong tiểu mục:** không; áp dụng gate phụ thuộc của nhóm.
- **Đầu vào:** Train/validation folds theo mùa, ngân sách trials và seed; yêu cầu riêng: Chọn search space.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/tuning.py; configs/search-space.yaml; tests/test_tuning.py; evidence tại evidence/T14-001.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chọn search space.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G14, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fit scaler riêng từng fold; objective dùng validation; thử seq_len 4/6/8; final test niêm phong đến model-selection freeze.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t14-002"></a>
## T14-002 — hidden size.

- **Trạng thái:** pending.
- **Nguồn:** 14. HYPERPARAMETER TUNING; dòng [934](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:934).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G09, G13; contract/fixture của tiểu mục 14. HYPERPARAMETER TUNING.
- **Task trước trong tiểu mục:** T14-001; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Train/validation folds theo mùa, ngân sách trials và seed; yêu cầu riêng: hidden size.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/tuning.py; configs/search-space.yaml; tests/test_tuning.py; evidence tại evidence/T14-002.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “hidden size.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G14, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fit scaler riêng từng fold; objective dùng validation; thử seq_len 4/6/8; final test niêm phong đến model-selection freeze.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t14-003"></a>
## T14-003 — layers.

- **Trạng thái:** pending.
- **Nguồn:** 14. HYPERPARAMETER TUNING; dòng [935](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:935).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G09, G13; contract/fixture của tiểu mục 14. HYPERPARAMETER TUNING.
- **Task trước trong tiểu mục:** T14-002; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Train/validation folds theo mùa, ngân sách trials và seed; yêu cầu riêng: layers.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/tuning.py; configs/search-space.yaml; tests/test_tuning.py; evidence tại evidence/T14-003.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “layers.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G14, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fit scaler riêng từng fold; objective dùng validation; thử seq_len 4/6/8; final test niêm phong đến model-selection freeze.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t14-004"></a>
## T14-004 — dropout.

- **Trạng thái:** pending.
- **Nguồn:** 14. HYPERPARAMETER TUNING; dòng [936](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:936).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G09, G13; contract/fixture của tiểu mục 14. HYPERPARAMETER TUNING.
- **Task trước trong tiểu mục:** T14-003; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Train/validation folds theo mùa, ngân sách trials và seed; yêu cầu riêng: dropout.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/tuning.py; configs/search-space.yaml; tests/test_tuning.py; evidence tại evidence/T14-004.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “dropout.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G14, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fit scaler riêng từng fold; objective dùng validation; thử seq_len 4/6/8; final test niêm phong đến model-selection freeze.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t14-005"></a>
## T14-005 — learning rate.

- **Trạng thái:** pending.
- **Nguồn:** 14. HYPERPARAMETER TUNING; dòng [937](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:937).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G09, G13; contract/fixture của tiểu mục 14. HYPERPARAMETER TUNING.
- **Task trước trong tiểu mục:** T14-004; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Train/validation folds theo mùa, ngân sách trials và seed; yêu cầu riêng: learning rate.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/tuning.py; configs/search-space.yaml; tests/test_tuning.py; evidence tại evidence/T14-005.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “learning rate.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G14, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fit scaler riêng từng fold; objective dùng validation; thử seq_len 4/6/8; final test niêm phong đến model-selection freeze.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t14-006"></a>
## T14-006 — batch size.

- **Trạng thái:** pending.
- **Nguồn:** 14. HYPERPARAMETER TUNING; dòng [938](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:938).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G09, G13; contract/fixture của tiểu mục 14. HYPERPARAMETER TUNING.
- **Task trước trong tiểu mục:** T14-005; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Train/validation folds theo mùa, ngân sách trials và seed; yêu cầu riêng: batch size.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/tuning.py; configs/search-space.yaml; tests/test_tuning.py; evidence tại evidence/T14-006.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “batch size.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G14, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fit scaler riêng từng fold; objective dùng validation; thử seq_len 4/6/8; final test niêm phong đến model-selection freeze.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t14-007"></a>
## T14-007 — sequence length.

- **Trạng thái:** pending.
- **Nguồn:** 14. HYPERPARAMETER TUNING; dòng [939](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:939).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G09, G13; contract/fixture của tiểu mục 14. HYPERPARAMETER TUNING.
- **Task trước trong tiểu mục:** T14-006; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Train/validation folds theo mùa, ngân sách trials và seed; yêu cầu riêng: sequence length.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/tuning.py; configs/search-space.yaml; tests/test_tuning.py; evidence tại evidence/T14-007.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “sequence length.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G14, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Test B=1/4, T=4/6/8; shape/dtype đúng; thay padding không đổi output hợp lệ; không qua storm boundary.
- **Kịch bản tiểu mục:** Fit scaler riêng từng fold; objective dùng validation; thử seq_len 4/6/8; final test niêm phong đến model-selection freeze.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t14-008"></a>
## T14-008 — horizon weights.

- **Trạng thái:** pending.
- **Nguồn:** 14. HYPERPARAMETER TUNING; dòng [940](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:940).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G09, G13; contract/fixture của tiểu mục 14. HYPERPARAMETER TUNING.
- **Task trước trong tiểu mục:** T14-007; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Train/validation folds theo mùa, ngân sách trials và seed; yêu cầu riêng: horizon weights.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/tuning.py; configs/search-space.yaml; tests/test_tuning.py; evidence tại evidence/T14-008.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “horizon weights.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G14, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Target đúng issue_time+h; thứ tự [6,12,24,48,72] nhất quán; thiếu +12 không lấy +18 thay.
- **Kịch bản tiểu mục:** Fit scaler riêng từng fold; objective dùng validation; thử seq_len 4/6/8; final test niêm phong đến model-selection freeze.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t14-009"></a>
## T14-009 — Chạy Optuna.

- **Trạng thái:** pending.
- **Nguồn:** 14. HYPERPARAMETER TUNING; dòng [941](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:941).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G09, G13; contract/fixture của tiểu mục 14. HYPERPARAMETER TUNING.
- **Task trước trong tiểu mục:** T14-008; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Train/validation folds theo mùa, ngân sách trials và seed; yêu cầu riêng: Chạy Optuna.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/tuning.py; configs/search-space.yaml; tests/test_tuning.py; evidence tại evidence/T14-009.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chạy Optuna.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G14, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fit scaler riêng từng fold; objective dùng validation; thử seq_len 4/6/8; final test niêm phong đến model-selection freeze.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t14-010"></a>
## T14-010 — Lưu trial.

- **Trạng thái:** pending.
- **Nguồn:** 14. HYPERPARAMETER TUNING; dòng [942](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:942).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G09, G13; contract/fixture của tiểu mục 14. HYPERPARAMETER TUNING.
- **Task trước trong tiểu mục:** T14-009; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Train/validation folds theo mùa, ngân sách trials và seed; yêu cầu riêng: Lưu trial.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/tuning.py; configs/search-space.yaml; tests/test_tuning.py; evidence tại evidence/T14-010.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Lưu trial.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G14, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fit scaler riêng từng fold; objective dùng validation; thử seq_len 4/6/8; final test niêm phong đến model-selection freeze.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t14-011"></a>
## T14-011 — Chọn best config.

- **Trạng thái:** pending.
- **Nguồn:** 14. HYPERPARAMETER TUNING; dòng [943](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:943).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G09, G13; contract/fixture của tiểu mục 14. HYPERPARAMETER TUNING.
- **Task trước trong tiểu mục:** T14-010; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Train/validation folds theo mùa, ngân sách trials và seed; yêu cầu riêng: Chọn best config.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/tuning.py; configs/search-space.yaml; tests/test_tuning.py; evidence tại evidence/T14-011.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Chọn best config.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G14, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fit scaler riêng từng fold; objective dùng validation; thử seq_len 4/6/8; final test niêm phong đến model-selection freeze.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t14-012"></a>
## T14-012 — Re-train best config.

- **Trạng thái:** pending.
- **Nguồn:** 14. HYPERPARAMETER TUNING; dòng [944](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:944).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G09, G13; contract/fixture của tiểu mục 14. HYPERPARAMETER TUNING.
- **Task trước trong tiểu mục:** T14-011; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Train/validation folds theo mùa, ngân sách trials và seed; yêu cầu riêng: Re-train best config.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/tuning.py; configs/search-space.yaml; tests/test_tuning.py; evidence tại evidence/T14-012.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Re-train best config.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G14, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Đầu ra giải quyết đúng mục việc; thử case bình thường và biên của tiểu mục bên dưới; ghi input/version/expected/actual.
- **Kịch bản tiểu mục:** Fit scaler riêng từng fold; objective dùng validation; thử seq_len 4/6/8; final test niêm phong đến model-selection freeze.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.

<a id="t14-013"></a>
## T14-013 — Đánh giá trên test một lần cuối.

- **Trạng thái:** pending.
- **Nguồn:** 14. HYPERPARAMETER TUNING; dòng [945](D:/IT-Dev/python-projects/Typhoon_vn/ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md:945).
- **Loại:** kiểm chứng rồi bổ sung phần thiếu.
- **Phụ thuộc:** G09, G13; contract/fixture của tiểu mục 14. HYPERPARAMETER TUNING.
- **Task trước trong tiểu mục:** T14-012; kiểm tra output trước khi bắt đầu.
- **Đầu vào:** Train/validation folds theo mùa, ngân sách trials và seed; yêu cầu riêng: Đánh giá trên test một lần cuối.
- **File/đầu ra:** thay đổi nhỏ trong src/typhoon_vn/training/tuning.py; configs/search-space.yaml; tests/test_tuning.py; evidence tại evidence/T14-013.md.
- **Bước thực hiện:**
  1. Định vị phần hiện có liên quan “Đánh giá trên test một lần cuối.”; ghi phần đạt/chưa đạt và ví dụ input/output.
  2. Hoàn thiện đúng mục này; giữ contract G14, không mở rộng module khác ngoài phụ thuộc bắt buộc.
  3. Kiểm chứng theo tiêu chí dưới; ghi evidence trước khi đóng task.
- **Kiểm thử riêng:** Assertion cho case thường và biên/lỗi; ghi lệnh, expected/actual và exit code; không chỉ kiểm tra hàm có tồn tại.
- **Kịch bản tiểu mục:** Fit scaler riêng từng fold; objective dùng validation; thử seq_len 4/6/8; final test niêm phong đến model-selection freeze.
- **DoD:** có output thực tế và kiểm chứng pass; evidence ghi command/input/version/expected/actual. Nếu scope tùy chọn không làm, ghi quyết định và giữ riêng với trạng thái complete.
- **Bằng chứng hiện tại:** chưa ghi; không đánh complete.
