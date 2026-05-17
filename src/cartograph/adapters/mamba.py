"""Mamba SSM adapter stub. Full implementation lands with T functor (Phase 1b).

Kept as a registered stub so users discover the planned surface via
`cartograph list-adapters`.
"""

from __future__ import annotations

from typing import Any

from cartograph.core.adapter import Capability, MissingCapabilityError
from cartograph.core.registry import register_adapter


@register_adapter("mamba")
class MambaAdapter:
    name = "mamba"
    capabilities: frozenset[Capability] = frozenset(
        {Capability.HIDDEN_STATES, Capability.SSM_STATES}
    )

    def __init__(self, model_id: str = "state-spaces/mamba-130m-hf") -> None:
        self.model_id = model_id

    def requires(self, *needed: Capability) -> None:
        missing = frozenset(needed) - self.capabilities
        if missing:
            raise MissingCapabilityError(self.name, missing)

    def forward(self, inputs: Any) -> Any:
        raise NotImplementedError("MambaAdapter is a Phase 1b stub")

    def hidden_states(self, inputs: Any, layer: int) -> Any:
        raise NotImplementedError("MambaAdapter is a Phase 1b stub")

    def attention(self, inputs: Any) -> Any:
        # By design: Mamba has no attention. Functors must respect capabilities.
        raise MissingCapabilityError(self.name, frozenset({Capability.ATTENTION}))
