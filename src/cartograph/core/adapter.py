"""ModelAdapter protocol: the only Protocol surface in Phase 1a (HYBRID-S decision)."""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Protocol, runtime_checkable


class Capability(StrEnum):
    """What a backing model permits a functor to compute.

    Functors must declare required capabilities and fail loud when an adapter
    cannot satisfy them. This avoids silent fallback to mock data.
    """

    HIDDEN_STATES = "hidden_states"
    ATTENTION = "attention"
    SAE_FEATURES = "sae_features"
    VELOCITY_FIELD = "velocity_field"
    SSM_STATES = "ssm_states"
    LOSS_LANDSCAPE = "loss_landscape"


@runtime_checkable
class ModelAdapter(Protocol):
    """Minimum contract every backing model must satisfy.

    Phase 1a keeps this surface intentionally narrow. Adding methods is a
    breaking change; instead, gate new functors on new `Capability` members.
    """

    name: str
    capabilities: frozenset[Capability]

    def forward(self, inputs: Any) -> Any:
        """Run a forward pass and return whatever the backing model returns."""

    def hidden_states(self, inputs: Any, layer: int) -> Any:
        """Return hidden states at `layer`. Required for Phi via SAE features."""

    def attention(self, inputs: Any) -> Any:
        """Return attention tensors. Required for T via rollout territories."""

    def requires(self, *needed: Capability) -> None:
        """Raise `MissingCapabilityError` if any `needed` capability is absent."""


class MissingCapabilityError(RuntimeError):
    """Raised when a functor requests a capability an adapter does not have."""

    def __init__(self, adapter_name: str, missing: frozenset[Capability]) -> None:
        joined = ", ".join(sorted(c.value for c in missing))
        super().__init__(f"adapter '{adapter_name}' is missing required capabilities: {joined}")
        self.adapter_name = adapter_name
        self.missing = missing
