"""Report + CartographicProfile shape."""

from __future__ import annotations

import pytest

from cartograph.core.report import CartographicProfile, FunctorResult


def _phi(adapter: str = "x") -> FunctorResult:
    return FunctorResult(functor="Phi", adapter=adapter, metrics={"n": 1.0})


def test_profile_is_complete_requires_all_four() -> None:
    partial = CartographicProfile(
        adapter="x", results={"Phi": _phi()}, cartograph_version="0.1.0a0"
    )
    assert not partial.is_complete()


def test_profile_functor_lookup() -> None:
    profile = CartographicProfile(
        adapter="x", results={"Phi": _phi()}, cartograph_version="0.1.0a0"
    )
    assert profile.functor("Phi").functor == "Phi"
    with pytest.raises(KeyError):
        profile.functor("U")
