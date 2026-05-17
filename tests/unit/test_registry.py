"""Registry: lookup + duplicate guard."""

from __future__ import annotations

import pytest

from cartograph.core.registry import (
    REGISTRY,
    load_adapter,
    register_adapter,
    register_builtin_adapters,
)


def test_hf_transformer_is_registered() -> None:
    register_builtin_adapters()
    assert "hf-transformer" in REGISTRY


def test_duplicate_registration_rejected() -> None:
    @register_adapter("__unit-test-temp__")
    def _factory():  # pragma: no cover - body not exercised
        raise RuntimeError("never called")

    try:
        with pytest.raises(ValueError):
            register_adapter("__unit-test-temp__")(_factory)
    finally:
        REGISTRY.pop("__unit-test-temp__", None)


def test_load_adapter_unknown_raises() -> None:
    with pytest.raises(KeyError):
        load_adapter("does-not-exist")
