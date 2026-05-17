# paper/

LaTeX source for the Cartograph preprint. Lives in the same repo as the code
(see ADR-0001 residual issue #2: same-repo vs separate-repo decision is
deferred to Phase 1c start).

## Build

```bash
cd paper
latexmk -pdf main.tex
```

## Figures

`figures/` is regenerated nightly by the `reproduce.yml` workflow, which
runs `scripts/make_paper_figures.py`. The checksum manifest
`figures.sha256` is enforced by `scripts/verify_release.py` (release gate #3).
