"""Quickstart example: compute Φ and U on GPT-2 small.

Phase 1a deliberately ships this as `.py` rather than `.ipynb` so it is
linted, type-checked, and CI-executable without nbconvert. A Jupyter
notebook version arrives in Phase 1b once F and T can also be plotted.

Run:
    uv run python examples/01_quickstart_gpt2.py
"""

from __future__ import annotations

from cartograph.adapters import HFTransformerAdapter
from cartograph.core.report import CartographicProfile
from cartograph.functors import PhiPhylaFunctor, UniversesFunctor
from cartograph.viz import plot_profile


def main() -> int:
    adapter = HFTransformerAdapter(model_id="gpt2", sae_release=None)

    phi_result = PhiPhylaFunctor(layer=6).compute(adapter, inputs="hello world") if False else None
    # Phase 1a: Φ requires an SAE release. The default path here would download
    # one; for an offline demo see tests/unit/test_phi.py.

    def perplexity(out) -> float:
        return float(out.last_hidden_state.exp().mean())

    def hidden_norm(out) -> float:
        return float(out.last_hidden_state.abs().mean())

    u_result = UniversesFunctor(
        objectives={"perplexity": perplexity, "hidden_norm": hidden_norm},
    ).compute(adapter, inputs=["alpha", "beta", "gamma"])
    print(u_result.metrics)

    profile = CartographicProfile(
        adapter=adapter.name,
        results={"U": u_result, **({"Phi": phi_result} if phi_result else {})},
        cartograph_version="0.1.0a0",
    )
    out = plot_profile(profile, "examples/_out/quickstart_profile.png")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
