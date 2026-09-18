# Data and experiment versioning

## DVC policy

Use DVC to track approved copies of source datasets, processed datasets, and
large model artefacts without placing them in Git. Once the Python 3.11
environment is installed, initialise it from the repository root:

```powershell
python -m dvc init
python -m dvc add data/processed/<dataset>.parquet
git add .dvc .gitignore data/processed/<dataset>.parquet.dvc
```

Choose and configure an approved remote before pushing any data. Do not add raw
third-party data unless its licence permits redistribution. The first tracked
artefacts are expected to be the cleaned dataset and training checkpoints.

## MLflow policy

`MODEL_REGISTRY_URI` defaults to `./mlruns` for local work. A training run must
log its Git revision, DVC dataset reference, configuration, metrics, artefacts,
and an immutable run ID. The shared experiment log uses that run ID as the
cross-reference; its template is [experiment-log-template.md](experiment-log-template.md).

The registry should promote a model only after an evaluation report is reviewed.
