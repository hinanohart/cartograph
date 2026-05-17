"""HuggingFace transformer adapter.

Phase 1a wires hidden states + attention; SAE encoding is delegated to an
externally-loaded SAE-Lens release (default: GPT-2 small). Llama Scope
adoption is tracked as ADR-0001 residual issue #1.
"""

from __future__ import annotations

from typing import Any

from cartograph.core.adapter import Capability, MissingCapabilityError
from cartograph.core.registry import register_adapter


@register_adapter("hf-transformer")
class HFTransformerAdapter:
    """ModelAdapter-conforming wrapper around `transformers.AutoModel`.

    Heavy deps (`torch`, `transformers`, `sae_lens`) are imported lazily so
    `cartograph --version` works without a CUDA install.
    """

    name = "hf-transformer"

    def __init__(self, model_id: str = "gpt2", sae_release: str | None = None) -> None:
        # SAE_FEATURES is gated on sae_release so `requires(SAE_FEATURES)` fails
        # loud rather than letting the call dive into `_sae_activations` and
        # raise an opaque RuntimeError from `sae_encode` instead of the typed
        # MissingCapabilityError that the Protocol contract promises.
        caps: set[Capability] = {
            Capability.HIDDEN_STATES,
            Capability.ATTENTION,
            Capability.LOSS_LANDSCAPE,
        }
        if sae_release is not None:
            caps.add(Capability.SAE_FEATURES)
        self.capabilities: frozenset[Capability] = frozenset(caps)
        self.model_id = model_id
        self.sae_release = sae_release
        self._model: Any | None = None
        self._tokenizer: Any | None = None
        self._sae: Any | None = None

    def _ensure_model(self) -> None:
        if self._model is not None:
            return
        from transformers import AutoModel, AutoTokenizer

        self._tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self._model = AutoModel.from_pretrained(
            self.model_id, output_hidden_states=True, output_attentions=True
        )
        self._model.eval()

    def _ensure_sae(self) -> None:
        if self._sae is not None or self.sae_release is None:
            return
        from sae_lens import SAE

        self._sae, _, _ = SAE.from_pretrained(release=self.sae_release, sae_id="default")

    def requires(self, *needed: Capability) -> None:
        missing = frozenset(needed) - self.capabilities
        if missing:
            raise MissingCapabilityError(self.name, missing)

    def forward(self, inputs: Any) -> Any:
        import torch

        self._ensure_model()
        assert self._tokenizer is not None and self._model is not None
        tokens = self._tokenizer(inputs, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            return self._model(**tokens)

    def hidden_states(self, inputs: Any, layer: int) -> Any:
        out = self.forward(inputs)
        return out.hidden_states[layer]

    def attention(self, inputs: Any) -> Any:
        out = self.forward(inputs)
        return out.attentions

    def sae_encode(self, hidden: Any, layer: int) -> Any:
        if self.sae_release is None:
            raise RuntimeError(
                "sae_release was not provided; this adapter cannot encode SAE features"
            )
        self._ensure_sae()
        assert self._sae is not None
        return self._sae.encode(hidden).detach().cpu().numpy()
