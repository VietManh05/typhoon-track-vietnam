# G05 — Scaling

- **Ngày:** 2026-09-19.
- **Phạm vi:** T05-001–T05-009.
- **Implementation:** split trước fit; `FeatureScaler` chỉ fit train, giữ order/fill/statistics, transform validation/test không đổi statistics, save/load cho inference và inverse transform.
- **Kiểm thử:** train-only leakage test, missing/extra/reordered rejection, all-NaN/Inf handling, save/load và inverse error ≤1e-6; batch mục tiêu 41 passed.
- **Kết quả:** held-out values không tham gia fit; scaler artifact có sidecar audit.

