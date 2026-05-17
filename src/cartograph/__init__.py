"""Cartograph: diagnose foundation models on Guattari's four schizoanalytic functors.

Phase 1a (alpha-pre) exposes Phi (Machinic Phyla) and U (Universes of Reference)
as the two production-ready functors. F (Flows) and T (Existential Territories)
are stubbed and become first-class in Phase 1b.
"""

from cartograph.core.adapter import Capability, ModelAdapter
from cartograph.core.registry import REGISTRY, register_adapter
from cartograph.core.report import CartographicProfile, FunctorResult

__version__ = "0.1.0a0"
__all__ = [
    "REGISTRY",
    "Capability",
    "CartographicProfile",
    "FunctorResult",
    "ModelAdapter",
    "__version__",
    "register_adapter",
]
