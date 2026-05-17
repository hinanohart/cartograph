# ADR-0001 — Adopt HYBRID-S architecture

- Status: accepted
- Date: 2026-05-17
- Deciders: hinanohart (BDFL, transitions to Stewards per GOVERNANCE.md)

## Context

Cartograph is a research-grade OSS that diagnoses foundation models on
Guattari's four schizoanalytic functors (F / Φ / T / U). Three architectural
candidates were explored in parallel:

- **Lean**: single package, 4 submodules, ~11 deps, 3-4 month optimistic plan
- **Modular**: Protocol-per-functor with `entry_points` plugins; ~3 GB extras
- **Skeptic**: identifies six structural weaknesses (W1-W6) and proposes a
  three-stage release plan to retire them

An independent critic synthesised **HYBRID-S**: Skeptic's stage split + the
Modular `ModelAdapter` Protocol *only* + Lean's dependency discipline. Both
unconditional Lean and full Modular were rejected as either underestimating
construct-validity risk or paying abstraction tax for nonexistent plugins.

## Decision

1. **Single package** `cartograph` with submodules `core/ functors/ adapters/
   bridge/ viz/`.
2. **ModelAdapter is the only Protocol** in Phase 1a. Functors and the
   Visualizer stay concrete classes; the Visualizer Protocol question reopens
   at end of Phase 1b.
3. **Stage the release**:
   - Phase 1a (M1-2): Φ + U + adapter, `v0.1.0a0`, two internal peers
   - Phase 1b (M3-5): F + T integrated, `v0.2.0`, ≥3 external peers
   - Phase 1c (M6): docs/examples/arXiv preprint, `v0.3.0`
4. **Phase 2 bridge seam exists from Phase 1a** as
   `bridge/differentiable.py`. All `compute_differentiable` methods return
   `None` until H3 GO/NO-GO at end of Phase 1c.
5. **Five GitHub Actions workflows**: `ci`, `integration`, `reproduce` (nightly
   paper-figure regeneration), `docs`, `release` (driven by
   `scripts/verify_release.py` six-item checklist).
6. **Three human judgment points** become ADRs:
   - H1: base-model bump (quarterly)
   - H2: construct-validity peer review (each minor release)
   - H3: Phase 2 CFlow GO/NO-GO (end of Phase 1c)

## Weakness mitigations (from Skeptic round)

| W | Mitigation |
|---|---|
| W1 | PH scale: Phase 1b restricted to landmark/witness complexes |
| W2 | SAE is now widely public (Llama Scope arXiv:2410.20526); planned `adapters/llama_scope.py` |
| W3 | T construct-validity gate: at least one Guattari-semantic-exclusive prediction must be identified before Phase 1b release |
| W4 | Four-axis overrun: structural fix via 1a/1b stage split |
| W5 | Phase 1→2 bridge: seam + H3 GO/NO-GO |
| W6 | SOTA churn: H1 quarterly + ModelAdapter contains swap cost |

## Honest scope

5-6 months on one maintainer is realistic; 3-4 months is optimistic. The
README does not claim "complete" or "permanent" — per
[feedback_no-permanent-claim](../../README.md#non-claims), avoid that vocabulary.

## Consequences

- New first-party functors require **only** a new `Capability` member +
  concrete class. No Protocol breaking change.
- Third-party adapters can ship today without an `entry_points` opening,
  via `register_adapter("...")` decorator import.
- Phase 2 work can begin in a sibling repo without renaming this one if H3 is
  GO; the bridge seam keeps the import surface stable either way.
