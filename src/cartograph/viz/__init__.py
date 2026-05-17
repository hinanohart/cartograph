"""Visualisation. Phase 1a ships a minimal matplotlib renderer only.

The Visualizer Protocol (residual issue #4) is opened at end of Phase 1b
once we have all four functors' artifact shapes nailed down.
"""

from cartograph.viz.matplotlib_basic import plot_profile

__all__ = ["plot_profile"]
