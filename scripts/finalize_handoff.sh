#!/usr/bin/env bash
# finalize_handoff.sh
# ----------------------------------------------------------------------
# Cartograph alpha-pre v0.1.0a0 — the steps that still need a human
# decision after the repo is already public and CI is green.
#
# Current public state (verified 2026-05-18):
#   * https://github.com/hinanohart/cartograph  (public, Apache-2.0)
#   * https://hinanohart.github.io/cartograph/  (Pages, HTTP 200)
#   * main branch: 12 commits, ci/integration/docs all green
#   * branch protection: PR required, linear history, admin bypass on,
#                        3 required status checks
#   * dependabot alerts: 0 open
#   * open PRs: 0
#
# Run from the repo root:
#     bash scripts/finalize_handoff.sh
#
# Every block pauses for a y/N confirmation because each one is either
# externally irreversible (PyPI release), bills a credit card (kluster),
# or sends real messages to real people (peer outreach).
# ----------------------------------------------------------------------

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

confirm() {
  read -r -p "  proceed with: $1 ? [y/N] " ans
  [[ "$ans" == "y" || "$ans" == "Y" ]]
}

step() {
  echo
  echo "════════════════════════════════════════════════════════════════"
  echo " $1"
  echo "════════════════════════════════════════════════════════════════"
}

# ----------------------------------------------------------------------
step "1/4  Pre-flight (local mirror of CI gates)"
# ----------------------------------------------------------------------
echo "running the same gates CI runs, so any drift surfaces here first"
uv run pytest -q
uv run ruff check .
uv run mypy src/cartograph
uv run python scripts/verify_release.py --tag v0.1.0a0
echo "OK — all local gates pass."

# ----------------------------------------------------------------------
step "2/4  PyPI Trusted Publisher setup (REQUIRED before tag push)"
# ----------------------------------------------------------------------
cat <<'NOTE'
release.yml uses PyPI Trusted Publishing (OIDC, no API token in the repo).
That only works after PyPI knows which GitHub workflow it should trust.
Without this setup, the tag push will run release.yml and the publish
step will fail with "trusted publisher not configured" — the GitHub
Release will still be created, but PyPI will not receive the wheel.

Steps (one-time, takes ~2 min):
  1. Open  https://pypi.org/manage/account/publishing/
  2. "Add a new pending publisher" (project does not exist yet on PyPI)
     - PyPI Project Name : cartograph
     - Owner             : hinanohart
     - Repository name   : cartograph
     - Workflow name     : release.yml
     - Environment name  : (leave empty)
  3. Save.

If the project name `cartograph` is already taken on PyPI, pick an
alternative (e.g. `cartograph-oss`) and update pyproject.toml `name`
and CHANGELOG/CITATION accordingly — that itself is a code change that
needs a new commit before tagging.

NOTE
if confirm "open https://pypi.org/manage/account/publishing/ in your browser now"; then
  xdg-open "https://pypi.org/manage/account/publishing/" 2>/dev/null \
    || open "https://pypi.org/manage/account/publishing/" 2>/dev/null \
    || echo "(could not auto-open browser; visit the URL manually)"
fi

# ----------------------------------------------------------------------
step "3/4  Tag v0.1.0a0 and push (fires release.yml)"
# ----------------------------------------------------------------------
cat <<'NOTE'
This is the point of no return for the PyPI version number:
  - regenerates paper/figures via make_paper_figures.py
  - runs verify_release.py (six gates)
  - builds sdist + wheel with `uv build`
  - publishes to PyPI via Trusted Publishing (if configured in step 2)
  - creates a GitHub Release with auto-generated notes

PyPI version deletion is per-version-permanent: once 0.1.0a0 is up,
that exact string can never be reused even after `yank`. If you have
ANY doubt, say N here and fix things first.

NOTE
if confirm "git tag v0.1.0a0 && git push origin v0.1.0a0"; then
  if git rev-parse v0.1.0a0 >/dev/null 2>&1; then
    echo "tag v0.1.0a0 already exists locally; skipping tag creation"
  else
    git tag -a v0.1.0a0 -m "Phase 1a alpha-pre"
  fi
  git push origin v0.1.0a0
  echo
  echo "tag pushed. Watch the release run:"
  echo "  gh run watch --repo hinanohart/cartograph \$(gh run list --repo hinanohart/cartograph --workflow=release.yml --limit 1 --json databaseId --jq '.[0].databaseId')"
fi

# ----------------------------------------------------------------------
step "4/4  kluster.ai trial renewal + peer reviewer outreach"
# ----------------------------------------------------------------------
cat <<'NOTE'
(a) kluster.ai (optional, but recommended for ongoing work)
    The local trial expired during the build. To re-enable automatic
    code review on future commits:
      visit  https://platform.kluster.ai/
      pick a plan, subscribe, and the kluster_code_review_auto tool
      will start succeeding again on your next Claude Code session.

(b) Peer reviewer first contact (deadline 2026-06-17 — month 1 of 1a)
    Three slots from docs/peer_reviews/README.md:
      [ ] philosophy peer  (Pasquinelli / Hui / Sha Xin Wei orbit)
      [ ] mech-interp peer (TransformerLens / Anthropic / Nanda orbit)
      [ ] TDA peer         (giotto-tda / Carriere orbit)
    Tick each box in docs/peer_reviews/README.md when you send the
    first message; the review log lives under docs/peer_reviews/.

Optional follow-ups for later (not blocking v0.1.0a0):
  - Open an arXiv timing discussion in docs/decisions/ once the
    reviewer slate is confirmed.
  - When giotto-tda ships a Python 3.11+ wheel, revisit the
    `homology` extra (currently removed for Phase 1a).

DONE — everything past this point is on the human timeline.
NOTE
