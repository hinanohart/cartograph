# Changelog

All notable changes to this project will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0a0] — 2026-05-17

### Fixed (second-pass audit)
- `HFTransformerAdapter` now declares `SAE_FEATURES` only when `sae_release`
  is provided, so `adapter.requires(SAE_FEATURES)` fails loud as the Protocol
  contract promises (previously it silently passed and the call dove into a
  bare `RuntimeError` inside `sae_encode`).
- `UniversesFunctor._hypervolume` now delegates to `pymoo.indicators.hv.HV`;
  the hand-rolled box-sum double-counted overlapping orthants (true 3.0,
  returned 4.0 for the {(0,1),(1,0)} L-frontier).
- `UniversesFunctor.compute` rejects empty inputs (prevents downstream viz
  IndexError on a zero-row frontier).
- `PhiPhylaFunctor` rejects NaN/Inf features and non-finite thresholds
  (symmetric to the U guard; closes a silent-zero-graph foot-gun).
- `gate_capability_matrix` matches `` `adapter-name` `` as a code token
  rather than a bare substring; populates the registry via
  `register_builtin_adapters()`.
- `gate_changelog` uses a bracket-anchored regex; `v0.1.0` no longer falsely
  matches a `## [0.1.0a0]` header.
- `make_paper_figures.py` strips the matplotlib `Software` PNG metadata
  chunk, so byte-identical sha256 survives matplotlib patch upgrades.
- Phi reproducibility subprocess test surfaces the child stderr/stdout on
  failure instead of a bare `CalledProcessError`.
- `pyproject.toml`: `transformer-lens` moved to the new `interp` extra so
  `pip install cartograph` stays lean (it is required only by Phase 1b
  adapters that do not yet exist).

### Added
- HYBRID-S architecture (ADR-0001).
- `ModelAdapter` Protocol + capability-frozenset gating.
- `PhiPhylaFunctor` (SAE co-activation Jaccard graph) with batch-relative
  quantile **or** absolute `coactivation_threshold` for cross-paper
  comparability.
- `UniversesFunctor` (Pareto frontier over user-supplied objectives) with
  NaN/Inf rejection.
- `FlowsFunctor` and `TerritoriesFunctor` typed stubs (Phase 1b).
- `HFTransformerAdapter` (GPT-2 default) + `MambaAdapter` stub.
- Phase 2 differentiability seam (`bridge/differentiable.py`) with the
  four future-symbol list and SI-differentiation blocker.
- Minimal matplotlib renderer for cartographic profiles (Agg-safe).
- Five GitHub Actions workflows: ci, integration, reproduce, docs, release.
  `release.yml` regenerates paper figures before running the six-item gate.
- `scripts/verify_release.py` six-item release gate (unified signatures,
  no silent skip of byte-identical figure check).
- `register_builtin_adapters()` explicit registration entry point.
- Reproducibility test that runs in a subprocess and pins a golden Phi
  adjacency SHA-256.
- mkdocs-material documentation skeleton.

### Notes
- Phase 1a release. Construct-validity peer review is the gating concern;
  see `docs/peer_reviews/`. No claim of completeness or permanence.

[0.1.0a0]: https://github.com/hinanohart/cartograph/releases/tag/v0.1.0a0
