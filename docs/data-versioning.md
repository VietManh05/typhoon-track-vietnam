# Data and experiment versioning

## DVC policy

Use DVC to track approved copies of source datasets, processed datasets, and
large model artefacts without placing them in Git. The repository is already
initialised for DVC and includes a licence-safe synthetic fixture stage:

```powershell
python -m dvc repro phase2-fixture
python -m dvc status
```

The stage consumes `tests/fixtures/phase2_track.csv`, records dependency/output
hashes in `dvc.lock`, and produces ignored files under `data/processed/`.
Changing the fixture, feature code, or build script invalidates the stage.

Choose and configure an approved remote before pushing any data. The remote URL
is never committed; an operator sets `DVC_REMOTE_URL` and runs:

```powershell
python scripts/configure_dvc_remote.py
```

This writes DVC's local config only. Do not add or push raw third-party data
unless its licence permits redistribution.

## MLflow policy

`MODEL_REGISTRY_URI` defaults to `./mlruns` for local work. A training run must
log its Git revision, DVC dataset reference, configuration, metrics, artefacts,
and an immutable run ID. The shared experiment log uses that run ID as the
cross-reference; its template is [experiment-log-template.md](experiment-log-template.md).

The registry should promote a model only after an evaluation report is reviewed.
