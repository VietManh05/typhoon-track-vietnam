# Contributing

## Before contributing

1. Use Python 3.11 and create `.env` from `.env.example`; never commit it.
2. Install the development tools with `python -m pip install -e ".[api,dev,experiment]"`.
3. Install the repository hooks with `pre-commit install`.
4. Keep raw data, credentials, model checkpoints, and generated experiment
   artefacts out of Git. Version approved datasets with DVC instead.

## Workflow

- Create a short-lived branch from `main` using a descriptive name such as
  `feat/ibtracs-ingestion` or `fix/timestamp-validation`.
- Keep a pull request focused on one concern and include tests for behavioural
  changes.
- Run `make test` and `pre-commit run --all-files` before requesting review.
- Record a dataset version and MLflow run ID for any model-result claim.

## Commit convention

Use Conventional Commits:

```text
<type>(optional-scope): imperative summary
```

Allowed types are `feat`, `fix`, `docs`, `test`, `refactor`, `build`, `ci`,
`chore`, and `perf`. Examples:

```text
feat(ingestion): parse IBTrACS timestamps as UTC
fix(features): fit scaler only on training storms
docs(architecture): clarify model-registry promotion
```

Use `!` or a `BREAKING CHANGE:` footer for incompatible changes.

## Review checklist

- No secret, raw dataset, checkpoint, or generated experiment output is added.
- Timestamp and geographic-coordinate assumptions are explicit.
- Train/validation/test leakage has been considered.
- API-facing changes preserve the forecast disclaimer and provenance fields.

## Repository hosting

The local repository has no upstream remote yet. A maintainer with access to
the chosen host should add the remote, import/fork the approved baseline, and
then make the first shared push. Do not guess an organisation or publish the
repository without that approval.
