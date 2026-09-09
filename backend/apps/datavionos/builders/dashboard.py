"""
DatavionOS dashboard builder.

Builds runtime dashboard cards from canonical ModuleContract instances.

Responsibilities
----------------
This builder is responsible only for dashboard presentation eligibility.

It evaluates:

- Module availability
- Dashboard configuration
- Feature entitlements
- RBAC permissions
- Deterministic dashboard ordering

Subscription/module entitlement resolution belongs to:

    ModuleAvailabilitySelector

The builder therefore does NOT query:

- Subscription models
- ModuleEntitlement
- Billing services
- Tenant models

Architecture:

ModuleAvailabilitySelector
        |
        v
Available ModuleContract[]
        |
        v
DashboardBuilder
        |
        +--> Feature flags
        |
        +--> RBAC permissions
        |
        +--> Dashboard configuration
        |
        v
DashboardCard[]
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
class DashboardCard:
    """
    Runtime dashboard card.

    This is a presentation contract generated from a
    canonical ModuleContract.
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
    Build runtime dashboard cards.

    The builder expects modules to have already passed platform-level
    availability and SaaS entitlement checks.

    Remaining dashboard visibility checks are:

    1. Module availability
    2. Dashboard configuration
    3. Feature entitlements
    4. RBAC permissions
    """

    def build(
        self,
        *,
        modules: list[ModuleContract],
        permissions: set[str],
        feature_flags: dict[str, bool],
    ) -> list[DashboardCard]:
        """
        Build dashboard cards from available modules.

        Args:
            modules:
                Modules already resolved by ModuleAvailabilitySelector.

            permissions:
                Effective permissions for the current runtime context.

            feature_flags:
                Enabled SaaS feature flags.

        Returns:
            Deterministically ordered dashboard cards.
        """

        cards: list[DashboardCard] = []

        for module in modules:
            if not self._module_available(
                module,
            ):
                continue

            dashboard = module.dashboard

            if dashboard is None:
                continue

            if not dashboard.enabled:
                continue

            if not self._features_enabled(
                module=module,
                feature_flags=feature_flags,
            ):
                continue

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
                    category=self._category_value(
                        module,
                    ),
                    order=dashboard.order,
                ),
            )

        return sorted(
            cards,
            key=lambda card: (
                card.order,
                card.key,
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

        Therefore the builder delegates to ``is_available`` rather than
        duplicating lifecycle logic.
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

        A module without feature requirements is allowed.

        A declared feature is considered enabled only when its runtime
        feature flag explicitly resolves to True.

        Missing feature flags therefore fail closed.
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
        module: ModuleContract,
        permissions: set[str],
    ) -> bool:
        """
        Determine whether the user may see the module dashboard card.

        Modules without declared permissions are available.

        When permissions are declared, at least one matching effective
        permission is required.
        """

        if not module.permissions:
            return True

        return any(permission in permissions for permission in module.permissions)

    # ==================================================================
    # Category
    # ==================================================================

    @staticmethod
    def _category_value(
        module: ModuleContract,
    ) -> str:
        """
        Resolve the serialized category value.

        ModuleCategory is normally an enum, but this helper keeps the
        presentation boundary tolerant of enum-backed and string-backed
        values.
        """

        return str(
            getattr(
                module.category,
                "value",
                module.category,
            ),
        )


__all__ = (
    "DashboardBuilder",
    "DashboardCard",
)
