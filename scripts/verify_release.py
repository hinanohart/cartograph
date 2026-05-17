"""Six-item release gate (ADR-0001 §verify_release).

Fails loudly when any of these is not satisfied for a release tag:

1. every public functor's smoke test passes
2. adapter capability matrix in docs equals what code declares
3. paper/figures/ matches the reproduce.yml artefact byte-for-byte
4. CHANGELOG.md latest section matches the release tag
5. CITATION.cff version equals the release tag
6. docs/peer_reviews/<version>.md exists
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class GateFailure(RuntimeError):
    pass


def _strip_v(tag: str) -> str:
    return tag.removeprefix("v")


def gate_smoke_tests(_tag: str) -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/unit", "tests/integration", "-q"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        raise GateFailure("smoke tests failed")


def gate_capability_matrix(_tag: str) -> None:
    # Phase 1a: parse docs/reference/adapters.md once it exists; until then
    # this gate just asserts that every registered adapter is referenced.
    docs = REPO_ROOT / "docs" / "reference" / "adapters.md"
    if not docs.exists():
        raise GateFailure("missing docs/reference/adapters.md")
    text = docs.read_text(encoding="utf-8")
    from cartograph.core.registry import REGISTRY  # late import

    for name in REGISTRY:
        if name not in text:
            raise GateFailure(f"docs/reference/adapters.md missing adapter '{name}'")


def gate_paper_figures(_tag: str) -> None:
    figs = REPO_ROOT / "paper" / "figures"
    manifest = REPO_ROOT / "paper" / "figures.sha256"
    if not manifest.exists():
        raise GateFailure(
            "paper/figures.sha256 absent; run `python scripts/make_paper_figures.py` "
            "before tagging a release"
        )
    expected: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        # format: "<sha256>  <relpath>"
        digest, relpath = line.split("  ", 1)
        expected[relpath.strip()] = digest.strip()
    for relpath, expected_hash in expected.items():
        target = figs / relpath
        if not target.exists():
            raise GateFailure(f"figure {relpath} missing on disk")
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != expected_hash:
            raise GateFailure(f"figure {relpath} hash mismatch (expected {expected_hash})")


def gate_changelog(tag: str) -> None:
    changelog = REPO_ROOT / "CHANGELOG.md"
    if not changelog.exists():
        raise GateFailure("CHANGELOG.md missing")
    head = changelog.read_text(encoding="utf-8").splitlines()[:30]
    bare = _strip_v(tag)
    if not any(bare in line for line in head):
        raise GateFailure(f"CHANGELOG.md head does not mention tag {bare}")


def gate_citation(tag: str) -> None:
    citation = REPO_ROOT / "CITATION.cff"
    if not citation.exists():
        raise GateFailure("CITATION.cff missing")
    m = re.search(r"^version:\s*([^\s#]+)", citation.read_text(encoding="utf-8"), re.MULTILINE)
    if m is None:
        raise GateFailure("CITATION.cff has no version field")
    if m.group(1).strip().strip("\"'") != _strip_v(tag):
        raise GateFailure(f"CITATION.cff version {m.group(1)} != tag {_strip_v(tag)}")


def gate_peer_review_log(tag: str) -> None:
    log = REPO_ROOT / "docs" / "peer_reviews" / f"{_strip_v(tag)}.md"
    if not log.exists():
        raise GateFailure(f"missing peer review log: {log}")


Gate = Callable[[str], None]

GATES: list[tuple[str, Gate]] = [
    ("smoke tests", gate_smoke_tests),
    ("capability matrix", gate_capability_matrix),
    ("paper figures byte-identical", gate_paper_figures),
    ("CHANGELOG tag", gate_changelog),
    ("CITATION version", gate_citation),
    ("peer review log", gate_peer_review_log),
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="verify_release")
    parser.add_argument("--tag", required=True, help="release tag, e.g. v0.1.0a0")
    args = parser.parse_args(argv)

    failures: list[str] = []
    for name, fn in GATES:
        try:
            fn(args.tag)
            print(f"  PASS  {name}")
        except GateFailure as exc:
            failures.append(f"{name}: {exc}")
            print(f"  FAIL  {name}: {exc}")
    if failures:
        print(f"\n{len(failures)} of {len(GATES)} gates failed")
        return 1
    print(f"\nall {len(GATES)} gates passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
