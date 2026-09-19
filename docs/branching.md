# Branch workflow

- Protected integration branches: `main` and `develop`.
- Start feature work from `develop` only when a concrete task is assigned.
- Naming: `feature/<task-id>-<short-slug>` using lowercase ASCII and hyphens, for example `feature/t18-001-typhoons-schema`.
- One feature branch should represent one task or one explicitly documented task slice.
- Merge through review into `develop`; promotion to `main` is a separate release decision.
- Do not create empty speculative branches, automatically checkout a dirty worktree, or push without an explicit remote instruction.
