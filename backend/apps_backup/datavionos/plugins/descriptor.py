"""
Plugin descriptor contracts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class PluginCategory(
    StrEnum,
):
    """
    Plugin category.
    """

    INTEGRATION = "integration"

    AI = "ai"

    WORKFLOW = "workflow"

    ANALYTICS = "analytics"

    UI = "ui"

    AUTOMATION = "automation"

    CONNECTOR = "connector"

    CUSTOM = "custom"


class PluginStatus(
    StrEnum,
):
    """
    Plugin lifecycle status.
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
class PluginDescriptor:
    """
    Immutable plugin descriptor.
    """

    id: str

    name: str

    display_name: str

    version: str

    category: PluginCategory

    status: PluginStatus = PluginStatus.ACTIVE

    description: str | None = None

    author: str | None = None

    homepage: str | None = None

    target_modules: frozenset[str] = field(
        default_factory=frozenset,
    )

    tags: frozenset[str] = field(
        default_factory=frozenset,
    )

    metadata: dict[str, str] = field(
        default_factory=dict,
    )


__all__ = [
    "PluginCategory",
    "PluginDescriptor",
    "PluginStatus",
]
