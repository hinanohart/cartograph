"""Integration smoke: import + CLI run without crashing.

Marked `slow` only when it actually pulls a model. The default smoke
keeps everything offline so CI can run it on every push.
"""

from __future__ import annotations

import subprocess
import sys


def test_package_imports() -> None:
    import cartograph

    assert cartograph.__version__.startswith("0.1")


def test_cli_version_runs() -> None:
    out = subprocess.run(
        [sys.executable, "-m", "cartograph.cli", "--version"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "cartograph" in out.stdout


def test_cli_list_adapters_includes_builtins() -> None:
    out = subprocess.run(
        [sys.executable, "-m", "cartograph.cli", "list-adapters"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "hf-transformer" in out.stdout
    assert "mamba" in out.stdout
