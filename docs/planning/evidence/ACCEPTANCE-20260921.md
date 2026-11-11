# Acceptance verification — 2026-09-21

- **Scope:** current local regression plus the public Cloudflare Pages release; the Python/VPS backend and real alert delivery are not deployed.
- **Workspace:** dirty changes were preserved; no reset, clean, commit, push, or secret persistence.

## Results

| Gate | Command summary | Actual | Exit |
|---|---|---:|---:|
| Planning | `validate_plan.py` | 818/818 mapped; 731 nodes; 3,236 links; source unchanged | 0 |
| Python lint | flake8 + isort check + Black check on `src tests migrations` | pass; 133 files unchanged | 0 |
| Backend regression | pytest full suite | 235 passed, 1 skipped, 3 warnings | 0 |
| PostGIS | integration test against PostGIS 16/3.4 | 1 passed | 0 |
| Frontend and Pages Functions tests | Node test runner | 15 passed | 0 |
| Frontend type/build | TypeScript no-emit + Vite production build | pass | 0 |
| Python dependencies | `pip check` | no broken requirements | 0 |
| Frontend dependencies | production npm audit, high threshold | 0 vulnerabilities | 0 |
| Compose | development, preview, and production config with ephemeral local values | valid | 0 |

## Artifacts

- `acceptance-20260921-pytest.xml`
- `acceptance-20260921-postgis.xml`
- Production frontend bundle under `src/typhoon_vn/dashboard/`

## Remaining external gates

- Licensed/current real data credentials and operational data validation.
- Real alert recipients/channels and explicit send approval.
- A reviewed live tropical-cyclone feed and trained-model backend.
- Monitoring observation window, rollback drill, and formal release approval.

These items are not represented as locally complete or production-ready.
