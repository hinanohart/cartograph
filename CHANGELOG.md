# Changelog

All notable changes to this project will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0a0] — 2026-05-17

### Added
- HYBRID-S architecture (ADR-0001).
- `ModelAdapter` Protocol + capability-frozenset gating.
- `PhiPhylaFunctor` (SAE co-activation Jaccard graph).
- `UniversesFunctor` (Pareto frontier over user-supplied objectives).
- `FlowsFunctor` and `TerritoriesFunctor` typed stubs (Phase 1b).
- `HFTransformerAdapter` (GPT-2 default) + `MambaAdapter` stub.
- Phase 2 differentiability seam (`bridge/differentiable.py`).
- Minimal matplotlib renderer for cartographic profiles.
- Five GitHub Actions workflows: ci, integration, reproduce, docs, release.
- `scripts/verify_release.py` six-item release gate.
- mkdocs-material documentation skeleton.

### Notes
- Phase 1a release. Construct-validity peer review is the gating concern;
  see `docs/peer_reviews/`. No claim of completeness or permanence.

[0.1.0a0]: https://github.com/hinanohart/cartograph/releases/tag/v0.1.0a0
