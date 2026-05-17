"""Four functors. Phase 1a: Phi + U are implemented; F + T are stubs.

Each functor exposes:
- `compute(adapter, inputs) -> FunctorResult` (eager)
- `compute_differentiable(adapter, inputs) -> torch.Tensor | None` (Phase 2 seam)
"""

from cartograph.functors.f_flows import FlowsFunctor
from cartograph.functors.phi_phyla import PhiPhylaFunctor
from cartograph.functors.t_territories import TerritoriesFunctor
from cartograph.functors.u_universes import UniversesFunctor

__all__ = [
    "FlowsFunctor",
    "PhiPhylaFunctor",
    "TerritoriesFunctor",
    "UniversesFunctor",
]
