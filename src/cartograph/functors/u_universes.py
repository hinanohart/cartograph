"""U (Universes of Reference): multi-objective Pareto loss surface projection.

Guattari's universes of reference are non-discursive value-domains a model
implicitly serves. We approximate them by the Pareto frontier of the model's
loss surface across multiple objectives (e.g. perplexity, calibration,
toxicity, refusal-rate), then read the geometry of that frontier as the
multi-valued reference system.

Phase 1a scope:
- accept a list of objective callables (model_output -> scalar)
- compute pairwise Pareto dominance counts
- report hypervolume + spread (delta) metrics

References:
- Miettinen 1999 (Tchebycheff scalarisation)
- pymoo (Blank & Deb 2020, arXiv:2002.04504) — production multi-objective lib
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

import numpy as np
import numpy.typing as npt

from cartograph.core.adapter import Capability, ModelAdapter
from cartograph.core.report import FunctorResult

Objective = Callable[[Any], float]
FloatArray = npt.NDArray[np.floating[Any]]
BoolArray = npt.NDArray[np.bool_]


class UniversesFunctor:
    """Estimate the Pareto frontier over user-supplied objectives."""

    name = "U"
    required: frozenset[Capability] = frozenset({Capability.LOSS_LANDSCAPE})

    def __init__(self, objectives: dict[str, Objective]) -> None:
        if len(objectives) < 2:
            raise ValueError("U requires >=2 objectives to define a Pareto surface")
        self.objectives = objectives

    def compute(self, adapter: ModelAdapter, inputs: Iterable[Any]) -> FunctorResult:
        adapter.requires(*self.required)
        objective_names = sorted(self.objectives)
        rows: list[list[float]] = []
        for x in inputs:
            out = adapter.forward(x)
            rows.append([float(self.objectives[k](out)) for k in objective_names])
        values = np.asarray(rows, dtype=np.float64)
        pareto_mask = self._pareto_mask(values)
        frontier = values[pareto_mask]
        metrics = {
            "n_evaluations": float(values.shape[0]),
            "n_pareto_optimal": float(int(pareto_mask.sum())),
            "hypervolume": float(self._hypervolume(frontier)),
            "spread": float(self._spread(frontier)),
        }
        return FunctorResult(
            functor=self.name,
            adapter=adapter.name,
            metrics=metrics,
            artifacts={"frontier": frontier, "objectives": objective_names},
            notes=f"objectives={objective_names}",
        )

    def compute_differentiable(self, adapter: ModelAdapter, inputs: Iterable[Any]) -> Any | None:
        return None

    @staticmethod
    def _pareto_mask(values: FloatArray) -> BoolArray:
        """Minimisation Pareto: row i is kept iff no other row j dominates it."""
        n = values.shape[0]
        keep = np.ones(n, dtype=bool)
        for i in range(n):
            le = np.all(values <= values[i], axis=1)
            lt_any = np.any(values < values[i], axis=1)
            dominators = le & lt_any
            dominators[i] = False
            if np.any(dominators):
                keep[i] = False
        return keep

    @staticmethod
    def _hypervolume(frontier: FloatArray) -> float:
        if frontier.size == 0:
            return 0.0
        ref = frontier.max(axis=0) + 1.0
        # Crude box-dominated approximation; pymoo handles SOTA when available.
        diffs = np.clip(ref - frontier, 0.0, None)
        return float(diffs.prod(axis=1).sum())

    @staticmethod
    def _spread(frontier: FloatArray) -> float:
        if frontier.shape[0] < 2:
            return 0.0
        ranges = frontier.max(axis=0) - frontier.min(axis=0)
        return float(np.linalg.norm(ranges))
