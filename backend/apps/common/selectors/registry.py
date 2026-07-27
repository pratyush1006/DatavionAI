"""
DatavionOS Selector Registry.

Enterprise registry for selector discovery.

Supports:

- Selector registration
- Metadata discovery
- Tenant awareness
- Safe runtime lookup
- Thread-safe operations
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from types import MappingProxyType
from typing import Final

from .base import BaseSelector

# ============================================================================
# Metadata
# ============================================================================


@dataclass(
    frozen=True,
    slots=True,
)
class SelectorRegistration:
    """
    Selector registration metadata.
    """

    name: str

    selector: type[BaseSelector]

    module: str

    description: str | None = None

    tenant_scoped: bool = True


# ============================================================================
# Registry Storage
# ============================================================================


_SELECTOR_REGISTRY: dict[
    str,
    SelectorRegistration,
] = {}


_REGISTRY_LOCK = RLock()


SELECTOR_REGISTRY: Final = MappingProxyType(
    _SELECTOR_REGISTRY,
)


# ============================================================================
# Registration
# ============================================================================


def register_selector(
    name: str,
    selector_class: type[BaseSelector],
    *,
    description: str | None = None,
    tenant_scoped: bool = True,
    overwrite: bool = False,
) -> None:
    """
    Register selector.
    """

    with _REGISTRY_LOCK:
        if not overwrite and name in _SELECTOR_REGISTRY:
            existing = _SELECTOR_REGISTRY[name]

            raise ValueError(
                f"Selector '{name}' already "
                f"registered by "
                f"{existing.selector.__module__}."
            )

        _SELECTOR_REGISTRY[name] = SelectorRegistration(
            name=name,
            selector=selector_class,
            module=selector_class.__module__,
            description=description,
            tenant_scoped=tenant_scoped,
        )


# ============================================================================
# Lookup
# ============================================================================


def get_selector(
    name: str,
) -> type[BaseSelector]:
    """
    Return selector class.
    """

    try:
        return _SELECTOR_REGISTRY[name].selector

    except KeyError as exc:
        raise LookupError(f"Unknown selector '{name}'.") from exc


def get_selector_metadata(
    name: str,
) -> SelectorRegistration:
    """
    Return selector metadata.
    """

    try:
        return _SELECTOR_REGISTRY[name]

    except KeyError as exc:
        raise LookupError(f"Unknown selector '{name}'.") from exc


def has_selector(
    name: str,
) -> bool:
    """
    Check selector existence.
    """

    return name in _SELECTOR_REGISTRY


def unregister_selector(
    name: str,
) -> None:
    """
    Remove selector.
    """

    with _REGISTRY_LOCK:
        _SELECTOR_REGISTRY.pop(
            name,
            None,
        )


def list_selectors() -> tuple[str, ...]:
    """
    Return selector names.
    """

    return tuple(
        sorted(
            _SELECTOR_REGISTRY.keys(),
        )
    )


# ============================================================================
# Decorator
# ============================================================================


def selector(
    name: str,
    *,
    description: str | None = None,
    tenant_scoped: bool = True,
):
    """
    Selector registration decorator.
    """

    def decorator(
        cls: type[BaseSelector],
    ) -> type[BaseSelector]:

        register_selector(
            name,
            cls,
            description=description,
            tenant_scoped=tenant_scoped,
        )

        return cls

    return decorator


__all__: tuple[str, ...] = (
    "SELECTOR_REGISTRY",
    "SelectorRegistration",
    "get_selector",
    "get_selector_metadata",
    "has_selector",
    "list_selectors",
    "register_selector",
    "selector",
    "unregister_selector",
)
