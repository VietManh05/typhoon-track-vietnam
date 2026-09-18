# Feature contract

`typhoon_vn.features.build.FeatureBuilder` is the shared train/serve feature path. Its `FEATURE_COLUMNS` tuple is the canonical, versioned vocabulary and order.

Rules:

1. Derive features before selecting columns.
2. Training datasets and serving use `FeatureBuilder.transform` and select `FEATURE_COLUMNS` in that exact order.
3. Missing requested columns and duplicate feature names are errors; a persisted scaler rejects missing or reordered columns.
4. Targets are looked up by `issue_time + horizon * time_step_hours`, not row offset. A missing +12 h observation cannot be replaced by +18 h.
5. Input windows must be regular at `time_step_hours`, timestamps must be unique per storm, and no window/target crosses a storm boundary.
6. Split membership is by whole storm. When split by year, each storm is assigned by its final observed UTC year so a storm crossing New Year remains in one set.
7. The scaler is fitted only on the train split. Its feature order, fill values, means and scales are persisted and reused without refit for validation/test/inference.
