"""
DatavionOS navigation registry.

Converts enabled platform modules into
frontend navigation metadata.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class NavigationItem:
    """
    Frontend navigation item.
    """

    label: str

    route: str

    icon: str

    module: str

    category: str


class NavigationRegistry:
    """
    Runtime navigation registry.
    """

    _items: dict[str, NavigationItem] = {}

    @classmethod
    def register(
        cls,
        item: NavigationItem,
    ) -> None:

        cls._items[item.module] = item

    @classmethod
    def resolve(
        cls,
        modules: list,
    ) -> list[NavigationItem]:
        """
        Resolve navigation from enabled modules.
        """

        result = []

        for module in modules:
            item = cls._items.get(
                module.code,
            )

            if item:
                result.append(
                    item,
                )

        return result


NavigationRegistry.register(
    NavigationItem(
        label="AI Healthcare Copilot",
        route="/ai",
        icon="brain",
        module="ai",
        category="artificial_intelligence",
    )
)


NavigationRegistry.register(
    NavigationItem(
        label="Billing",
        route="/billing",
        icon="credit-card",
        module="billing",
        category="platform",
    )
)


NavigationRegistry.register(
    NavigationItem(
        label="Patients",
        route="/patients",
        icon="users",
        module="patients",
        category="clinical",
    )
)


NavigationRegistry.register(
    NavigationItem(
        label="Appointments",
        route="/appointments",
        icon="calendar",
        module="appointments",
        category="clinical",
    )
)


__all__ = [
    "NavigationItem",
    "NavigationRegistry",
]
