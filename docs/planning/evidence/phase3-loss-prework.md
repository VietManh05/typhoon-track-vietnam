# Phase 3 prework — synthetic loss contracts

- **Thời gian:** 2026-09-19 (Asia/Ho_Chi_Minh)
- **Phạm vi:** prework cho G10/T10-001..T10-004 bằng tensor synthetic; không phụ thuộc dữ liệu Phase 2.
- **Trạng thái planning:** không chuyển G10 hoặc T10 sang complete vì dependency G08 và cổng M1 chưa đạt.

## Thay đổi

- Harden `HaversineLoss`: validate shape/dtype/finite/latitude, reduction hợp lệ và wrap longitude qua dateline.
- Harden `MultiHorizonLoss`: validate số horizon/class, component weights, horizon weights, tensor shapes, prediction finite và class target hợp lệ.
- Bỏ hành vi clamp class target âm/vượt miền; dữ liệu sai nay fail rõ thay vì bị sửa im lặng.
- Thêm `tests/test_phase3_loss_contract.py` kiểm tra loss/gradient hữu hạn, invalid config, NaN/empty, class range, horizon weighting và Haversine chuẩn/dateline.

## Kiểm chứng

- Focused regression: `python -m pytest tests/test_phase3_loss_contract.py tests/test_training.py tests/test_training_resume.py tests/test_training_pipeline.py -q` → **21 passed in 8.70s**, exit 0.
- JUnit: `docs/planning/evidence/phase3-loss-prework-pytest.xml`.
- Target lint/format: flake8, Black check và isort check cho hai file thay đổi đều pass.
- Full suite: **89 passed, 1 failed**, 2 dependency warnings. Failure ở `tests/test_inference_api.py::test_missing_artifact_and_time_freshness_fail_or_warn` do thay đổi inference/frontend đồng thời ngoài lát cắt loss; focused training regression vẫn pass.
- Repository-wide lint bị chặn bởi ba F401 trong file frontend đồng thời `tests/test_frontend_build.py`; file này không thuộc thay đổi hiện tại.

## Giới hạn

Đây chỉ là contract kỹ thuật bằng dữ liệu synthetic. Chưa chứng minh target units/horizon từ dữ liệu thật, model skill, calibration hoặc promotion. T10-001..T10-004 vẫn pending cho đến khi dependencies được nghiệm thu.
