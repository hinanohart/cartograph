"""Seam for Phase 2 CFlow (Chaosmotic refrain loss in Flow Matching).

In Phase 1a/1b every functor's `compute_differentiable` returns `None`.
The H3 GO/NO-GO at end of Phase 1c decides whether this becomes a real
backend or stays an unimplemented optional method forever.

This file deliberately holds zero logic. Putting the seam in place now
prevents a breaking-change rename later if H3 is GO.
"""

from __future__ import annotations


def is_bridge_ready() -> bool:
    """Return True when CFlow differentiable backends are wired up.

    Phase 1a always returns False. Phase 2 will replace the body.
    """

    return False
