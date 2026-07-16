"""
Platform bootstrap builder.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.platform_core.builders.dashboard import (
    DashboardCard,
)
from apps.platform_core.builders.navigation import (
    NavigationItem,
)
from apps.platform_core.registries.module import (
    PlatformModule,
)
from apps.platform_core.selectors.bootstrap import (
    PlatformBootstrapContext,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PlatformBootstrap:
    """
    Platform bootstrap payload.
    """

    context: PlatformBootstrapContext

    modules: list[PlatformModule]

    navigation: list[NavigationItem]

    dashboard: list[DashboardCard]

    branding: dict[str, object]

    feature_flags: dict[str, bool]

    subscription: dict[str, object]

    preferences: dict[str, object]


class PlatformBootstrapBuilder:
    """
    Build the platform bootstrap payload.
    """

    def build(
        self,
        *,
        context: PlatformBootstrapContext,
        modules: list[PlatformModule],
        navigation: list[NavigationItem],
        dashboard: list[DashboardCard],
        branding: dict[str, object],
        feature_flags: dict[str, bool],
        subscription: dict[str, object] | None = None,
        preferences: dict[str, object] | None = None,
    ) -> PlatformBootstrap:
        """
        Build the bootstrap payload.
        """

        subscription = {} if subscription is None else subscription

        preferences = {} if preferences is None else preferences

        return PlatformBootstrap(
            context=context,
            modules=modules,
            navigation=navigation,
            dashboard=dashboard,
            branding=branding,
            feature_flags=feature_flags,
            subscription=subscription,
            preferences=preferences,
        )


platform_bootstrap_builder = PlatformBootstrapBuilder()


__all__ = [
    "PlatformBootstrap",
    "PlatformBootstrapBuilder",
    "platform_bootstrap_builder",
]
