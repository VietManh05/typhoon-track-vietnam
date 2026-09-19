# Typhoon VN Forecast System

Vietnam-focused tropical-cyclone track forecasting research and decision-support software. It ingests source observations, builds leakage-aware features and multi-horizon datasets, trains PyTorch models, exports validated bundles, and serves forecasts through FastAPI.

> **Safety:** forecasts are decision support only, not official weather warnings. Follow NCHMF and competent authorities for operational decisions.

## Verified status

The local test path currently covers ingestion, feature contracts, storm-safe splitting, train-only scaling, deterministic checkpoint/resume, model-bundle integrity, synthetic training smoke, trained/baseline inference, and API validation/auth/rate limiting.

This repository is **not production-ready**. PostGIS/Alembic migrations, Redis read/invalidation, a live-provider worker, subscription ownership, and alert delivery remain backlog items. Synthetic smoke results and the constant-motion baseline are not evidence of real-storm forecast skill.

## Architecture

```text
source providers -> canonical UTC observations -> cleaning/features
                 -> storm-safe datasets -> train/evaluate
                 -> checksum-validated model bundle
                 -> reusable inference service -> FastAPI
```

See [architecture](docs/architecture.md), [observation contract](docs/contracts/observations.md), [feature contract](docs/contracts/features.md), and [model-bundle contract](docs/contracts/model-bundle.md).

## Requirements

- Python 3.11
- PowerShell commands below assume Windows; equivalent shell commands work elsewhere.
- Docker is optional for local API/unit tests and has not been used to prove the PostGIS/Redis production path.

## Setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[api,train,ingestion,dev]"
python -m pip check
python -m pytest -q --basetemp=.pytest-local
```

The project is installed editable as `typhoon-vn-forecast-system`; `pyproject.toml` is the authoritative dependency declaration.

## CLI

Inspect the available commands:

```powershell
python -m typhoon_vn.cli --help
python -m typhoon_vn.cli train --help
```

Run the configured LSTM experiment and export a reloadable bundle:

```powershell
python -m typhoon_vn.cli train --config configs/phase3_lstm.yaml --output-dir runs/phase3-lstm
```

The checked-in configuration uses 100 epochs and is not a quick command. The integration test uses a one-epoch synthetic fixture in a temporary directory. CLI output labels such runs `synthetic-demo`; do not report them as real-storm metrics.

## API

Start the development API:

```powershell
python -m uvicorn typhoon_vn.api.app:app --reload
```

Then open <http://127.0.0.1:8000/docs>. Implemented routes include health/readiness/version, forecast, active storms, track/impact, observation ingestion, subscriptions, and draft alerts. Production mode requires an API key and disables baseline fallback; the current operational store is still a draft and must not be treated as a migrated PostGIS deployment.

## Local services

`docker-compose.yml` declares development PostGIS, Redis, MinIO, and API services:

```powershell
docker compose up --build
```

This compose path is not currently accepted as production evidence: migration, environment naming, cache read/invalidation, and worker-service gaps are documented in [R14 operational gaps](docs/planning/evidence/R14-operational-gaps.md).

## Data and provenance

See [data ingestion](docs/data-ingestion.md) before downloading or processing any source. Raw data, checkpoints, local secrets, caches, and experiment artifacts are ignored by Git. User-facing forecasts retain source, issue time, model/dataset version, uncertainty wording, warnings, and disclaimer.

## Repository workflow

The existing remote is `origin` at `VietManh05/typhoon-track-vietnam`. Local `main` and `develop` branches exist. Follow [branch workflow](docs/branching.md) and [contribution guidance](CONTRIBUTING.md); do not push or rename the remote without explicit authorization.

## License

Released under the [MIT License](LICENSE).
