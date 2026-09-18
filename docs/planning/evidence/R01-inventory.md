# R01 — Kiểm kê trạng thái làm việc

- Thời gian: 2026-09-18 22:00 +07:00
- Trạng thái: complete

## Lệnh và kết quả

1. `git status --short`
   - Expected: liệt kê chính xác file tracked/untracked.
   - Actual: toàn bộ cây dự án hiện là untracked (`??`), gồm `src/`, `tests/`, `docs/`, cấu hình, dữ liệu placeholder và checkpoint.
   - Exit code: 0.
2. `git rev-parse --verify HEAD`
   - Expected: xác định commit nền nếu có.
   - Actual: `fatal: Needed a single revision`; repository chưa có commit nền.
   - Exit code: 128.
3. `git diff --stat`
   - Actual: rỗng vì không có file tracked; không được dùng kết quả này để kết luận workspace sạch.
   - Exit code: 0.
4. `dir /s /b src\*.py tests\*.py`
   - Actual: 55 source Python files và 6 test files được kiểm kê; namespace triển khai là `src/typhoon_vn`.
   - Exit code: 0.

## Checkpoint cần giữ nguyên

- `checkpoints/best.pt`: SHA-256 `9b92a8a9d0bcb1a4704820b83289e1195b67a351a6b069bd6d2c515c7148a9ed`
- `checkpoints/last.pt`: SHA-256 `cd92781195b419b06cc4a399d85b639132e177ffc166b5951101aab52979a270`

## Kết luận

Không xóa/reset/add hàng loạt. Git diff rỗng không có ý nghĩa khi toàn bộ dự án untracked. Tiếp theo: R02 kiểm tra môi trường.
