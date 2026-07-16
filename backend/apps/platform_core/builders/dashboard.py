"""
Platform dashboard builder.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.platform_core.registries.module import PlatformModule


@dataclass(
    frozen=True,
    slots=True,
)
class DashboardCard:
    """
    Dashboard card.
    """

    key: str

    title: str

    description: str

    icon: str

    route: str

    category: str

    order: int


class DashboardBuilder:
    """
    Build dashboard cards.
    """

    def build(
        self,
        *,
        modules: list[PlatformModule],
        permissions: set[str],
        feature_flags: dict[str, bool],
    ) -> list[DashboardCard]:
        """
        Build dashboard.
        """

        cards: list[DashboardCard] = []

        for module in modules:
            if not module.enabled:
                continue

            if module.permission not in permissions:
                continue

            cards.append(
                DashboardCard(
                    key=module.key,
                    title=module.title,
                    description=module.description,
                    icon=module.icon,
                    route=module.route,
                    category=module.category,
                    order=module.order,
                ),
            )

        return sorted(
            cards,
            key=lambda card: card.order,
        )


__all__ = [
    "DashboardBuilder",
    "DashboardCard",
]
