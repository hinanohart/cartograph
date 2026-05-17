"""Adapter registry. Phase 1a uses a simple in-process dict.

Phase 1b end (see ADR-0001) will decide whether to open this via
`importlib.metadata.entry_points` for third-party adapters.
"""

from __future__ import annotations

from collections.abc import Callable

from cartograph.core.adapter import ModelAdapter

AdapterFactory = Callable[..., ModelAdapter]

REGISTRY: dict[str, AdapterFactory] = {}


def register_adapter(name: str) -> Callable[[AdapterFactory], AdapterFactory]:
    """Decorator that registers an adapter factory under `name`.

    Duplicate names raise `ValueError` — silent override masks bugs.
    """

    def _decorate(factory: AdapterFactory) -> AdapterFactory:
        if name in REGISTRY:
            raise ValueError(f"adapter '{name}' already registered")
        REGISTRY[name] = factory
        return factory

    return _decorate


def load_adapter(name: str, **kwargs: object) -> ModelAdapter:
    if name not in REGISTRY:
        raise KeyError(f"unknown adapter '{name}'. registered: {sorted(REGISTRY)}")
    return REGISTRY[name](**kwargs)


def register_builtin_adapters() -> None:
    """Import built-in adapter modules so their decorators fire.

    Idempotent: re-import of an already-loaded module is a no-op in Python,
    and `register_adapter` raises only on *new* duplicate registration.
    Call this from any entry point that needs the registry populated
    (CLI, tests) instead of relying on side-effect imports.
    """

    import cartograph.adapters  # noqa: F401
