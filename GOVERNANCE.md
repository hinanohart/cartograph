# Governance

## Current model: BDFL (Phase 1a–1b)

`hinanohart` holds final decision authority for Phase 1a and 1b. Decisions
that change the four-functor public API, the adapter Protocol, or the release
gate are recorded as ADRs under `docs/decisions/`.

## Transition: BDFL → Stewards (target: Phase 1c)

The project transitions to a Stewards model when **any one** of the
following triggers fires:

1. ≥3 external code contributors with merged non-trivial PRs
2. ≥5 institutional citations of the v0.2.0 alpha
3. A successful Phase 2 GO/NO-GO decision (H3) producing a sibling repo

Stewards (target 3–5 people) will cover: code, peer-review coordination,
philosophy/construct-validity, and release management.

## Decision process

- **Day-to-day** (typo fixes, dep bumps, new adapters): direct merge after CI.
- **API surface changes** (Protocol additions, capability changes, functor
  semantics): require an ADR and 7-day comment window.
- **Release gate failures** (`scripts/verify_release.py` exit nonzero):
  block the release; never bypass.

## Code of conduct

Apache-2.0 covers the license. A `CODE_OF_CONDUCT.md` (Contributor Covenant
v2.1) will land before the first external PR is solicited.
