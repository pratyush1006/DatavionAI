"""
Platform bootstrap builder.

Builds the DatavionOS runtime bootstrap payload.

The bootstrap payload is the runtime contract between
the DatavionOS backend kernel and frontend applications.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.builders.dashboard import (
    DashboardCard,
)
from apps.datavionos.builders.navigation import (
    NavigationItem,
)
from apps.datavionos.registries.module import (
    PlatformModule,
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
    - modules
    - navigation
    - dashboard
    - feature flags
    - subscription
    - branding
    """

    context: PlatformBootstrapContext

    modules: tuple[PlatformModule, ...]

    navigation: tuple[NavigationItem, ...]

    dashboard: tuple[DashboardCard, ...]

    branding: dict[str, object]

    feature_flags: dict[str, bool]

    subscription: dict[str, object] | None

    preferences: dict[str, object] | None


class PlatformBootstrapBuilder:
    """
    Builds immutable DatavionOS bootstrap payload.

    This layer does not resolve business rules.
    It only assembles already resolved runtime data.
    """

    def build(
        self,
        *,
        context: PlatformBootstrapContext,
        modules: list[PlatformModule],
        navigation: list[NavigationItem],
        dashboard: list[DashboardCard],
        branding: dict[str, object] | None = None,
        feature_flags: dict[str, bool] | None = None,
        subscription: dict[str, object] | None = None,
        preferences: dict[str, object] | None = None,
    ) -> PlatformBootstrap:
        """
        Create runtime bootstrap object.
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
            branding=(branding or {}),
            feature_flags=(feature_flags or {}),
            subscription=subscription,
            preferences=preferences,
        )


platform_bootstrap_builder = PlatformBootstrapBuilder()


__all__ = (
    "PlatformBootstrap",
    "PlatformBootstrapBuilder",
    "platform_bootstrap_builder",
)
