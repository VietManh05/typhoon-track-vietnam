# Task Plan: Typhoon VN complete roadmap implementation

## Goal
Implement the existing Vietnam typhoon forecasting roadmap end to end, reusing the existing Python modules, with a runnable local API/dashboard, reproducible training/evaluation, operational persistence/workers/alerts, deployment configuration, tests, and honest documentation of external prerequisites.

## Next Step
Run the existing test suite and inventory integration boundaries before implementing the missing application layers.

## Current Phase
Phase 1: discovery and baseline validation

## Phases
### Phase 1: Discovery and baseline
- [x] Read skill, README, architecture, roadmap, and source inventory.
- [x] Confirm scope: user explicitly selected the entire roadmap including API/dashboard.
- [ ] Run baseline tests and inspect data/model integration.
- **Status:** in_progress

### Phase 2: Reproducible data, training, evaluation and registry
- [ ] Connect CLI to cleaning/training; preserve train/serve feature contract.
- [ ] Fix leakage, timing and checkpoint issues that compromise reproducibility.
- [ ] Add artifact manifests, quality-gated promotion and evaluation tooling.
- **Status:** pending

### Phase 3: Inference and operational backend
- [ ] Add validated forecast/track/active/impact endpoints and provenance.
- [ ] Implement persistence, observations worker, cache, alert rules and throttling.
- [ ] Add authentication, rate limiting, health and metrics.
- **Status:** pending

### Phase 4: Dashboard
- [ ] Implement responsive Vietnamese/English map, tracks, forecast uncertainty, timeline and location inspection.
- [ ] Show data/model provenance, demo state and official-warning disclaimer.
- **Status:** pending

### Phase 5: Operations and documentation
- [ ] Add deployment/CI, backup, monitoring and operator runbooks.
- [ ] Map roadmap requirements to implemented evidence or explicit external dependencies.
- **Status:** pending

### Phase 6: Verification and delivery
- [ ] Run unit/integration tests, formatting/lint and local end-to-end verification.
- [ ] Record actual results, limitations and remaining external work.
- **Status:** pending

## Decisions Made
- Preserve all pre-existing files: repository currently has an entirely untracked working tree.
- Resolver returned no selected named plan; use legacy project-root planning files.
- Do not describe synthetic demonstrations as trained/validated operational forecasts.
- No remote publishing or sending alert messages is authorized by this implementation request.

## Errors Encountered
- Sandbox process creation failed with `helper_unknown_error: setup refresh had errors`; approved escalated read commands work.

## External prerequisites
Real forecast skill, official forecast comparisons, live provider credentials, licensed geographic inputs, hosting credentials and deployment validation require external resources. Record these accurately; do not mark unverified production outcomes complete.

- Baseline pytest failed collection: torch and FastAPI missing; dependency install running. apply_patch update failed because sandbox helper cannot initialize; use approved shell writes.
