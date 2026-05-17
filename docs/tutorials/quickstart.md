# Quickstart (GPT-2)

This walks through computing Φ and U on GPT-2 small. F and T are Phase 1b.

```python
from cartograph.adapters import HFTransformerAdapter
from cartograph.functors import PhiPhylaFunctor, UniversesFunctor

adapter = HFTransformerAdapter(model_id="gpt2", sae_release="gpt2-small-res-jb")

phi = PhiPhylaFunctor(layer=6).compute(adapter, inputs=["hello world"])
print(phi.metrics)

def perplexity(out) -> float:
    return float(out.logits.exp().mean())

def hidden_norm(out) -> float:
    return float(out.last_hidden_state.abs().mean())

u = UniversesFunctor(
    objectives={"perplexity": perplexity, "hidden_norm": hidden_norm},
).compute(adapter, inputs=["a", "b", "c"])
print(u.metrics)
```

The first call downloads the GPT-2 weights and the SAE-Lens release; subsequent
calls hit the local cache. For an offline smoke test that avoids any model
download, see `tests/unit/test_phi.py` which uses a `_FakeAdapter`.
