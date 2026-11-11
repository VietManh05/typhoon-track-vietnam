# Model bundle contract

A promoted bundle is a directory containing `manifest.json`, `weights.pt`, `scaler.json`, and `split-manifest.json`.

The current bundle schema is **2**. Regression targets and outputs are unscaled
WGS84 degrees; the persisted scaler transforms inputs only. Schema 1 bundles
are rejected because the previous dataset path could scale regression targets.
Retrain and reevaluate those artifacts; changing the manifest version alone is
not a migration. Export selects `best.pt`, while `last.pt` remains available for
training resume. Cache identity includes the manifest so retraining under the
same display version cannot serve a previous bundle's predictions.

For learned-model evaluation, use `backtest_bundle(load_bundle(path), frame)`.
The lower-level backtest functions require the fitted scaler for learned models;
classical persistence/CLIPER baselines continue to consume raw features.

## Validation and trust boundary

`load_bundle` validates a strict manifest schema, an allowlisted model constructor, the canonical feature vocabulary/order, dimensions, horizon/calibration coverage, and SHA-256 for every payload **before deserializing weights**. PyTorch weights are loaded with `weights_only=True`; scaler state is strict JSON rather than joblib/pickle.

Internal checksums detect corruption but are not a cryptographic signature or external trust anchor. Production promotion must distribute/pin the reviewed `manifest.json` digest through deployment configuration or a signed registry. A checksum shipped only beside an attacker-controlled manifest does not establish provenance.

## Required metadata

- bundle schema and model version;
- dataset version, digest, and synthetic-data flag;
- exact model type and constructor parameters;
- input length and time-step hours;
- ordered feature names and feature-schema digest;
- output horizons and intensity labels;
- scaler train-only means/scales/fill values;
- split-manifest checksum;
- validation radii and non-coverage uncertainty wording;
- checksum for every bundle payload.

## Serving rules

Serving builds features over all supplied chronological fixes, selects the final input window only after feature derivation, applies the persisted scaler without fitting, and maps requested hours by explicit horizon value. Missing, corrupt, incompatible or non-finite artifacts fail closed; the service must not silently fall back when an artifact was explicitly requested.
