"""
Module dependency contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ModuleDependencyType(
    StrEnum,
):
    """
    Relationship between modules.
    """

    REQUIRED = "required"

    OPTIONAL = "optional"

    EXTENSION = "extension"

    INCOMPATIBLE = "incompatible"


@dataclass(
    frozen=True,
    slots=True,
)
class ModuleDependency:
    """
    Immutable module dependency.
    """

    module_id: str

    dependency_type: ModuleDependencyType

    minimum_version: str | None = None

    maximum_version: str | None = None

    description: str | None = None


__all__ = [
    "ModuleDependency",
    "ModuleDependencyType",
]
