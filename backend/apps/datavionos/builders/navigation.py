"""
DatavionOS navigation builder.

Builds runtime navigation from canonical ModuleContract instances.

Responsibilities
----------------
This builder is responsible only for navigation presentation eligibility.

It evaluates:

- Module availability
- Navigation configuration presence
- Feature entitlements
- RBAC permissions
- Deterministic navigation ordering

Subscription/module entitlement resolution belongs to:

    ModuleAvailabilitySelector

The builder therefore does NOT query:

- Subscription models
- ModuleEntitlement
- Billing services
- Tenant models
- Module registry discovery

Architecture:

ModuleAvailabilitySelector
        |
        v
Available ModuleContract[]
        |
        v
NavigationBuilder
        |
        +--> Navigation configuration
        |
        +--> Feature flags
        |
        +--> RBAC permissions
        |
        v
NavigationItem[]
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.contracts.module import (
    ModuleContract,
)


@dataclass(
    frozen=True,
    slots=True,
)
class NavigationItem:
    """
    Runtime sidebar navigation item.

    This is a presentation contract generated from a
    canonical ModuleContract.
    """

    title: str

    route: str

    icon: str

    category: str

    permissions: tuple[str, ...]

    order: int


class NavigationBuilder:
    """
    Build runtime navigation items.

    The builder expects modules to have already passed platform-level
    availability and SaaS entitlement checks.

    Remaining navigation visibility checks are:

    1. Module availability
    2. Navigation configuration presence
    3. Feature entitlements
    4. RBAC permissions
    """

    def build(
        self,
        *,
        modules: list[ModuleContract],
        permissions: set[str],
        feature_flags: dict[str, bool] | None = None,
    ) -> list[NavigationItem]:
        """
        Build navigation from available modules.

        Args:
            modules:
                Modules already resolved by ModuleAvailabilitySelector.

            permissions:
                Effective permissions for the current runtime context.

            feature_flags:
                Enabled SaaS feature flags.

        Returns:
            Deterministically ordered navigation items.
        """

        resolved_feature_flags = feature_flags if feature_flags is not None else {}

        navigation: list[NavigationItem] = []

        for module in modules:
            if not self._module_available(
                module,
            ):
                continue

            if not module.has_navigation:
                continue

            navigation_config = module.navigation

            # Defensive guard for static type narrowing and future
            # contract changes.
            if navigation_config is None:
                continue

            if not self._features_enabled(
                module=module,
                feature_flags=resolved_feature_flags,
            ):
                continue

            module_permissions = tuple(
                module.permissions,
            )

            if not self._has_permission(
                permissions=permissions,
                required_permissions=module_permissions,
            ):
                continue

            navigation.append(
                NavigationItem(
                    title=navigation_config.title,
                    route=navigation_config.route,
                    icon=navigation_config.icon,
                    category=self._category_value(
                        module,
                        navigation_config.category,
                    ),
                    permissions=module_permissions,
                    order=navigation_config.order,
                ),
            )

        return sorted(
            navigation,
            key=lambda item: (
                item.order,
                item.route,
            ),
        )

    # ==================================================================
    # Module Availability
    # ==================================================================

    @staticmethod
    def _module_available(
        module: ModuleContract,
    ) -> bool:
        """
        Validate platform-level module availability.

        ModuleContract owns the canonical lifecycle rule:

            enabled and active

        The builder delegates to ``is_available`` instead of duplicating
        lifecycle logic.
        """

        return module.is_available

    # ==================================================================
    # Feature Entitlements
    # ==================================================================

    @staticmethod
    def _features_enabled(
        *,
        module: ModuleContract,
        feature_flags: dict[str, bool],
    ) -> bool:
        """
        Determine whether all required module features are enabled.

        Modules without feature requirements are allowed.

        Missing feature flags fail closed.
        """

        if not module.feature_flags:
            return True

        return all(
            feature_flags.get(
                feature,
                False,
            )
            for feature in module.feature_flags
        )

    # ==================================================================
    # RBAC
    # ==================================================================

    @staticmethod
    def _has_permission(
        *,
        permissions: set[str],
        required_permissions: tuple[str, ...],
    ) -> bool:
        """
        Determine whether the user may see the navigation item.

        Modules without declared permissions are available.

        When permissions are declared, at least one matching effective
        permission is required.
        """

        if not required_permissions:
            return True

        return any(permission in permissions for permission in required_permissions)

    # ==================================================================
    # Category
    # ==================================================================

    @staticmethod
    def _category_value(
        module: ModuleContract,
        navigation_category: object,
    ) -> str:
        """
        Resolve the navigation category.

        Navigation configuration provides the explicit category.
        The module category is used as the fallback.

        Enum-backed values are normalized to their string value.
        """

        category = navigation_category if navigation_category else module.category

        return str(
            getattr(
                category,
                "value",
                category,
            ),
        )


__all__ = (
    "NavigationBuilder",
    "NavigationItem",
)
