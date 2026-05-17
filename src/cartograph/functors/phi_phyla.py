"""Phi (Machinic Phyla): SAE feature graph + circuit decomposition.

Guattari frames Phi as the abstract-machinic plane that conditions which
concrete assemblages can form. We operationalise it in two layers:

- **Phase 1a (this release)**: the directed graph of sparse-autoencoder
  features that co-activate above threshold on a corpus. Returns adjacency
  + scalar centrality metrics. This alone is *not* the full Phi: it captures
  co-activation but not the directed *machinic* causation between feature
  groups.
- **Phase 1b (planned)**: circuit decomposition layered on top of the
  co-activation graph, following the Anthropic Transformer Circuits line
  (Elhage et al. 2021-2024) and using attribution-graph methods to recover
  directed feature→feature pathways. Without this layer Phi is incomplete
  as a Guattarian construct; see ADR-0001 §Weakness mitigations (W2).

Phase 1a scope (what this file actually implements):
- adjacency built from co-activation (Jaccard above quantile threshold)
- edge density + mean degree as scalar metrics
- adjacency artifact returned for downstream visualisation

References:
- Bricken et al. 2023 (Anthropic, SAE feature dictionaries)
- Elhage et al. 2021-2024 (Transformer Circuits) — Phase 1b decomposition basis
- He et al. 2024 (Llama Scope, arXiv:2410.20526) — adopt-decision in ADR Phase 1a mid
"""

from __future__ import annotations

from typing import Any

import numpy as np
import numpy.typing as npt

from cartograph.core.adapter import Capability, ModelAdapter
from cartograph.core.report import FunctorResult

FloatArray = npt.NDArray[np.floating[Any]]


class PhiPhylaFunctor:
    """Compute the machinic-phyla graph of an adapter on a corpus.

    Threshold semantics: when `coactivation_threshold` is given, a feature is
    counted as active iff its scalar activation strictly exceeds the absolute
    threshold (cross-batch comparable, recommended for cross-paper numbers).
    When `coactivation_threshold is None` (default), the threshold is the
    `coactivation_quantile`-th percentile *within the batch*, which keeps
    every batch's "top 1%" but is **not comparable across corpora or batches
    of different size**. Always pin the absolute threshold for publication.
    """

    name = "Phi"
    required: frozenset[Capability] = frozenset({Capability.HIDDEN_STATES, Capability.SAE_FEATURES})

    def __init__(
        self,
        layer: int,
        coactivation_quantile: float = 0.99,
        coactivation_threshold: float | None = None,
    ) -> None:
        if not 0.0 < coactivation_quantile < 1.0:
            raise ValueError("coactivation_quantile must lie in (0, 1)")
        self.layer = layer
        self.coactivation_quantile = coactivation_quantile
        self.coactivation_threshold = coactivation_threshold

    def compute(self, adapter: ModelAdapter, inputs: Any) -> FunctorResult:
        adapter.requires(*self.required)
        features = self._sae_activations(adapter, inputs)
        adjacency = self._coactivation_adjacency(features)
        metrics = {
            "n_features": float(features.shape[1]),
            "edge_density": float(adjacency.mean()),
            "mean_degree": float(adjacency.sum(axis=1).mean()),
        }
        thr_note = (
            f"abs={self.coactivation_threshold}"
            if self.coactivation_threshold is not None
            else f"q={self.coactivation_quantile}(batch-relative)"
        )
        return FunctorResult(
            functor=self.name,
            adapter=adapter.name,
            metrics=metrics,
            artifacts={"adjacency": adjacency},
            notes=f"layer={self.layer}, {thr_note}",
        )

    def compute_differentiable(self, adapter: ModelAdapter, inputs: Any) -> Any | None:
        """Phase 2 seam. Phase 1a returns None — bridge ADR pending."""

        return None

    def _sae_activations(self, adapter: ModelAdapter, inputs: Any) -> FloatArray:
        hidden = adapter.hidden_states(inputs, layer=self.layer)
        # Adapter is responsible for SAE encoding when SAE_FEATURES is declared.
        if hasattr(adapter, "sae_encode"):
            arr: FloatArray = np.asarray(adapter.sae_encode(hidden, layer=self.layer))
            return arr
        raise NotImplementedError(
            f"adapter '{adapter.name}' declared SAE_FEATURES but lacks sae_encode"
        )

    def _coactivation_adjacency(self, features: FloatArray) -> FloatArray:
        if features.ndim != 2:
            raise ValueError(f"features must be 2D (n_samples, n_features); got {features.shape}")
        if self.coactivation_threshold is None:
            threshold: FloatArray | float = np.quantile(
                features, self.coactivation_quantile, axis=0
            )
        else:
            threshold = float(self.coactivation_threshold)
        active = (features > threshold).astype(np.float32)
        co = active.T @ active
        np.fill_diagonal(co, 0.0)
        denom = active.sum(axis=0)[:, None] + active.sum(axis=0)[None, :] - co
        denom = np.where(denom > 0, denom, 1.0)
        jaccard: FloatArray = co / denom
        return jaccard
