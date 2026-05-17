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
| W2 | SAE is now widely public (Llama Scope arXiv:2410.20526); planned `adapters/llama_scope.py`. Φ's circuit-decomposition layer (directed feature→feature pathways, Transformer Circuits line) is a Phase 1b deliverable; without it Phase 1a Φ is a co-activation graph only and not the full Guattarian construct. |
| W3 | T construct-validity gate: at least one Guattari-semantic-exclusive prediction must be identified before Phase 1b release. Encoded as `tests/integration/test_t_semantic_exclusivity.py` (added in Phase 1b) asserting one observation reproducible by T but not by plain attention rollout. |
| W4 | Four-axis overrun: structural fix via 1a/1b stage split |
| W5 | Phase 1→2 bridge: seam + H3 GO/NO-GO |
| W6 | SOTA churn: H1 quarterly + ModelAdapter contains swap cost |

## Honest scope

5-6 months on one maintainer is realistic; 3-4 months is optimistic. The
README's `## Non-claims` section explicitly disclaims "complete" and
"permanent" framing; ADRs and release notes follow the same vocabulary.

## Consequences

- New first-party functors require **only** a new `Capability` member +
  concrete class. No Protocol breaking change.
- Third-party adapters can ship today without an `entry_points` opening,
  via `register_adapter("...")` decorator import.
- Phase 2 work can begin in a sibling repo without renaming this one if H3 is
  GO; the bridge seam keeps the import surface stable either way.

## Residual issues (10) — carry-over from architecture decision

Each item names a forthcoming ADR (or in-place commit) and the trigger that
forces the decision. References elsewhere in the repo (`residual #N`) point
to the numbers in this list.

1. **Llama Scope SAE adapter adoption** (`adapters/llama_scope.py`). Trigger:
   Phase 1a mid-point review; decide whether to bundle He et al. 2024
   (arXiv:2410.20526) or keep SAE-Lens as the sole upstream.
2. **paper/ co-located vs separate repository**. Trigger: start of Phase 1c;
   decide whether `paper/main.tex` stays in this repo or moves to
   `cartograph-paper`.
3. **`plugins/` monorepo opening via `entry_points`**. Trigger: end of Phase 1b
   *only if* ≥2 external adapters have been requested; otherwise stay with the
   `register_adapter` decorator.
4. **Visualizer Protocol-isation**. Trigger: end of Phase 1b once all four
   functors' artifact shapes are frozen.
5. **Phase 2 CFlow: same repo vs sibling repo (H3)**. Trigger: end of Phase
   1c; recorded as `docs/decisions/ADR-XXXX-cflow-bridge.md`. Must include the
   mathematical-differentiation-vs-Stochastic-Interpolants section (see
   `bridge/differentiable.py` docstring).
6. **Stewards transition trigger conditions**. Trigger: any of the three
   `GOVERNANCE.md` triggers fires; ADR records the slate.
7. **Construct-validity peer slate of 3**. Trigger: within month 1 of
   Phase 1a; outreach log lives in `docs/peer_reviews/README.md`.
8. **arXiv preprint timing (mid Phase 1c vs post-α)**. Trigger: Phase 1c
   start; the call point sits between "preprint during 1c so reviewers see
   it before α tag" and "post-α so we can cite the published tag".
9. **T Guattari-semantic-exclusive prediction (W3 gate)**. Trigger: before
   `v0.2.0` release; at least one prediction must be identified that is
   not reproducible by plain attention rollout. The Phase 1b release gate
   adds `tests/integration/test_t_semantic_exclusivity.py` asserting one
   such observation, **and a gate #7 must be added to
   `scripts/verify_release.py` at Phase 1b kickoff** so the test cannot be
   silently skipped.
10. **`experiments/_wip/cartograph-phaseN-<slug>/` failure-museum operating
    rule**. Already documented in `experiments/_wip/README.md`; tracked here
    so the rule has a referent inside ADR-0001.

## Default base model (Phase 1a)

`HFTransformerAdapter` defaults to `gpt2`, not the originally-considered
Llama-3-8B. Reason: GPT-2 small downloads in seconds, runs CI without GPU,
and ships with SAE-Lens releases (`gpt2-small-res-jb`). Llama-3-8B is gated
on HF and 16 GB+, which would break the `integration.yml` budget. Migration
to Llama-3-8B (or Llama Scope) is the H1 quarterly call.
