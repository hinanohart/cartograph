"""U functor: Pareto frontier basic correctness."""

from __future__ import annotations

import pytest

from cartograph.core.adapter import Capability, MissingCapabilityError
from cartograph.functors.u_universes import UniversesFunctor


class _ScalarAdapter:
    name = "scalar"
    capabilities = frozenset({Capability.LOSS_LANDSCAPE})

    def forward(self, inputs):
        return inputs

    def hidden_states(self, inputs, layer):
        raise MissingCapabilityError(self.name, frozenset({Capability.HIDDEN_STATES}))

    def attention(self, inputs):
        raise MissingCapabilityError(self.name, frozenset({Capability.ATTENTION}))

    def requires(self, *needed):
        missing = frozenset(needed) - self.capabilities
        if missing:
            raise MissingCapabilityError(self.name, missing)


def test_u_rejects_single_objective() -> None:
    with pytest.raises(ValueError):
        UniversesFunctor(objectives={"only": lambda out: 0.0})


def test_u_finds_pareto_front_two_objective() -> None:
    objectives = {"o1": lambda x: float(x[0]), "o2": lambda x: float(x[1])}
    inputs = [(1.0, 5.0), (2.0, 4.0), (3.0, 3.0), (4.0, 4.5), (5.0, 1.0)]
    result = UniversesFunctor(objectives).compute(_ScalarAdapter(), inputs)
    # (1,5), (2,4), (3,3), (5,1) dominate (4,4.5); expect 4 frontier points.
    assert result.metrics["n_evaluations"] == 5
    assert result.metrics["n_pareto_optimal"] == 4
    frontier = result.artifacts["frontier"]
    assert frontier.shape == (4, 2)
    assert (4.0, 4.5) not in [tuple(r) for r in frontier]


def test_u_hypervolume_nonneg() -> None:
    objectives = {"o1": lambda x: float(x), "o2": lambda x: float(-x)}
    result = UniversesFunctor(objectives).compute(_ScalarAdapter(), [0.0, 1.0, 2.0])
    assert result.metrics["hypervolume"] >= 0.0
