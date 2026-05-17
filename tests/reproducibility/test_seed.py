"""Reproducibility: Phi adjacency hash pinned across subprocess invocations.

The earlier shape of this test compared two same-process runs of the same
seeded RNG, which is a trivially-true property of deterministic generators.
This version (a) regenerates the artefact in a *separate* Python subprocess
so import order / global state cannot make it pass, and (b) compares the
hash against a golden value committed to this file. If BLAS or numpy
versions drift in a way that changes the bytes, the test fails loudly and
the maintainer has to bump the golden hash with an explicit commit.

Phase 1a only locks Phi adjacency. Phase 1b extends to all four functors
and is wired into the `reproduce.yml` workflow (paper-figure regeneration).
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
import textwrap

import pytest

# Golden hash captured on Linux/CPython 3.12/numpy 2.x with seed=42,
# 128x16 SAE features, coactivation_quantile=0.95. Update only with a
# deliberate commit that explains the cause (numpy major bump, BLAS swap,
# intentional algorithm change).
GOLDEN_HASH = "5de76427489741fef4964766fdd31dcc97ea89cf3e549df13cce2e1934394e3a"

_REGEN_SCRIPT = textwrap.dedent(
    """
    import hashlib, sys
    import numpy as np
    from cartograph.core.adapter import Capability, MissingCapabilityError
    from cartograph.functors.phi_phyla import PhiPhylaFunctor

    class _SeededFakeAdapter:
        name = "seeded-fake"
        capabilities = frozenset({Capability.HIDDEN_STATES, Capability.SAE_FEATURES})

        def __init__(self, seed):
            self._seed = seed

        def forward(self, inputs):
            return inputs

        def hidden_states(self, inputs, layer):
            return inputs

        def attention(self, inputs):
            raise MissingCapabilityError(self.name, frozenset({Capability.ATTENTION}))

        def sae_encode(self, hidden, layer):
            rng = np.random.default_rng(self._seed)
            return rng.random((128, 16))

        def requires(self, *needed):
            missing = frozenset(needed) - self.capabilities
            if missing:
                raise MissingCapabilityError(self.name, missing)

    adj = PhiPhylaFunctor(layer=0, coactivation_quantile=0.95).compute(
        _SeededFakeAdapter(seed=42), inputs="x"
    ).artifacts["adjacency"]
    sys.stdout.write(hashlib.sha256(adj.tobytes()).hexdigest())
    """
).strip()


@pytest.mark.reproducibility
def test_phi_adjacency_byte_identical_under_seed() -> None:
    proc = subprocess.run(
        [sys.executable, "-c", _REGEN_SCRIPT],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        # Surface child traceback to the parent run; otherwise debug is opaque.
        raise AssertionError(
            f"regen subprocess failed (rc={proc.returncode}):\n"
            f"--- stdout ---\n{proc.stdout}\n"
            f"--- stderr ---\n{proc.stderr}"
        )
    actual = proc.stdout.strip()
    assert actual == GOLDEN_HASH, (
        f"Phi adjacency hash drift: actual={actual} expected={GOLDEN_HASH}. "
        "Investigate before bumping the golden constant — likely numpy/BLAS "
        "change or accidental algorithm edit."
    )


@pytest.mark.reproducibility
def test_phi_adjacency_hash_is_deterministic() -> None:
    """Sanity: hashes from two same-process runs match (cheap fast check)."""

    digests: list[str] = []
    for _ in range(2):
        proc = subprocess.run(
            [sys.executable, "-c", _REGEN_SCRIPT],
            capture_output=True,
            text=True,
            check=True,
        )
        digests.append(hashlib.sha256(proc.stdout.strip().encode()).hexdigest())
    assert digests[0] == digests[1]
