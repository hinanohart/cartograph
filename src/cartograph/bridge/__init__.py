"""Phase 2 (CFlow) differentiability seam.

This module exists in Phase 1a to lock the import surface. Phase 1a/1b
implementations all return `None` from `compute_differentiable`; Phase 2
ADR-XXXX-cflow-bridge decides whether CFlow lives in this repo or a sibling.
"""

from cartograph.bridge.differentiable import is_bridge_ready

__all__ = ["is_bridge_ready"]
