"""Reproducibility: byte-identical artefacts under fixed seed.

Phase 1a only locks Phi adjacency. Phase 1b extends to all four functors
and is wired into the `reproduce.yml` workflow (paper-figure regeneration).
"""

from __future__ import annotations

import hashlib

import numpy as np
import pytest

from cartograph.core.adapter import Capability, MissingCapabilityError
from cartograph.functors.phi_phyla import PhiPhylaFunctor


class _SeededFakeAdapter:
    name = "seeded-fake"
    capabilities = frozenset({Capability.HIDDEN_STATES, Capability.SAE_FEATURES})

    def __init__(self, seed: int) -> None:
        self._seed = seed

    def forward(self, inputs):
        return inputs

    def hidden_states(self, inputs, layer):
        return inputs

    def attention(self, inputs):
        raise MissingCapabilityError(self.name, frozenset({Capability.ATTENTION}))

    def sae_encode(self, hidden, layer):
        rng = np.random.default_rng(self._seed)
        return rng.random((128, 16))

    def requires(self, *needed):
        missing = frozenset(needed) - self.capabilities
        if missing:
            raise MissingCapabilityError(self.name, missing)


@pytest.mark.reproducibility
def test_phi_adjacency_byte_identical_under_seed() -> None:
    functor = PhiPhylaFunctor(layer=0, coactivation_quantile=0.95)
    a = functor.compute(_SeededFakeAdapter(seed=42), inputs="x").artifacts["adjacency"]
    b = functor.compute(_SeededFakeAdapter(seed=42), inputs="x").artifacts["adjacency"]
    assert hashlib.sha256(a.tobytes()).hexdigest() == hashlib.sha256(b.tobytes()).hexdigest()
