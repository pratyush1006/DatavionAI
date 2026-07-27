"""
Plugin service aggregation.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.plugins.loader import (
    PluginLoader,
)
from apps.datavionos.plugins.registry import (
    PluginRegistry,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PluginServices:
    """
    Aggregate of plugin services.
    """

    registry: PluginRegistry

    loader: PluginLoader


__all__ = [
    "PluginServices",
]
