"""Phi functor shape + edge-case tests (no model load)."""

from __future__ import annotations

import numpy as np
import pytest

from cartograph.core.adapter import Capability, MissingCapabilityError
from cartograph.functors.phi_phyla import PhiPhylaFunctor


class _FakeAdapter:
    name = "fake"
    capabilities = frozenset({Capability.HIDDEN_STATES, Capability.SAE_FEATURES})

    def __init__(self, features: np.ndarray) -> None:
        self._features = features

    def forward(self, inputs):
        return inputs

    def hidden_states(self, inputs, layer):
        return inputs

    def attention(self, inputs):
        raise MissingCapabilityError(self.name, frozenset({Capability.ATTENTION}))

    def sae_encode(self, hidden, layer):
        return self._features

    def requires(self, *needed):
        missing = frozenset(needed) - self.capabilities
        if missing:
            raise MissingCapabilityError(self.name, missing)


def test_phi_quantile_validation() -> None:
    with pytest.raises(ValueError):
        PhiPhylaFunctor(layer=0, coactivation_quantile=0.0)


def test_phi_metrics_shape() -> None:
    rng = np.random.default_rng(0)
    features = rng.random((64, 8))
    functor = PhiPhylaFunctor(layer=0, coactivation_quantile=0.9)
    result = functor.compute(_FakeAdapter(features), inputs="x")
    assert result.functor == "Phi"
    assert result.metrics["n_features"] == 8
    assert result.artifacts["adjacency"].shape == (8, 8)


def test_phi_adjacency_invariants() -> None:
    """Jaccard adjacency must be symmetric, zero-diagonal, [0,1]-bounded.

    Defends against silent regressions in `_coactivation_adjacency` that
    only-shape tests cannot catch (e.g. dropping `fill_diagonal`, swapping
    `co.T` for `co`, multiplying by `denom` instead of dividing).
    """

    rng = np.random.default_rng(1)
    features = rng.random((64, 8))
    adj = (
        PhiPhylaFunctor(layer=0, coactivation_quantile=0.9)
        .compute(_FakeAdapter(features), inputs="x")
        .artifacts["adjacency"]
    )
    assert (adj.diagonal() == 0).all()
    assert np.allclose(adj, adj.T)
    assert ((adj >= 0) & (adj <= 1)).all()


def test_phi_rejects_nan_features() -> None:
    features = np.zeros((4, 3))
    features[0, 0] = np.nan
    with pytest.raises(ValueError, match="NaN or Inf"):
        PhiPhylaFunctor(layer=0).compute(_FakeAdapter(features), inputs="x")


def test_phi_rejects_nonfinite_threshold() -> None:
    with pytest.raises(ValueError, match="finite"):
        PhiPhylaFunctor(layer=0, coactivation_threshold=float("nan"))


def test_phi_differentiable_returns_none_in_phase_1a() -> None:
    functor = PhiPhylaFunctor(layer=0)
    assert functor.compute_differentiable(_FakeAdapter(np.zeros((4, 2))), inputs="x") is None
