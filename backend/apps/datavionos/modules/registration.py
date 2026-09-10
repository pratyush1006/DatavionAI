"""
DatavionOS module contract registration.

Registration is dynamic: every ``*_module.py`` definition in this package
is discovered and registered. No module-name list is maintained here.
"""

from __future__ import annotations

from apps.datavionos.registries.module import module_registry

from .discovery import discover_modules


def register_datavionos_modules() -> None:
    """Discover, validate and idempotently register module contracts."""

    discovered = discover_modules()
    registered = {module.identifier for module in module_registry.all()}
    pending = tuple(
        module for module in discovered
        if module.identifier not in registered
    )
    if pending:
        module_registry.register_modules(pending)


__all__ = [
    "register_datavionos_modules",
]
