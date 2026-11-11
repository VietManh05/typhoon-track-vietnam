# G14 — Tuning và kiểm định theo mùa

- **Ngày:** 2026-09-19.
- **Trạng thái:** complete; phạm vi T14-001–T14-013.
- **Implementation/decision:** Optuna search space bao phủ hidden/layers/dropout/lr/batch/sequence/horizon weights, objective chỉ nhận validation folds, trial được lưu và final test bị khóa ở đúng một lần.
- **Coverage:** `tests/test_phase3_management.py; reports/evaluation/sequence-length-ablation.json`.
- **Lệnh focused:** `.venv/Scripts/python.exe -m pytest tests/test_baselines.py tests/test_models.py tests/test_uncertainty.py tests/test_training.py tests/test_training_resume.py tests/test_training_pipeline.py tests/test_model_bundle.py tests/test_phase3_loss_contract.py tests/test_phase3_management.py tests/test_phase3_training_contracts.py tests/test_environment_forecast.py tests/test_evaluation.py -q`.
- **Actual focused:** **61 passed**, 1 cảnh báo PyTorch nested-tensor, exit 0; JUnit `phase3-functional-pytest.xml`.
- **Lệnh regression:** `.venv/Scripts/python.exe -m pytest -q --ignore=tests/test_frontend_build.py --ignore=tests/test_health.py --ignore=tests/test_inference_api.py`.
- **Actual regression:** **131 passed**, 1 cảnh báo PyTorch nested-tensor, exit 0; JUnit `phase3-regression-pytest.xml`.
- **Expected:** contract bình thường, biên và failure-mode của nhóm đều pass; không đọc final-test trong selection và không đổi nghĩa uncertainty.
- **Phạm vi bằng chứng:** fixture local/synthetic kiểm chứng chức năng và tính tái lập. Không diễn giải các số synthetic thành chất lượng khí tượng hay quyền promote production.
