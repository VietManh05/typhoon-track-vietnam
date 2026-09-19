# G06 — Dataset, window, horizon và split

- **Ngày:** 2026-09-19.
- **Phạm vi:** T06-001–T06-026.
- **Implementation:** configurable sequence length, sliding windows theo storm, float32 input/mask, direct horizons 6/12/24/48/72h bằng exact timestamp lookup, bỏ sample thiếu target, split whole-storm/random hoặc whole-storm/year, manifest lưu train/validation/test IDs/policy/seed/counts và reject overlap.
- **Kiểm thử:** shape/dtype/mask/window/horizon/storm boundary/gap/duplicate/cross-year/zero-ratio/no-overlap; batch mục tiêu 41 passed.
- **Kết quả:** không suy target bằng row offset và không leak storm giữa splits.

