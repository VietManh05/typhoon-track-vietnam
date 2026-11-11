# Operations runbook

Version: 0.1.0-phase7-local

Typhoon VN is not an official warning system. Production infrastructure acceptance is pending.

1. Check /health, /ready and /metrics. Record UTC time, request ID, deployment/model version and error response; do not include secrets in incident reports.
2. If readiness fails, inspect database connectivity and model-bundle validation. Do not enable baseline fallback in production to conceal a missing model.
3. For missing NCHMF weather, inspect /api/weather/nchmf. A 503 means the source could not be fetched/parsed and there is no cache. Cached fallback is marked metadata.isStale; observedAt remains the source time. A successful HTTP response alone does not establish fresh observations.
4. Check source URLs and timestamps before comparing forecasts. Homepage temperatures and bulletin links are not storm-center observations and must not enter the training dataset as such.
5. If a provider changes markup, retain a local response checksum and reproduce with a fixture. Do not replace missing values with zeros or report a successful ingestion.
6. Stop affected alert delivery during investigation; preserve pending/retry/dead-letter records. This acceptance run does not send messages to real recipients.

## Backup and recovery

`typhoon_vn.operations.backup.BackupManager` copies a file, writes its SHA-256 manifest, and checks that hash before restore. It is a file-level helper, not a transactional backup of a running PostGIS or SQLite database. Quiesce writers/use the database's backup facility first. Restore into an isolated target, test queries and check model manifests before switching traffic.

Keep previous application image, model bundle and configuration versions. Registry paths may be machine-specific; verify them after copying to another host. Roll back only to a tested compatible database/model combination. Run focused tests and health/readiness after recovery.

## Routine validation

Run `python -m pytest tests/test_phase6_operations.py tests/test_nchmf.py -q` for local contracts. Record actual results in planning evidence. See [deployment](deployment.md) for infrastructure prerequisites.
