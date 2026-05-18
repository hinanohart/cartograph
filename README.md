# Cartograph

Diagnostic OSS for evaluating foundation models on Félix Guattari's four
schizoanalytic functors: **F** (Flows), **Φ** (Machinic Phyla), **T**
(Existential Territories), **U** (Universes of Reference).

> [!IMPORTANT]
> Research software. The Phase 1a `v0.1.0a0` alpha-pre ships **Φ** and **U**
> as working functors; **F** and **T** are typed stubs that land in Phase 1b.
> See [ADR-0001](docs/decisions/ADR-0001-hybrid-s.md).

## Why this exists

Mechanistic interpretability tells us *how* a circuit fires. Cartograph asks an
orthogonal question: *what kind of subjectivity does this model produce?* The
four functors operationalise that question from *Schizoanalytic Cartographies*
(1989) without rebranding existing techniques. Construct validity is gated on
external peer review at every minor release.

> ⚠️ **PyPI name notice**: A package named `cartograph` already exists on PyPI from a different author. **Do NOT** run `pip install cartograph` or `uv add cartograph`. This project is distributed via GitHub source only until a unique PyPI name is chosen. See https://github.com/hinanohart/cartograph#install for the correct install method.

## Install

```bash
uv add cartograph  # do not run, see above
```

Optional extras: `cartograph[homology]` (giotto-tda + ripser, Phase 1b),
`cartograph[mamba]` (mamba-ssm, Phase 1b), `cartograph[all]`.

## Quickstart

```python
from cartograph.adapters import HFTransformerAdapter
from cartograph.functors import PhiPhylaFunctor

adapter = HFTransformerAdapter(model_id="gpt2", sae_release="gpt2-small-res-jb")
result = PhiPhylaFunctor(layer=6).compute(adapter, inputs=["hello world"])
print(result.metrics)
```

Full walkthrough: [docs/tutorials/quickstart.md](docs/tutorials/quickstart.md).

## Release plan

| Phase | Tag | Scope | Gate |
|---|---|---|---|
| 1a | `v0.1.0a0` | Φ + U + adapter Protocol | two internal peers |
| 1b | `v0.2.0` | + F + T integrated report | ≥3 external peers (philosophy / mech-interp / TDA) |
| 1c | `v0.3.0` | docs + examples + arXiv preprint | preprint posted |
| 2  | — | CFlow (intervention) | H3 GO/NO-GO decision |

Honest estimate: ~5-6 months on a single maintainer.

## Non-claims

This README intentionally does not say "complete", "permanent", or
"fully automatic". The project ships in stages, every release carries an
explicit peer-review log, and construct-validity gaps are recorded in
`docs/peer_reviews/` rather than hidden.

## Citing

See [CITATION.cff](CITATION.cff). When citing the project itself, include
the version tag; when citing Guattari's framework, cite *Schizoanalytic
Cartographies* (Athlone 2013 translation) and Segovia 2025 for the
four-functor reading.

## License

[Apache-2.0](LICENSE).

## Acknowledgements

Builds on TransformerLens, SAE-Lens, pymoo, and (Phase 1b) giotto-tda /
ripser / mamba-ssm. See ADR-0001 for the architecture rationale and the
six structural weaknesses (W1-W6) it mitigates.
