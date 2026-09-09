"""
DatavionOS module registry initializer.

Module definitions are discovered from the DatavionOS module package;
this initializer contains no module-specific list.
"""

from __future__ import annotations

from apps.datavionos.modules.registration import register_datavionos_modules


def initialize_module_registry() -> None:
    """Discover and register all DatavionOS module contracts."""

    register_datavionos_modules()


__all__ = [
    "initialize_module_registry",
]
