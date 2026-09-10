"""
DatavionOS platform bootstrap builder.

Builds the immutable runtime bootstrap payload consumed by
DatavionOS frontend applications.

The builder is intentionally a pure assembly layer.

It does NOT:

- resolve subscriptions
- resolve module availability
- evaluate RBAC
- evaluate feature entitlements
- resolve navigation
- resolve dashboard content

Those responsibilities belong to the appropriate
selectors, resolvers, builders, and services.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.builders.dashboard import (
    DashboardCard,
)
from apps.datavionos.builders.navigation import (
    NavigationItem,
)
from apps.datavionos.contracts.module import (
    ModuleContract,
)
from apps.datavionos.selectors.bootstrap import (
    PlatformBootstrapContext,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PlatformBootstrap:
    """
    Immutable DatavionOS runtime bootstrap payload.

    Runtime contract:

    - user context
    - tenant context
    - organization context
    - employee context
    - platform roles
    - organization roles
    - effective permissions
    - available modules
    - navigation
    - dashboard
    - feature flags
    - subscription
    - branding
    - preferences
    """

    context: PlatformBootstrapContext

    modules: tuple[ModuleContract, ...]

    navigation: tuple[NavigationItem, ...]

    dashboard: tuple[DashboardCard, ...]

    branding: dict[str, object]

    feature_flags: dict[str, bool]

    subscription: dict[str, object] | None

    preferences: dict[str, object] | None


class PlatformBootstrapBuilder:
    """
    Assemble the immutable DatavionOS bootstrap payload.

    This class contains no business logic.

    All supplied runtime data must already have been resolved by
    the appropriate upstream services/selectors/builders.
    """

    def build(
        self,
        *,
        context: PlatformBootstrapContext,
        modules: list[ModuleContract] | tuple[ModuleContract, ...],
        navigation: list[NavigationItem] | tuple[NavigationItem, ...],
        dashboard: list[DashboardCard] | tuple[DashboardCard, ...],
        branding: dict[str, object] | None = None,
        feature_flags: dict[str, bool] | None = None,
        subscription: dict[str, object] | None = None,
        preferences: dict[str, object] | None = None,
    ) -> PlatformBootstrap:
        """
        Create the immutable runtime bootstrap payload.

        Collections are normalized to tuples so the resulting
        bootstrap contract cannot be mutated after construction.

        Mutable mapping inputs are copied to prevent callers from
        mutating the bootstrap payload through their original
        dictionary references.
        """

        return PlatformBootstrap(
            context=context,
            modules=tuple(
                modules,
            ),
            navigation=tuple(
                navigation,
            ),
            dashboard=tuple(
                dashboard,
            ),
            branding=dict(
                branding or {},
            ),
            feature_flags=dict(
                feature_flags or {},
            ),
            subscription=(
                dict(subscription)
                if subscription is not None
                else None
            ),
            preferences=(
                dict(preferences)
                if preferences is not None
                else None
            ),
        )


platform_bootstrap_builder = PlatformBootstrapBuilder()


__all__ = (
    "PlatformBootstrap",
    "PlatformBootstrapBuilder",
    "platform_bootstrap_builder",
)
