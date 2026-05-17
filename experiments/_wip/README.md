# experiments/_wip/

Working-in-progress experiments. Each subdirectory is one experiment that
either failed or has not yet been promoted to a tested code path.

## Rules

- One subdirectory per experiment, named `cartograph-phaseN-<short-slug>/`.
- Each subdirectory has its own `README.md` saying **what was tried**,
  **what happened**, and **what would have to be true** for the idea to
  return to the main tree.
- Heavy artefacts (`data/`, `checkpoints/`) are gitignored; only the
  reproducible recipe lives in git.
- Code here is **not** linted, type-checked, or covered by the release gate.
  It is preserved for institutional memory rather than for reuse.

## Why this directory exists

Deleting failed experiments destroys the rationale for current design
choices. Keeping a structured failure museum prevents the same blind alley
from being re-explored every six months.
