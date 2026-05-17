"""Model adapters. Phase 1a ships HuggingFace transformer + Mamba stub."""

from cartograph.adapters.hf_transformer import HFTransformerAdapter
from cartograph.adapters.mamba import MambaAdapter

__all__ = ["HFTransformerAdapter", "MambaAdapter"]
