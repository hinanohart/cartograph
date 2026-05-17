"""Minimal matplotlib renderer for a `CartographicProfile`.

Renders a 2x2 grid (Phi adjacency heatmap, U frontier scatter, F/T
placeholders) so that Phase 1a notebooks have visual feedback even
before F/T land.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cartograph.core.report import CartographicProfile


def plot_profile(profile: CartographicProfile, out_path: str | Path) -> Path:
    """Render `profile` to `out_path` (.png). Returns the resolved path."""

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    fig.suptitle(f"Cartographic profile — {profile.adapter}")

    _draw_phi(axes[0, 0], profile.results.get("Phi"))
    _draw_u(axes[0, 1], profile.results.get("U"))
    _placeholder(axes[1, 0], "F (Flows) — Phase 1b")
    _placeholder(axes[1, 1], "T (Territories) — Phase 1b")

    resolved = Path(out_path).resolve()
    resolved.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(resolved, dpi=120)
    plt.close(fig)
    return resolved


def _draw_phi(ax: Any, result: Any) -> None:
    if result is None:
        _placeholder(ax, "Phi — not computed")
        return
    adj = result.artifacts.get("adjacency")
    if adj is None:
        _placeholder(ax, "Phi — no adjacency artifact")
        return
    ax.imshow(adj, aspect="auto")
    ax.set_title("Phi: SAE co-activation (Jaccard)")


def _draw_u(ax: Any, result: Any) -> None:
    if result is None or result.artifacts.get("frontier") is None:
        _placeholder(ax, "U — not computed")
        return
    frontier = result.artifacts["frontier"]
    names = result.artifacts.get("objectives", ["o0", "o1"])
    if frontier.shape[1] < 2:
        _placeholder(ax, "U — needs >=2 objectives")
        return
    ax.scatter(frontier[:, 0], frontier[:, 1])
    ax.set_xlabel(names[0])
    ax.set_ylabel(names[1])
    ax.set_title("U: Pareto frontier")


def _placeholder(ax: Any, text: str) -> None:
    ax.text(0.5, 0.5, text, ha="center", va="center", fontsize=12)
    ax.set_xticks([])
    ax.set_yticks([])
