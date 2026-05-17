"""Minimal CLI entry point. Phase 1a exposes version + listing only.

Subcommands (`diagnose`, `report`) arrive in Phase 1b once F/T functors land.
"""

from __future__ import annotations

import argparse
import sys

from cartograph import __version__
from cartograph.core.registry import REGISTRY, register_builtin_adapters


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cartograph")
    parser.add_argument("--version", action="version", version=f"cartograph {__version__}")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("list-adapters", help="list registered model adapters")

    args = parser.parse_args(argv)

    if args.cmd == "list-adapters":
        register_builtin_adapters()
        for name in sorted(REGISTRY):
            print(name)
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
