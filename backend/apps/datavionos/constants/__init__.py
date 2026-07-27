"""
Public constants exported by the DatavionOS kernel.

The constants package contains immutable values that define the identity,
versioning, and other platform-wide metadata for DatavionOS.

Only stable, public constants should be re-exported from this module.
Avoid exposing implementation details or importing runtime components to
keep package initialization lightweight and free from side effects.
"""

from __future__ import annotations

from apps.datavionos.constants.capability import (
    CapabilityCategory,
    CapabilityStatus,
    ModuleCategory,
    ModuleStatus,
    PluginStatus,
    ServiceLifetime,
    ServiceStatus,
)
from apps.datavionos.constants.platform import (
    BOOTSTRAP_ENDPOINT,
    PLATFORM_NAME,
    PLATFORM_VERSION,
)
from apps.datavionos.constants.version import (
    DATAVIONOS_CODENAME,
    DATAVIONOS_NAME,
    DATAVIONOS_VENDOR,
    DATAVIONOS_VERSION,
    VERSION,
)

__all__ = [
    "BOOTSTRAP_ENDPOINT",
    "DATAVIONOS_CODENAME",
    "DATAVIONOS_NAME",
    "DATAVIONOS_VENDOR",
    "DATAVIONOS_VERSION",
    "PLATFORM_NAME",
    "PLATFORM_VERSION",
    "VERSION",
    "CapabilityCategory",
    "CapabilityStatus",
    "ModuleCategory",
    "ModuleStatus",
    "PluginStatus",
    "ServiceLifetime",
    "ServiceStatus",
]
