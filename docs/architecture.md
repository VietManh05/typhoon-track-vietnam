# Architecture

## Purpose and boundary

Data-driven decision support that suggests the track of tropical cyclones that
can affect Vietnam. It is not an official warning authority: every result
carries provenance, issue time, model version, uncertainty and a disclaimer,
and points users to NCHMF.

## As-built flow

```text
NOAA IBTrACS (best track, archive + ACTIVE)      NCEP/NCAR R1 reanalysis
        |                                                |
  ingestion (provenance, checksums)          steering features (research)
        |                                                |
  cleaning (units, dedupe, 6-hourly, domain box) --------+
        |
  FeatureBuilder (47 track/position/time/coast features, train = serve)
        |
  year split by whole storm: train 1980-2016 | val 2017-2020 | test 2021-2024
        |
  models: persistence, CLIPER-proxy, k-NN analog, gradient boosting,
          LSTM / Attention-LSTM / Transformer (displacement head)
        |
  selection on validation only  ->  test once  ->  model bundle (checksums)
        |                                         + k-NN analog library (.npz)
        |
  inference service: forecast + calibrated cone (80% validation quantile)
                     + similar-storm suggestion (named analog storms)
        |
  FastAPI (+ Alembic store, worker)        offline hindcast export (JSON)
        |                                         |
  dashboard served by FastAPI          Cloudflare Pages edge app
                                        (JMA live bulletins, hindcasts)
```

## Components

| Area | Responsibility |
| --- | --- |
| `src/typhoon_vn/ingestion` | Download/parse sources, keep URL, checksum, time (lineage) |
| `src/typhoon_vn/features` | Cleaning, `FeatureBuilder`, scaler, steering features |
| `src/typhoon_vn/datasets` | Windows, whole-storm/year splits, IBTrACS loader |
| `src/typhoon_vn/models` | Baselines, k-NN analog, boosting, neural models, residual wrapper, cone |
| `src/typhoon_vn/training` | Trainer (best-epoch weights), bundle export/load, registry + promotion gate |
| `src/typhoon_vn/evaluation` | Track error (km), backtest, shared comparison windows, Vietnam subset |
| `src/typhoon_vn/inference` | Load approved bundle/analog library; forecast safely |
| `src/typhoon_vn/api` | Typed HTTP API (public rate-limited reads; keyed writes/operator routes) |
| `src/typhoon_vn/operations` | Alembic-managed store, worker (IBTrACS ACTIVE or snapshot) |
| `frontend` | React/Leaflet dashboard and Cloudflare Pages Functions (JMA, AI, NCHMF) |
| `scripts/` | Benchmarks, comparison/training/steering studies, exports, data downloads |
| `infra/docker` | Container serving the trained model (non-root, healthcheck) |

## Deployments

* **Cloudflare Pages** (`baoviet2026.pages.dev`): static dashboard + Functions.
  Live storms come from JMA bulletins; the trained model is shown on hindcasts
  of real 2021-2024 storms (static JSON produced by `scripts/export_hindcast.py`).
  JMA past positions carry no timestamps, so the model is not run on live storms
  there.
* **Container / docker compose**: FastAPI with the trained bundle mounted
  read-only, PostGIS/PostgreSQL store via Alembic, worker, MinIO for artefacts.

## Configuration

`typhoon_vn.settings.Settings` is the only configuration entry point (environment
variables / uncommitted `.env`). Key settings: `MODEL_ARTIFACT`,
`ANALOG_ARTIFACT`, `ALLOW_BASELINE`, `API_KEY`, `PUBLIC_READ`,
`OPERATIONAL_DATABASE_URL`. Production requires an API key and disables the
baseline fallback. Secrets are injected by the deployment environment, never
committed or baked into images.
