# Post-season evaluation report template

Version: 0.1.0-phase7-local

Status: pending real-season data and independent evaluation. Not an official warning system.

Record the following before approving a completed report:

- Season/date range, storm IDs, approved sources, licenses and dataset checksums.
- Training/validation/final-test storm splits; model/bundle hash and selection policy.
- Track error in km at +6/+12/+24/+48/+72 hours, sample counts, excluded cases and missing-data policy.
- Persistence baseline on identical issue times/horizons and physical coordinates.
- Intensity errors with units, uncertainty coverage/calibration and failure cases.
- Historical official-forecast comparison matched by source issue and valid time.
- Ingestion delays, outages, alert delivery outcomes and operator review.
- Reproducible commands, environment versions, actual pass/fail results and artifact paths.
- Remaining limitations and explicit promotion/rollback decision.

Do not fill metrics from synthetic fixtures or describe unavailable historical comparisons as complete.
