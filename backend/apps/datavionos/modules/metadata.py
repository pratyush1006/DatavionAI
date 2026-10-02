"""
Module metadata contracts.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(
    frozen=True,
    slots=True,
)
class ModuleMetadata:
    """
    Presentation metadata for a module.
    """

    icon: str | None = None

    color: str | None = None

    category_label: str | None = None

    navigation_group: str | None = None

    display_order: int = 0

    visible: bool = True

    featured: bool = False

    supports_search: bool = True

    supports_favorites: bool = True

    supported_locales: frozenset[str] = field(
        default_factory=frozenset,
    )

    keywords: frozenset[str] = field(
        default_factory=frozenset,
    )

    metadata: dict[str, str] = field(
        default_factory=dict,
    )


__all__ = [
    "ModuleMetadata",
]
