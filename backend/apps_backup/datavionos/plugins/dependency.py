"""
Plugin dependency contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PluginDependencyTarget(
    StrEnum,
):
    """
    Target type for a dependency.
    """

    MODULE = "module"

    PLUGIN = "plugin"


class PluginDependencyType(
    StrEnum,
):
    """
    Relationship between plugins and their dependencies.
    """

    REQUIRED = "required"

    OPTIONAL = "optional"

    EXTENSION = "extension"

    INCOMPATIBLE = "incompatible"


@dataclass(
    frozen=True,
    slots=True,
)
class PluginDependency:
    """
    Immutable plugin dependency.
    """

    target_type: PluginDependencyTarget

    target_id: str

    dependency_type: PluginDependencyType

    minimum_version: str | None = None

    maximum_version: str | None = None

    description: str | None = None


__all__ = [
    "PluginDependency",
    "PluginDependencyTarget",
    "PluginDependencyType",
]
