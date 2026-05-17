"""Report types: per-functor result + aggregated cartographic profile.

These are dataclasses to stay serialization-friendly (json/yaml) and to keep
the public surface auditable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class FunctorResult:
    """Output of one functor on one (adapter, input) pair."""

    functor: str
    adapter: str
    metrics: dict[str, float]
    artifacts: dict[str, Any] = field(default_factory=dict)
    notes: str = ""


@dataclass(frozen=True)
class CartographicProfile:
    """Aggregated four-functor diagnosis of a foundation model.

    `frozen=True` prevents rebinding the dataclass attributes, but the
    `results` dict itself remains mutable — `profile.results["X"] = ...`
    succeeds. Treat it as read-only; deep immutability would need a
    `MappingProxyType` wrapper which is Phase 1b polish.
    """

    adapter: str
    results: dict[str, FunctorResult]
    cartograph_version: str
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def functor(self, name: str) -> FunctorResult:
        if name not in self.results:
            raise KeyError(f"functor '{name}' not in profile. present: {sorted(self.results)}")
        return self.results[name]

    def is_complete(self) -> bool:
        """Phase 1a always False (F and T are stubs); becomes meaningful in 1b."""

        return {"F", "Phi", "T", "U"}.issubset(self.results)
