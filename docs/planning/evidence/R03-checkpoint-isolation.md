# R03 — Cô lập checkpoint khi chạy test

- Thời gian: 2026-09-18 22:00 +07:00
- Trạng thái: complete

## Thay đổi

`tests/test_training.py::test_trainer_runs_one_epoch` nhận `tmp_path` và truyền `checkpoint_dir=tmp_path / "checkpoints"` vào `TrainingConfig`. Test không còn ghi vào thư mục `checkpoints/` của workspace.

## Kiểm chứng

- Lần chạy đầu với `tmp_path` mặc định thất bại ở setup do `PermissionError` tại `C:\Users\YOU\AppData\Local\Temp\pytest-of-YOU`; chưa chạy code test.
- Reproducer thành công: `.venv\Scripts\python.exe -m pytest tests\test_training.py::test_trainer_runs_one_epoch -q --basetemp=.pytest-tmp`
- Actual: `1 passed in 12.75s`.
- Exit code: 0.

Checkpoint trước và sau test không đổi:

- `best.pt`: `9b92a8a9d0bcb1a4704820b83289e1195b67a351a6b069bd6d2c515c7148a9ed`
- `last.pt`: `cd92781195b419b06cc4a399d85b639132e177ffc166b5951101aab52979a270`

## Kết luận

Đạt DoD R03. Các lần pytest trong workspace này cần `--basetemp=.pytest-tmp` do quyền truy cập temp mặc định.
