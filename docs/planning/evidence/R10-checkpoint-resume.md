# R10 — Checkpoint/resume deterministic

- **Trạng thái:** complete
- **Files:** `src/typhoon_vn/training/trainer.py`, `tests/test_training_resume.py`.

Checkpoint version 2 lưu model, optimizer, scheduler, epoch, history, best epoch/loss, patience và RNG Python/NumPy/Torch/CUDA. Checkpoint được ghi atomically sau scheduler/history/early-stop state. Loader rỗng và metric không hữu hạn bị từ chối trước khi tạo best giả. Scheduler mismatch/version/state thiếu fail closed.

Regression so sánh train CPU 2 epoch liên tục với 1 epoch + resume: history/LR/early-stop state giống nhau và weights khớp `atol=1e-7, rtol=0`.

Command cuối: `.venv\Scripts\python.exe -m pytest -q --basetemp=.pytest-final --junitxml=docs\planning\evidence\R10-R14-pytest.xml`

Actual: **61 passed, 2 dependency warnings, 12.34s, exit 0**.
