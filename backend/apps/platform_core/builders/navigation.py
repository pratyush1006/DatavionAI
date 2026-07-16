"""
Navigation builder.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.platform_core.registries.module_registry import (
    module_registry,
)


@dataclass(
    frozen=True,
    slots=True,
)
class NavigationItem:
    """
    Sidebar navigation item.
    """

    title: str

    route: str

    icon: str

    category: str


class NavigationBuilder:
    """
    Build sidebar navigation.
    """

    def build(
        self,
        permissions: set[str],
    ) -> list[NavigationItem]:
        """
        Build navigation.
        """

        navigation: list[NavigationItem] = []

        for module in module_registry.all():
            if not module.enabled or module.permission not in permissions:
                continue

            navigation.append(
                NavigationItem(
                    title=module.title,
                    route=module.route,
                    icon=module.icon,
                    category=module.category,
                ),
            )

        return navigation


__all__ = [
    "NavigationBuilder",
    "NavigationItem",
]
