# R06 — Target theo thời gian thực

- Trạng thái: complete
- Files: `src/typhoon_vn/datasets/typhoon_dataset.py`, `tests/test_phase2_contracts.py`.

Dataset giờ lập map timestamp→row riêng từng storm và lấy target tại `issue_time + horizon * time_step_hours`. Input window cũng phải có nhịp thời gian đều. Timestamp trùng trong cùng storm bị từ chối rõ ràng; target thiếu khiến sample bị bỏ thay vì lấy nhầm hàng kế tiếp.

Kiểm chứng trong full suite: fixture bỏ target +12 h nhưng giữ +18 h không sinh sample sai; target đúng theo timestamp; duplicate bị reject; grouping không vượt storm. Full suite `49 passed`, exit code 0; report `phase2-pytest.xml`.
