# G04 — Feature engineering

- **Ngày:** 2026-09-19.
- **Phạm vi:** T04-001–T04-054.
- **Implementation:** một `FeatureBuilder` dùng chung train/serve cho position lags/deltas, motion, coast/reference locations, cyclic time, intensity; environmental extractor dùng latest field available tại issue time, SST/gradient, MSLP, wind 850/200, humidity và shear; data dictionary có order/dtype/unit/source/missing policy/version/fingerprint.
- **Kiểm thử:** acceptance phủ canonical order, real elapsed time, no cross-storm lag, geospatial, SST point/gradient, wind shear=5 m/s, và từ chối field có `available_at` sau issue time. Batch mục tiêu: 41 passed.
- **Quyết định ngoại vi:** không tải ERA5/OISST trong test; archive hoàn thiện sau sự kiện không được dùng làm feature realtime nếu chưa available tại issue time.

