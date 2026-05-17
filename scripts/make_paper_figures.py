"""Regenerate paper figures from seed-fixed synthetic inputs.

Phase 1a only produces the Phi adjacency heatmap and an empty placeholder
for U. Phase 1b expands to all four functors.

Outputs are deterministic given the seed; the reproduce.yml workflow
compares the rendered PNGs byte-for-byte against `paper/figures.sha256`.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np


def render_phi_heatmap(out: Path, seed: int = 42) -> Path:
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(seed)
    adj = rng.random((16, 16))
    adj = (adj + adj.T) / 2.0
    np.fill_diagonal(adj, 0.0)

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(adj, aspect="auto")
    ax.set_title("Phi: SAE co-activation (synthetic)")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


def write_manifest(figures: list[Path], manifest: Path) -> None:
    lines = []
    for fig in figures:
        digest = hashlib.sha256(fig.read_bytes()).hexdigest()
        lines.append(f"{digest}  {fig.name}")
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(prog="make_paper_figures")
    parser.add_argument("--out", type=Path, default=Path("paper/figures"))
    args = parser.parse_args()

    figures = [render_phi_heatmap(args.out / "phi_heatmap.png")]
    write_manifest(figures, args.out.parent / "figures.sha256")
    for fig in figures:
        print(f"wrote {fig}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
