# Observation contract

## Canonical meaning

- Positions use WGS84 decimal degrees and canonical names `lat`/`lon`.
- Event time is `timestamp`; all accepted datetimes must be timezone-aware and are normalised to UTC.
- `downloaded_at` records acquisition time, is also timezone-aware, and is normalised to UTC.
- Raw wind retains `wind` + `wind_unit`; the Phase-2 bridge converts supported `kt|knot|knots|m/s|ms` values to canonical `wind_ms`.
- Unknown wind units with a numeric wind value are rejected, never silently converted to missing.
- Coordinates and numeric observations must be finite. Latitude/longitude are range checked.
- Provenance fields are `source`, `source_url`, `source_file_checksum`, `dataset_version`, and `downloaded_at`. They survive the raw-to-clean bridge when present.

## Forecast times

- `issue_time`: UTC time at the final input observation.
- `horizon_hours`: positive supported lead relative to `issue_time`.
- `valid_time`: exactly `issue_time + horizon_hours`; response/request models reject naive datetimes.
- `generated_at`: UTC service generation time and may differ from issue time.

## Safety

Pydantic public contracts forbid extra fields and NaN/Infinity. Forecast output must include source, model and dataset versions, uncertainty metadata, warnings and the official-warning disclaimer.
