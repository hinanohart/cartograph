# Contributing

Thanks for considering a contribution. Cartograph is research software; we
care about construct validity as much as about code.

## Development setup

```bash
git clone https://github.com/hinanohart/cartograph
cd cartograph
uv sync --all-extras --dev
uv run pytest -q
```

## Before opening a PR

- `uv run ruff check src tests && uv run ruff format --check src tests`
- `uv run mypy src`
- `uv run pytest tests/unit -q`
- New public API: include an ADR under `docs/decisions/`.
- New functor or capability: include a peer-review note in the PR
  describing how construct validity will be checked.

## Peer review process for releases

Every minor release ships with a peer review log in
`docs/peer_reviews/<version>.md`. The release workflow refuses to publish
without it (gate #6 of `scripts/verify_release.py`).

We target three external reviewers per release:

1. one philosopher familiar with *Schizoanalytic Cartographies*
2. one mechanistic interpretability researcher
3. one applied topological data analysis researcher

## Reporting construct-validity concerns

Construct validity (does the metric *measure* the Guattarian concept?) is the
single most likely failure mode of this project. Open an issue with the
`construct-validity` label; these jump to the front of the queue.

## Commit messages

Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`...). Do **not**
reference internal R-numbers (e.g. "R14 protocol") in commit messages; those
belong in PR descriptions.
