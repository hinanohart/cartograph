# Changelog

All notable changes to this project will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0a0] — 2026-05-17

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
