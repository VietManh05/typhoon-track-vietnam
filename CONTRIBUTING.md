# Contributing

## Before contributing

1. Use Python 3.11 and create `.env` from `.env.example`; never commit local secrets.
2. Install the groups needed by the change. For the full local test path: `python -m pip install -e ".[api,train,ingestion,dev]"`.
3. Run `python -m pip check`. Install both hook stages with `pre-commit install --hook-type pre-commit --hook-type commit-msg` when the dev tool is available.
4. Keep raw data, credentials, checkpoints, caches, and generated experiment artifacts out of Git. Version only approved/licensed datasets.

## Workflow

- Local integration branches are `main` and `develop`. Start concrete feature work from `develop`.
- Name a branch `feature/<task-id>-<short-slug>`, for example `feature/t18-001-typhoons-schema`. Do not create speculative empty branches. See [branch workflow](docs/branching.md).
- Keep one task or documented task slice per branch and include tests/evidence for behavioral changes.
- Run `python -m pytest -q --basetemp=.pytest-local` before review. Run `pre-commit run --all-files` when hooks are installed.
- Record dataset/model/bundle versions and clearly label synthetic data, baselines, and uncertainty limitations.
- Never checkout/reset a dirty user worktree, add files in bulk, rename a remote, or push without explicit authorization.

## Commit convention

Use Conventional Commits:

```text
<type>(optional-scope): imperative summary
```

Allowed types: `feat`, `fix`, `docs`, `test`, `refactor`, `build`, `ci`, `chore`, and `perf`. Use `!` or a `BREAKING CHANGE:` footer for incompatible changes.

Examples:

```text
feat(ingestion): parse IBTrACS timestamps as UTC
fix(features): fit scaler only on training storms
docs(architecture): clarify model-bundle promotion
```

## Review checklist

- No secret, unapproved dataset, checkpoint, or generated experiment output is added.
- Timezone, units, CRS, and geographic-coordinate assumptions are explicit.
- Train/validation/test leakage and train-only preprocessing are considered.
- API changes preserve source, issue/valid/generated times, model/dataset versions, uncertainty wording, warnings, and official-warning disclaimer.
- New artifact loading validates schemas/checksums and fails closed.
- Evidence records command, input, expected, actual, and exit code; file existence alone is not completion.

## Repository hosting

The configured remote is `origin` at `https://github.com/VietManh05/typhoon-track-vietnam.git`. Do not rename, replace, publish, or push it without maintainer authorization. Remote branch/protection settings require hosting access and must not be inferred from local refs.
