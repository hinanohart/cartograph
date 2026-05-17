"""F (Flows): persistent homology of the velocity field.

Phase 1a is a stub — `compute` raises `NotImplementedError`. Implementation
arrives in Phase 1b using landmark/witness complexes (W1 mitigation in
ADR-0001) via giotto-tda or ripser.

Why stub now: declaring the type surface in 1a keeps the four-functor public
API stable from day one; users who try to call F get a directed error message
instead of silent absence.

References (Phase 1b implementation basis):
- Lipman et al. 2022 (Flow Matching velocity-field formulation)
- giotto-tda / ripser (production PH backends)
- Carriere et al. 2020 "A General Neural Network Architecture for Persistence
  Diagrams and Graph Classification" (arXiv:2010.08356) — differentiable PH,
  the bridge to Phase 2 CFlow's `compute_differentiable` path.
"""

from __future__ import annotations

from typing import Any

from cartograph.core.adapter import Capability, ModelAdapter
from cartograph.core.report import FunctorResult


class FlowsFunctor:
    name = "F"
    required: frozenset[Capability] = frozenset({Capability.VELOCITY_FIELD})

    def __init__(self, max_dim: int = 2, n_landmarks: int = 256) -> None:
        if max_dim < 0:
            raise ValueError("max_dim must be non-negative")
        if n_landmarks < 16:
            raise ValueError("n_landmarks must be >=16 for stable homology")
        self.max_dim = max_dim
        self.n_landmarks = n_landmarks

    def compute(self, adapter: ModelAdapter, inputs: Any) -> FunctorResult:
        adapter.requires(*self.required)
        raise NotImplementedError(
            "FlowsFunctor lands in Phase 1b (landmark/witness PH). "
            "Track progress: docs/decisions/ADR-0002-f-functor.md (forthcoming)."
        )

    def compute_differentiable(self, adapter: ModelAdapter, inputs: Any) -> Any | None:
        return None
