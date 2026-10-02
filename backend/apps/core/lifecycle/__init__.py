"""
DatavionOS lifecycle management.

Public API for platform startup, bootstrap and shutdown.
"""

from __future__ import annotations

from .bootstrap import (
    BootstrapState,
    bootstrap_platform,
    initialize_registries,
    is_bootstrapped,
)
from .shutdown import (
    shutdown_platform,
)
from .startup import (
    startup_platform,
)

__all__ = [
    "BootstrapState",
    "bootstrap_platform",
    "initialize_registries",
    "is_bootstrapped",
    "shutdown_platform",
    "startup_platform",
]
