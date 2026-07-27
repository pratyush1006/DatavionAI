"""
Dependency injection registry contracts.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class ServiceLifetime(
    StrEnum,
):
    """
    Supported service lifetimes.
    """

    TRANSIENT = "transient"
    SCOPED = "scoped"
    SINGLETON = "singleton"


@dataclass(
    frozen=True,
    slots=True,
)
class ServiceRegistration:
    """
    Immutable service registration metadata.
    """

    service_type: type[Any]

    implementation_type: type[Any] | None = None

    factory: Callable[..., Any] | None = None

    instance: Any | None = None

    lifetime: ServiceLifetime = ServiceLifetime.SINGLETON

    name: str | None = None


__all__ = [
    "ServiceLifetime",
    "ServiceRegistration",
]
