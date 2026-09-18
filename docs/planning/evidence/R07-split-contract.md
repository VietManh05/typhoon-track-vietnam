# R07 — Split storm/năm

- Trạng thái: complete
- Files: `src/typhoon_vn/datasets/typhoon_dataset.py`, `tests/test_phase2_contracts.py`.

## Kết quả

- Validate ratio trong `[0,1)` và tổng phải `<1`.
- Ratio bằng 0 tạo đúng tập rỗng, không ép lấy một storm/năm.
- Random split vẫn phân theo whole storm.
- Year split gán toàn bộ storm theo năm UTC của fix cuối, vì vậy storm qua 31/12→01/01 không bị chia giữa tập.
- Seed vẫn là input quyết định cho random split.

Kiểm chứng: full suite `49 passed`, exit code 0; report `phase2-pytest.xml`.
