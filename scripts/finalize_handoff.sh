#!/usr/bin/env bash
# finalize_handoff.sh
# ----------------------------------------------------------------------
# Cartograph alpha-pre v0.1.0a0 — the steps Claude could NOT do for you
# because they require either a network credential, a user-only token,
# or a deliberate human go/no-go.
#
# Run this from the repo root:
#     bash scripts/finalize_handoff.sh
#
# It is intentionally interactive — every block pauses for you to confirm,
# because each block has real-world side effects (publishes code, contacts
# people, posts to a public timeline) and a wrong choice is hard to undo.
#
# Constraints respected by this script:
#   * R13 — Claude cannot create or push public repositories; you do it.
#   * R11 — no API tokens are read here; gh / git use your local keychain.
#   * feedback_no-permanent-claim — release messages do not say
#     "complete" or "fully automatic".
#   * feedback_no-r-numbers-in-commits — no R-numbers in commit text.
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
step "1/6  Pre-flight: tests + verify_release + ruff + mypy"
# ----------------------------------------------------------------------
echo "running the same gates CI will run"
uv run pytest -q
uv run ruff check .
uv run mypy src/cartograph
uv run python scripts/verify_release.py --tag v0.1.0a0
echo "OK — all local gates pass."

# ----------------------------------------------------------------------
step "2/6  MEMORY.md: append the post-compact follow-up entries"
# ----------------------------------------------------------------------
cat <<'NOTE'
The auto-memory hook denies overwrites of MEMORY.md, so paste these two
lines into ~/.claude/projects/-home-runza/memory/MEMORY.md by hand under
the 📋 ログ / TODO section. (You can also use your editor of choice;
the file is plain markdown.)

  - [project_guattari-cartograph-arch-2026-05-17.md](project_guattari-cartograph-arch-2026-05-17.md) — Cartograph OSS HYBRID-S 確定アーキ。5 commit + 2 post-compact fix commit で v0.1.0a0 scaffold は SHIP-READY (local only)
  - [_log_cartograph_2026-05-17_post_compact_fix.md](_log_cartograph_2026-05-17_post_compact_fix.md) — 1 回目 audit: CRITICAL 3 / MAJOR 6 / MINOR 6 自動修正
  - [_log_cartograph_2026-05-17_post_compact_audit2.md](_log_cartograph_2026-05-17_post_compact_audit2.md) — 2 回目 audit: CRITICAL 3 / MAJOR 6 / MINOR 8 自動修正、verify_release 6/6 真 PASS (pytest 30/30)

NOTE
if confirm "open MEMORY.md in \$EDITOR now"; then
  "${EDITOR:-vi}" "$HOME/.claude/projects/-home-runza/memory/MEMORY.md"
fi

# ----------------------------------------------------------------------
step "3/6  GitHub: create the public repository (R13 trigger — explicit)"
# ----------------------------------------------------------------------
cat <<'NOTE'
This is the first irreversible public step. The repo URL hard-coded in
CITATION.cff / docs is https://github.com/hinanohart/cartograph .
Pre-conditions you must verify before saying y:
  * gh auth status reports a logged-in user that can create repos under
    the hinanohart org (or wherever the canonical home will live).
  * The repo name `cartograph` is available there.
  * You have read CITATION.cff to confirm the repository-code URL.

NOTE
if confirm "run: gh repo create hinanohart/cartograph --public --source=. --remote=origin --description 'Schizoanalytic diagnosis of foundation models (Phase 1a alpha-pre)'"; then
  gh repo create hinanohart/cartograph \
    --public --source=. --remote=origin \
    --description "Schizoanalytic diagnosis of foundation models (Phase 1a alpha-pre)"
fi

# ----------------------------------------------------------------------
step "4/6  Push main branch + tag v0.1.0a0"
# ----------------------------------------------------------------------
cat <<'NOTE'
This triggers release.yml on GitHub Actions, which will:
  - regenerate paper/figures via make_paper_figures.py
  - run verify_release.py (six gates)
  - build distributions with `uv build`
  - publish to PyPI via Trusted Publishing
  - create a GitHub Release with auto-generated notes

If anything is wrong, abort now: deleting a published PyPI version is
permanent on a per-version basis.

NOTE
if confirm "git push -u origin main"; then
  git push -u origin main
fi

if confirm "git tag v0.1.0a0 && git push origin v0.1.0a0   (this is what fires release.yml)"; then
  if git rev-parse v0.1.0a0 >/dev/null 2>&1; then
    echo "tag v0.1.0a0 already exists locally; skipping creation"
  else
    git tag -a v0.1.0a0 -m "Phase 1a alpha-pre"
  fi
  git push origin v0.1.0a0
fi

# ----------------------------------------------------------------------
step "5/6  kluster.ai trial: re-enable code review (optional)"
# ----------------------------------------------------------------------
cat <<'NOTE'
The local kluster trial expired during the build. If you want kluster
verification for further work on this repo:
  - visit https://platform.kluster.ai/ to pick a plan
  - subscribe / renew
  - the kluster_code_review_auto tool will start succeeding again
    automatically on the next session.

No action required if you are content to ship v0.1.0a0 without it.
NOTE

# ----------------------------------------------------------------------
step "6/6  Outreach: peer reviewer first contacts (deadline 2026-06-17)"
# ----------------------------------------------------------------------
cat <<'NOTE'
Three slots from docs/peer_reviews/README.md need first contact:
  - philosophy peer  (Pasquinelli / Hui / Sha Xin Wei orbit)
  - mech-interp peer (TransformerLens / Anthropic / Nanda orbit)
  - TDA peer         (giotto-tda / Carriere orbit)

Update the checkboxes in docs/peer_reviews/README.md as you go. The
month-1 deadline is 2026-06-17 (one month from v0.1.0a0 release date).

Optional: open arXiv timing discussion in docs/decisions/ once you have
the slate locked.

DONE — the rest of Phase 1a / 1b / 1c is on the human timeline.
NOTE
