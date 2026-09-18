# Typhoon VN Forecast System

An operational-support system for tropical-cyclone track forecasting focused on
Vietnam and the East Sea. It is designed to turn best-track observations and
environmental data into reproducible training, multi-horizon forecasts, an API,
and a map-based dashboard. Forecasts are decision support only, not official
weather warnings.

## Architecture

```text
CMA / JTWC / JMA / IBTrACS / NCHMF / ERA5 / SST
                    |
                    v
     ingestion -> validation -> features -> versioned storage
                    |
                    v
  train / evaluate / registry (LSTM, later attention and ensemble)
                    |
                    v
       FastAPI inference -> dashboard -> alert channels
```

The module boundaries follow this flow so ingestion, modelling, serving, and
visualisation can be tested and deployed independently. The detailed design is
in [docs/architecture.md](docs/architecture.md).

## Current status

Phases 0-1 establish repository conventions, a development environment, and a
source-aware data-ingestion pipeline. The API currently exposes only health and
version endpoints; model inference and forecast endpoints intentionally belong
to later roadmap phases.

## Data ingestion

The Phase 1 pipeline preserves source files, records SHA-256 provenance, parses
supported best-track formats, and partitions canonical raw observations by source
and UTC year. Consult [docs/data-ingestion.md](docs/data-ingestion.md) before
downloading or processing a source.

## Quick start

The project is pinned to Python 3.11 (see `.python-version`). Use a Python 3.11
environment rather than the system interpreter if it is another version.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
Copy-Item .env.example .env
python -m pip install --upgrade pip
python -m pip install -e ".[api,dev,experiment]"
pre-commit install
python -m uvicorn typhoon_vn.api.app:app --reload
```

Open `http://127.0.0.1:8000/docs` to inspect the starter API. On systems with
GNU Make, `make setup`, `make serve`, and `make test` provide the same common
workflow.

## Local services

Docker Compose defines development-only PostGIS, Redis, MinIO, and API services.
After copying `.env.example` to `.env`, run:

```powershell
docker compose up --build
```

The default credentials are for local development only and must be replaced in
any shared environment. Docker Desktop is not installed in the current
workspace, so this command has not been executed here.

## Dependency groups

- `api`: FastAPI and Uvicorn for serving.
- `train`: data-science and PyTorch packages for training images/environments.
- `experiment`: DVC and MLflow for data and experiment provenance.
- `dev`: testing, formatting, linting, and pre-commit tooling.

`pyproject.toml` is the authoritative dependency declaration. The two
`requirements-*.txt` files are small deployment selectors for the API and
training images; they do not independently pin packages.

## Source baseline and Git hosting

This local repository has been initialized with the `main` branch. The roadmap
names `VietManh05/typhoon-track-vietnam` as the code baseline, but no remote
repository, clone URL, or hosting credentials were supplied. Add an approved
remote and import that baseline before making a first shared push; see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Safety note

This software must not be presented as an official warning product. Any
user-facing forecast should include its data source, issue time, model version,
uncertainty, and a clear official-warning disclaimer.
