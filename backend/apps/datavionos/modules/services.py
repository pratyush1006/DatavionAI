"""
Module service aggregation.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.modules.loader import (
    ModuleLoader,
)
from apps.datavionos.modules.registry import (
    ModuleRegistry,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ModuleServices:
    """
    Aggregate of module services.
    """

    registry: ModuleRegistry

    loader: ModuleLoader


__all__ = [
    "ModuleServices",
]
