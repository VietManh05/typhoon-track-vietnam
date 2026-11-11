# Typhoon VN model card

Version: 0.1.0-phase7-local

Status: research and local demonstration. This software is decision support,
not an official warning system. No model in this checkout is approved for
operational forecasts.

## Intended use

The project explores tropical-cyclone track forecasting for Vietnam and the
South China Sea. It provides data ingestion, feature construction, training,
evaluation, model bundles, inference APIs, a map dashboard, and operational
prototypes. Forecasts are not a substitute for NCHMF or other competent
authorities.

## Model families

The code provides `LSTMTrackForecaster`, `Seq2SeqLSTMTrackForecaster`,
`AttentionLSTMTrackForecaster`, and `TransformerTrackForecaster`, with
`PersistenceForecaster` and a damped-persistence `CLIPERForecaster` as
baselines. The latter is explicitly a proxy and does not claim published
CLIPER coefficients or forecast skill. The default experiment configuration
is `configs/phase3_lstm.yaml`; the one-epoch real-data smoke configuration is
`configs/ibtracs_smoke.yaml`.

## Data and training status

Training and bundle export paths support provenance, storm/year splits,
train-only feature scaling, checkpoint resume, and multi-horizon forecasts at
+6, +12, +24, +48, and +72 hours. Synthetic fixtures are used for deterministic
contract and integration tests. They do not measure real-storm skill.

No promoted production bundle is present under `checkpoints/promoted/`. The
IBTrACS candidate workflow in [retraining](retraining.md) trains on completed
seasons and preserves source checksums, but its output is not approved forecast
evidence until independent evaluation is recorded.
The available evaluation files identify their dataset as
`synthetic-functional-v1` and their split as contract-only; their metrics must
not be interpreted as real-world forecast performance. Real-data training,
independent storm-held-out evaluation, comparison with operational NWP, and
uncertainty calibration remain pending.

## Outputs and limitations

Track outputs are geographic latitude/longitude forecasts. The interface can
also carry intensity classes and an uncertainty radius. A radius derived from
validation radial error is not calibrated coverage unless independent held-out
coverage has been measured and documented. Baseline, synthetic, missing-feed,
and unavailable-provider states must remain distinguishable from operational
model output.

Known limitations include JMA live-feed display without a promoted model or
NCHMF alert delivery on the published Pages site, lack of an approved real-data model bundle,
and unverified production database, worker, alert-delivery, monitoring, and
rollback paths. See [deployment gates](deployment.md),
[post-season evaluation requirements](post-season-report.md), and the
[handover readiness review](../reports/handover-readiness-2026-09-23.md).

## Evaluation required before promotion

Before operational consideration, record the approved dataset sources and
checksums; storm/year train, validation, and final-test splits; bundle and
code hashes; sample counts; track error in kilometres at each forecast
horizon; persistence and NWP baselines; intensity metrics; uncertainty
coverage/calibration; failure cases; and independent reproduction. Promotion
must follow the documented release policy and operator review.

## Safety

This system is not an official warning system. Do not use synthetic results,
baseline output, or an illustrative uncertainty radius to make safety-critical
decisions. Consult official bulletins and competent authorities.
