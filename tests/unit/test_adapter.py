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
