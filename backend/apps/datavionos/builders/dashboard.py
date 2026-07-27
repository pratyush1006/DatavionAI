"""
Platform dashboard builder.

Builds runtime dashboard cards from
DatavionOS module contracts.

Dashboard visibility is controlled by:

1. Module availability
2. Subscription enabled modules
3. Feature flags
4. RBAC permissions
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.registries.module import (
    PlatformModule,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DashboardCard:
    """
    Runtime dashboard card.
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
    Build dashboard cards from runtime modules.
    """

    def build(
        self,
        *,
        modules: list[PlatformModule],
        permissions: set[str],
        feature_flags: dict[str, bool],
    ) -> list[DashboardCard]:
        """
        Build runtime dashboard.

        Filtering order:

        1. Module enabled state
        2. Dashboard availability
        3. Feature flag entitlement
        4. Permission authorization
        """

        cards: list[DashboardCard] = []

        for module in modules:
            #
            # Module enabled validation
            #
            if not self._module_enabled(
                module,
            ):
                continue

            #
            # Dashboard configuration validation
            #
            dashboard = getattr(
                module,
                "dashboard",
                None,
            )

            if dashboard is None:
                continue

            #
            # Feature flags
            #
            if not self._features_enabled(
                module=module,
                feature_flags=feature_flags,
            ):
                continue

            #
            # RBAC permissions
            #
            if not self._has_permission(
                module=module,
                permissions=permissions,
            ):
                continue

            cards.append(
                DashboardCard(
                    key=module.identifier,
                    title=dashboard.title,
                    description=dashboard.description,
                    icon=dashboard.icon,
                    route=dashboard.route,
                    category=(
                        module.category.value
                        if hasattr(
                            module.category,
                            "value",
                        )
                        else str(
                            module.category,
                        )
                    ),
                    order=dashboard.order,
                )
            )

        return sorted(
            cards,
            key=lambda card: card.order,
        )

    def _module_enabled(
        self,
        module: PlatformModule,
    ) -> bool:
        """
        Check module availability.
        """

        return bool(
            module.enabled,
        )

    def _features_enabled(
        self,
        *,
        module: PlatformModule,
        feature_flags: dict[str, bool],
    ) -> bool:
        """
        Check module feature requirements.
        """

        if not module.feature_flags:
            return True

        return all(
            feature_flags.get(
                flag,
                False,
            )
            for flag in module.feature_flags
        )

    def _has_permission(
        self,
        *,
        module: PlatformModule,
        permissions: set[str],
    ) -> bool:
        """
        Check module RBAC access.
        """

        if not module.permissions:
            return True

        return any(permission in permissions for permission in module.permissions)


__all__ = [
    "DashboardBuilder",
    "DashboardCard",
]
