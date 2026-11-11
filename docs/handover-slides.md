# Typhoon VN handover outline

Version: 0.1.0-phase7-local

Status: local demo handover outline; production acceptance remains pending.
Typhoon VN is decision support, not an official warning system.

## Slide 1 — Purpose and current state

- Vietnam-focused tropical-cyclone research and decision-support project.
- Python backend, model-training pipeline, API, map dashboard, and deployment
  configuration are present in the repository.
- Distinguish local capabilities from externally verified services.

## Slide 2 — Data and model pipeline

- Source adapters preserve provenance and checksums.
- Feature, dataset, scaler, checkpoint, bundle, and inference contracts have
  local automated coverage.
- Model families: LSTM, Seq2Seq LSTM, Attention LSTM, Transformer, and motion
  baselines.
- Forecast horizons: +6h, +12h, +24h, +48h, and +72h where supported.

## Slide 3 — What has been verified locally

- Python 3.11 test suite exercises ingestion, data contracts, model training
  smoke paths, bundle validation, inference, API, storage, cache, worker, and
  operational helper behavior.
- Frontend tests cover API/auth states and edge functions; TypeScript check
  and production build are available.
- Synthetic fixtures validate software behavior only; they are not forecast
  skill evidence.

## Slide 4 — Dashboard and API demonstration

- Show map layers, location weather, storm track, forecast timeline, analysis,
  and explicit demo/offline states.
- Show API documentation, health/readiness distinction, and response
  provenance.
- Demonstrate API failures as unavailable states, not as evidence that no
  storm exists.

## Slide 5 — Current operating limits

- The published Pages deployment has no live storm feed and does not deliver
  real alerts.
- A promoted real-data model bundle and independent real-storm skill report
  are not present in the reviewed checkout.
- PostGIS integration requires `POSTGIS_TEST_URL`; production Docker, Redis,
  worker, monitoring, and rollback require target-environment evidence.
- NCHMF weather/API availability can differ by deployment and provider access.

## Slide 6 — Acceptance gates and next actions

- Train on approved IBTrACS data and compare models on storm-held-out data.
- Evaluate +6h/+12h/+24h/+48h/+72h track error in kilometres against persistence
  and matched NWP baselines.
- Calibrate uncertainty on held-out validation and report independent test
  coverage.
- Verify backend HTTPS, database migrations, model loading, worker, metrics,
  alert recipients, backups, rollback, and operator UAT in the target
  environment.
- Freeze a clean source commit/tag and match it to deployed assets.

## Handover references

- [Model card](model-card.md)
- [User guide](user-guide.md)
- [Deployment gates](deployment.md)
- [Post-season evaluation report template](post-season-report.md)
- [Project Definition of Done](acceptance/project-dod.md)
- [Current readiness review](../reports/handover-readiness-2026-09-23.md)

No sample metric should be presented as real-storm performance unless its
dataset, split, sample count, model hash, and reproducible evaluation are
provided. This is not an official warning system.
