"""
DatavionAI Service Registry.

Centralized registry for enterprise service classes.

Design Principles
-----------------
- Framework agnostic
- Lightweight
- Extensible
- Thread-safe registration
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

from .base import BaseService

###############################################################################
# Service Registry
###############################################################################

_SERVICE_REGISTRY: dict[
    str,
    type[BaseService],
] = {}

SERVICE_REGISTRY: Final[
    MappingProxyType[
        str,
        type[BaseService],
    ]
] = MappingProxyType(
    _SERVICE_REGISTRY,
)

###############################################################################
# Registration
###############################################################################


def register_service(
    name: str,
    service_class: type[BaseService],
    *,
    overwrite: bool = False,
) -> None:
    """
    Register a service.
    """

    if not overwrite and name in _SERVICE_REGISTRY:
        raise ValueError(f"Service '{name}' is already registered.")

    _SERVICE_REGISTRY[name] = service_class


###############################################################################
# Lookup
###############################################################################


def get_service(
    name: str,
) -> type[BaseService]:
    """
    Return a registered service.
    """

    try:
        return _SERVICE_REGISTRY[name]

    except KeyError as exc:
        raise LookupError(f"Unknown service '{name}'.") from exc


def has_service(
    name: str,
) -> bool:
    """
    Return True if a service is registered.
    """

    return name in _SERVICE_REGISTRY


def unregister_service(
    name: str,
) -> None:
    """
    Remove a registered service.
    """

    _SERVICE_REGISTRY.pop(
        name,
        None,
    )


def list_services() -> tuple[str, ...]:
    """
    Return all registered services.
    """

    return tuple(
        sorted(
            _SERVICE_REGISTRY.keys(),
        )
    )


###############################################################################
# Decorator
###############################################################################


def service(
    name: str,
):
    """
    Decorator for service registration.
    """

    def decorator(
        cls: type[BaseService],
    ) -> type[BaseService]:
        register_service(
            name,
            cls,
        )

        return cls

    return decorator


###############################################################################
# Public Exports
###############################################################################

__all__ = (
    "SERVICE_REGISTRY",
    "get_service",
    "has_service",
    "list_services",
    "register_service",
    "service",
    "unregister_service",
)
