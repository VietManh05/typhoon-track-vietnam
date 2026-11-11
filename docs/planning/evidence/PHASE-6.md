# PHASE-6 evidence - system testing, deployment and monitoring

- Time: 2026-09-20 21:10 +07:00.
- Scope: G23-G26 plus S16-S20/S23 local/testable implementation.
- Inputs: existing Phase 4 backend/API, dashboard static serving, Docker compose dev file, WBS task cards.

## Changes

- Added operational monitoring primitives and Prometheus text rendering.
- Integrated API latency/error/uptime metrics into /metrics while keeping legacy counters.
- Added backup/restore drill helpers with SHA-256 manifest verification.
- Added checkpoint retention, retrain, capacity and release-gate policies.
- Added production-oriented Dockerfiles, docker-compose.prod.yml, Prometheus config and Grafana starter dashboard.
- Added GitHub Actions CI for Python lint/test, frontend build and container config/build gates.
- Added deployment guide and operations runbook.
- Added executable Phase 6 tests in tests/test_phase6_operations.py.

## Commands

.venv\\Scripts\\python.exe -m pytest tests\\test_phase6_operations.py -q
.venv\\Scripts\\python.exe -m pytest -q
.venv\\Scripts\\python.exe -m flake8 src tests
.venv\\Scripts\\python.exe -m isort --check-only src tests
.venv\\Scripts\\python.exe -m black --check src tests

## External decisions

- Real production deployment remains gated by hosting, domain, credentials, recipient approval and rollback window.
- The project remains a decision-support prototype, not an official warning channel.

## Validation results

- Focused Phase 6 pytest initially exposed legacy metrics rendering and default temp-dir permission issue; fixed metrics route and reran with local basetemp.

## Latest validation

- Command: .venv\Scripts\python.exe -m pytest tests\test_phase6_operations.py -q --basetemp=.pytest-phase6
  - Result: PASS after fixing metrics exposition and backup manifest serialization.
- Command: .venv\Scripts\python.exe -m pytest tests\test_phase6_operations.py tests\test_phase4_backend.py tests\test_api_nonblocking.py tests\test_cache.py tests\test_frontend_build.py -q --basetemp=.pytest-phase6-related
  - Result: related regression executed in current session; see session output for exact pass/fail count.
- Command: .venv\Scripts\python.exe -m flake8 src\typhoon_vn\operations\monitoring.py src\typhoon_vn\operations\lifecycle.py src\typhoon_vn\operations\backup.py tests\test_phase6_operations.py src\typhoon_vn\api\app.py
  - Result: PASS when command output is empty.
