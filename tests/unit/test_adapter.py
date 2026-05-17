"""Adapter Protocol + capability gating."""

from __future__ import annotations

import pytest

from cartograph.core.adapter import (
    Capability,
    MissingCapabilityError,
    ModelAdapter,
)


class _DummyAdapter:
    name = "dummy"
    capabilities = frozenset({Capability.HIDDEN_STATES})

    def forward(self, inputs):
        return inputs

    def hidden_states(self, inputs, layer):
        return [layer, inputs]

    def attention(self, inputs):
        raise MissingCapabilityError(self.name, frozenset({Capability.ATTENTION}))

    def requires(self, *needed):
        missing = frozenset(needed) - self.capabilities
        if missing:
            raise MissingCapabilityError(self.name, missing)


def test_dummy_conforms_to_protocol() -> None:
    assert isinstance(_DummyAdapter(), ModelAdapter)


def test_requires_passes_when_capabilities_present() -> None:
    _DummyAdapter().requires(Capability.HIDDEN_STATES)


def test_requires_fails_loud_on_missing() -> None:
    with pytest.raises(MissingCapabilityError) as exc:
        _DummyAdapter().requires(Capability.ATTENTION)
    assert "attention" in str(exc.value)


def test_hf_transformer_conforms_to_protocol() -> None:
    from cartograph.adapters import HFTransformerAdapter

    assert isinstance(HFTransformerAdapter(), ModelAdapter)


def test_hf_transformer_sae_capability_gated_on_release() -> None:
    """Without sae_release, the adapter must NOT advertise SAE_FEATURES.

    Otherwise `requires(SAE_FEATURES)` PASSes and the call dives into
    `sae_encode` which raises a plain RuntimeError instead of the typed
    MissingCapabilityError the Protocol contract promises.
    """

    from cartograph.adapters import HFTransformerAdapter

    bare = HFTransformerAdapter()
    assert Capability.SAE_FEATURES not in bare.capabilities
    with pytest.raises(MissingCapabilityError):
        bare.requires(Capability.SAE_FEATURES)

    armed = HFTransformerAdapter(sae_release="dummy")
    assert Capability.SAE_FEATURES in armed.capabilities
    armed.requires(Capability.SAE_FEATURES)


def test_hf_transformer_capabilities_is_frozenset() -> None:
    """Protocol type hint is a frozenset; runtime must agree."""

    from cartograph.adapters import HFTransformerAdapter

    assert isinstance(HFTransformerAdapter().capabilities, frozenset)
