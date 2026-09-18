# Architecture

## Purpose and boundary

The system provides data-driven track-forecast decision support for tropical
cyclones that can affect Vietnam. It is not an official warning authority.
Every consumer-facing result must carry provenance, issue time, model version,
uncertainty, and a disclaimer.

## Logical flow

```text
Raw sources
  CMA | JTWC | JMA | IBTrACS | NCHMF | ERA5 | NOAA OISST
    -> ingestion
    -> validation, de-duplication, normalisation
    -> feature builder and versioned feature store
    -> train / evaluate / model registry
    -> inference API
    -> dashboard, impact assessment, and alert channels
```

## Module ownership

| Area | Responsibility | Phase introduced |
| --- | --- | --- |
| `src/typhoon_vn/ingestion` | Download, parse, and preserve source provenance | 1 |
| `src/typhoon_vn/features` | Validated, train/serve-consistent features | 2 |
| `src/typhoon_vn/models`, `training` | Baselines, models, and evaluation | 3–4 |
| `src/typhoon_vn/inference` | Load approved artefacts and forecast safely | 6 |
| `src/typhoon_vn/api` | Typed external HTTP interface | 6–7 |
| `viz/frontend` | Map and dashboard experience | 7 |
| `infra` | Container and deployment definitions | 0, then 10+ |

## Local development dependencies

`docker-compose.yml` supplies PostGIS for future spatial persistence, Redis for
future caching/jobs, and MinIO for future checkpoint artefacts. The Phase 0 API
does not make network calls to these services: they are started now to make
later integrations explicit and reproducible.

## Configuration

`typhoon_vn.settings.Settings` is the only configuration entry point. It reads
environment variables and an uncommitted `.env` file. Defaults are deliberately
local-only. Production secrets must be injected by the deployment environment,
not committed in a repository or placed in image layers.
