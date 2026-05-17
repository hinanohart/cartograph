"""T (Existential Territories): attention-rollout territory graph + SSM comparison.

Phase 1a is a stub. Phase 1b will implement Abnar & Zuidema 2020 attention
rollout reframed as territorial closure, with a parallel Mamba SSM head (Ali
et al. ACL 2025 'Hidden Attention of Mamba') to satisfy the W3 construct-
validity gate: T must yield at least one prediction that is *not* reducible
to plain attention visualisation.
"""

from __future__ import annotations

from typing import Any

from cartograph.core.adapter import Capability, ModelAdapter
from cartograph.core.report import FunctorResult


class TerritoriesFunctor:
    name = "T"
    required: frozenset[Capability] = frozenset({Capability.ATTENTION})

    def __init__(self, rollout_alpha: float = 0.5) -> None:
        if not 0.0 <= rollout_alpha <= 1.0:
            raise ValueError("rollout_alpha must lie in [0, 1]")
        self.rollout_alpha = rollout_alpha

    def compute(self, adapter: ModelAdapter, inputs: Any) -> FunctorResult:
        adapter.requires(*self.required)
        raise NotImplementedError(
            "TerritoriesFunctor lands in Phase 1b after construct-validity gate "
            "(W3 mitigation). See docs/decisions/ADR-0003-t-functor.md (forthcoming)."
        )

    def compute_differentiable(self, adapter: ModelAdapter, inputs: Any) -> Any | None:
        return None
