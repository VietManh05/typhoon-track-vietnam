# Findings and decisions

## Requirements
- User requests planning-with-files and implementation of the entire existing roadmap, explicitly including API and dashboard.

## Repository findings
- README describes phases 0–1, but source contains ingestion, features, datasets, LSTM/attention/transformer models, uncertainty, evaluation and a trainer.
- API exposes only health/version; CLI prints placeholders.
- Dataset chooses default feature columns before constructing derived features; time gaps and year-boundary storm splits need verification.
- Trainer saves checkpoint before appending epoch history/scheduler step and does not restore full scheduler/early-stop state.
- Entire project is untracked. Avoid reset/cleanup or overwriting checkpoints.
- No project AGENTS.md found outside the unrelated nested open-code-review repository.
- No prior project planning files or named plan were found by the installed resolver.

## Resources
- ROADMAP_WBS_Typhoon_Vietnam_Chi_Tiet.md is the functional scope.
- docs/architecture.md and CONTRIBUTING.md define provenance, disclaimer, tests and Python 3.11 conventions.

## Issues
- Sandbox execution helper cannot initialize; escalated commands are currently required.

- Baseline pytest failed collection: torch and FastAPI missing; dependency install running. apply_patch update failed because sandbox helper cannot initialize; use approved shell writes.

## Replanning inspection
- User requests detailed small-task planning; pause feature implementation for this turn.
- Installed dependencies verified: torch 2.14.0, FastAPI 0.141.1, SQLAlchemy 2.0.54, Redis 5.3.1. Tests have not been rerun after install.
- API/inference/operations were written in previous turn but are untested. training.pipeline is referenced and missing. Dashboard is not implemented.
- Redis currently writes but does not read; durable SQL cache is implemented but untested. create_all is not an Alembic/PostGIS migration.
- Source roadmap has overlapping high-level milestones and a detailed WBS. Preserve original file and link every source checkbox to the new plan.
