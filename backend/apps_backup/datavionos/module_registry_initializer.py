"""DatavionOS module registry initializer.

DatavionOS module contracts are used by navigation/dashboard builders.
The current kernel bootstrap flow in this repo does not populate the
global `module_registry`, so we ensure AI module contracts are registered
during Django app startup.

This initializer is intentionally lightweight and idempotent.
"""

from __future__ import annotations

from apps.datavionos.modules.registration import (
    register_datavionos_modules,
)


def initialize_module_registry() -> None:
    """Register all platform module contracts required by DatavionOS."""

    register_datavionos_modules()
