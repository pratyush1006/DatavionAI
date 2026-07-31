"""
Module descriptor contracts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ModuleCategory(
    StrEnum,
):
    """
    Module category.
    """

    CORE = "core"

    CLINICAL = "clinical"

    ADMINISTRATIVE = "administrative"

    FINANCIAL = "financial"

    AI = "ai"

    INTEGRATION = "integration"

    PLATFORM = "platform"

    CUSTOM = "custom"


class ModuleStatus(
    StrEnum,
):
    """
    Module lifecycle status.
    """

    DEVELOPMENT = "development"

    PREVIEW = "preview"

    ACTIVE = "active"

    DEPRECATED = "deprecated"

    DISABLED = "disabled"


@dataclass(
    frozen=True,
    slots=True,
)
class ModuleDescriptor:
    """
    Immutable module descriptor.
    """

    id: str

    name: str

    display_name: str

    version: str

    category: ModuleCategory

    status: ModuleStatus = ModuleStatus.ACTIVE

    description: str | None = None

    author: str | None = None

    homepage: str | None = None

    tags: frozenset[str] = field(
        default_factory=frozenset,
    )

    metadata: dict[str, str] = field(
        default_factory=dict,
    )


__all__ = [
    "ModuleCategory",
    "ModuleDescriptor",
    "ModuleStatus",
]
