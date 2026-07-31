"""
Navigation builder.

Builds runtime navigation from registered DatavionOS modules.

Navigation visibility is controlled by:

1. Module availability
2. Feature flags
3. Subscription entitlement
4. RBAC permissions
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.registries.module import (
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

    permissions: tuple[str, ...]

    order: int


class NavigationBuilder:
    """
    Build runtime navigation.

    Navigation is dynamically generated
    per tenant runtime context.
    """

    def build(
        self,
        *,
        permissions: set[str],
        feature_flags: dict[str, bool] | None = None,
        modules: list | None = None,
    ) -> list[NavigationItem]:
        """
        Build navigation based on runtime access.
        """

        feature_flags = feature_flags or {}

        available_modules = modules if modules is not None else module_registry.all()

        navigation: list[NavigationItem] = []

        for module in available_modules:
            #
            # Module availability
            #
            if not module.enabled:
                continue

            #
            # Navigation metadata
            #
            navigation_config = getattr(
                module,
                "navigation",
                None,
            )

            #
            # Module has no navigation
            #
            if navigation_config is None:
                continue

            #
            # Feature flag validation
            #
            module_features = getattr(
                module,
                "feature_flags",
                (),
            )

            if module_features and not all(
                feature_flags.get(
                    feature,
                    False,
                )
                for feature in module_features
            ):
                continue

            #
            # Permission validation
            #
            module_permissions = tuple(
                getattr(
                    module,
                    "permissions",
                    (),
                )
                or ()
            )

            if module_permissions and not any(
                permission in permissions for permission in module_permissions
            ):
                continue

            navigation.append(
                NavigationItem(
                    title=navigation_config.title,
                    route=navigation_config.route,
                    icon=navigation_config.icon,
                    category=navigation_config.category,
                    permissions=module_permissions,
                    order=navigation_config.order,
                )
            )

        return sorted(
            navigation,
            key=lambda item: item.order,
        )


__all__ = (
    "NavigationBuilder",
    "NavigationItem",
)
