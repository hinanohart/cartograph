"""Seam for Phase 2 CFlow (Chaosmotic refrain loss in Flow Matching).

In Phase 1a/1b every functor's `compute_differentiable` returns `None`.
The H3 GO/NO-GO at end of Phase 1c decides whether this becomes a real
backend or stays an unimplemented optional method forever.

This file deliberately holds zero logic. Putting the seam in place now
prevents a breaking-change rename later if H3 is GO.

**Pre-publication blocker (do not remove)**: before any CFlow paper is
submitted, CFlow must be mathematically differentiated from Stochastic
Interpolants (Albergo & Vanden-Eijnden 2023, arXiv:2406.07507). Without
a proof that the Chaosmotic refrain loss is not reducible to an SI
variant, CFlow collapses into a rebrand of known generative-modelling
machinery. The H3 ADR (forthcoming as `ADR-XXXX-cflow-bridge.md`) must
contain this differentiation as a required section, and the Phase 2
release gate must include it as a blocker.
"""

from __future__ import annotations


def is_bridge_ready() -> bool:
    """Return True when CFlow differentiable backends are wired up.

    Phase 1a always returns False. Phase 2 will replace the body.
    """

    return False
