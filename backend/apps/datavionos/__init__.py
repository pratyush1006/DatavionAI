"""
DatavionOS Kernel.

DatavionOS is the AI-native, multi-tenant healthcare operating system that
provides the runtime infrastructure for the DatavionAI platform.

The kernel is responsible for platform composition, plugin discovery,
capability resolution, workspace orchestration, event dispatching,
and bootstrap generation.

This package intentionally exposes only stable public metadata. Runtime
components are imported lazily by consumers to avoid circular imports and
minimize import side effects.
"""

from __future__ import annotations

from apps.datavionos.constants.version import (
    DATAVIONOS_VERSION,
)

__version__ = DATAVIONOS_VERSION

__all__ = [
    "__version__",
]
