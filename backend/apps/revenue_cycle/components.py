"""Shared Revenue Cycle execution context."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RevenueCycleContext:
    """Immutable context passed through Revenue Cycle workflows."""

    actor: Any
    tenant: Any
    organization: Any
    request_id: str | None = None


__all__ = ("RevenueCycleContext",)
