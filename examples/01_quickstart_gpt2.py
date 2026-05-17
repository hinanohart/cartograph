"""Quickstart example: compute Φ and U on GPT-2 small.

Phase 1a deliberately ships this as `.py` rather than `.ipynb` so it is
linted, type-checked, and CI-executable without nbconvert. A Jupyter
notebook version arrives in Phase 1b once F and T can also be plotted.

Run (U only, no model download required for objectives that are constants):
    uv run python examples/01_quickstart_gpt2.py

Run (with Φ — requires HuggingFace + SAE-Lens download):
    uv run python examples/01_quickstart_gpt2.py --sae-release gpt2-small-res-jb
"""

from __future__ import annotations

import argparse
from typing import Any

from cartograph.adapters import HFTransformerAdapter
from cartograph.core.report import CartographicProfile, FunctorResult
from cartograph.functors import PhiPhylaFunctor, UniversesFunctor
from cartograph.viz import plot_profile


def _hidden_abs_mean(out: Any) -> float:
    return float(out.last_hidden_state.abs().mean())


def _hidden_l2(out: Any) -> float:
    return float(out.last_hidden_state.pow(2).mean().sqrt())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="quickstart")
    parser.add_argument("--model-id", default="gpt2", help="HF model id (default: gpt2 small)")
    parser.add_argument(
        "--sae-release",
        default=None,
        help="SAE-Lens release id (e.g. gpt2-small-res-jb); when omitted, Φ is skipped",
    )
    args = parser.parse_args(argv)

    adapter = HFTransformerAdapter(model_id=args.model_id, sae_release=args.sae_release)
    results: dict[str, FunctorResult] = {}

    if args.sae_release is not None:
        phi_result = PhiPhylaFunctor(layer=6).compute(adapter, inputs=["the quick brown fox"] * 8)
        results["Phi"] = phi_result
        print("Phi:", phi_result.metrics)

    u_result = UniversesFunctor(
        objectives={"hidden_abs_mean": _hidden_abs_mean, "hidden_l2": _hidden_l2},
    ).compute(adapter, inputs=["alpha", "beta", "gamma"])
    results["U"] = u_result
    print("U:", u_result.metrics)

    profile = CartographicProfile(
        adapter=adapter.name,
        results=results,
        cartograph_version="0.1.0a0",
    )
    out = plot_profile(profile, "examples/_out/quickstart_profile.png")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
