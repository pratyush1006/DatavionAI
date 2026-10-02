"""
DatavionOS bootstrap service.

Kernel orchestration layer for runtime initialization.

Responsibilities:

- Resolve tenant context
- Resolve organization context
- Resolve SaaS entitlements
- Resolve tenant-aware module availability
- Build navigation
- Build dashboard
- Resolve branding
- Return immutable bootstrap result

Architecture:

Tenant
   |
Organization
   |
DatavionOS Bootstrap Kernel
   |
   +--> Entitlement Resolver
   |
   +--> Module Availability Selector
   |       |
   |       +--> Module Registry
   |       +--> Tenant Eligibility
   |       +--> SaaS Module Entitlements
   |
   +--> Navigation Builder
   |
   +--> Dashboard Builder
   |
   +--> Branding Resolver
   |
   v
Platform Bootstrap Result

Domain logic stays inside domain services/selectors/builders.

This service intentionally does not query:

- Subscription models
- Module entitlement models
- Module registry internals
- Billing databases
- Tenant databases

Those responsibilities belong to their respective layers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from apps.datavionos.builders.dashboard import (
    DashboardBuilder,
    DashboardCard,
)
from apps.datavionos.builders.navigation import (
    NavigationBuilder,
    NavigationItem,
)
from apps.datavionos.registries.module import (
    module_registry,
)
from apps.datavionos.resolvers.branding import (
    BrandingResolver,
)
from apps.datavionos.selectors.module_availability import (
    CORE_ORGANIZATION_MODULES,
    ModuleAvailabilitySelector,
    module_availability_selector,
)
from apps.datavionos.services.effective_capability import (
    EffectiveCapabilityContext,
    build_effective_capability_context,
)
from apps.datavionos.services.saas_capability_control_plane import (
    SaaSCapabilityProvider,
    get_provider,
)


@dataclass(
    slots=True,
    frozen=True,
)
class PlatformBootstrapResult:
    """
    Immutable result returned by DatavionOS bootstrap.

    The result contains already-resolved runtime data and does not
    perform additional business-logic resolution.
    """

    tenant: Any

    organization: Any | None = None

    branding: dict[str, Any] | None = None

    feature_flags: dict[str, bool] | None = None

    navigation: list[NavigationItem] | None = None

    dashboard: list[DashboardCard] | None = None

    modules: list[Any] | None = None

    capabilities: dict[str, Any] | None = None


class PlatformBootstrapService:
    """
    DatavionOS kernel bootstrap orchestrator.

    Converts tenant context and SaaS entitlement capabilities into
    the runtime platform configuration consumed by the frontend.

    Resolution flow:

        tenant
          |
          +--> organization
          |
          +--> entitlement capabilities
          |
          +--> module availability
          |
          +--> navigation
          |
          +--> dashboard
          |
          +--> branding
          |
          v
        bootstrap result
    """

    def __init__(
        self,
        *,
        module_selector: ModuleAvailabilitySelector | None = None,
        navigation_builder: NavigationBuilder | None = None,
        dashboard_builder: DashboardBuilder | None = None,
        branding_resolver: BrandingResolver | None = None,
    ) -> None:
        """
        Initialize bootstrap orchestration dependencies.

        Dependencies are injectable to keep the orchestration layer
        testable without changing runtime behavior.
        """

        self._module_selector = module_selector or module_availability_selector

        self._navigation_builder = navigation_builder or NavigationBuilder()

        self._dashboard_builder = dashboard_builder or DashboardBuilder()

        self._branding_resolver = branding_resolver or BrandingResolver()

    # ==================================================================
    # Bootstrap
    # ==================================================================

    def bootstrap(
        self,
        *,
        tenant: Any,
        user: Any | None = None,
        organization: Any | None = None,
        permissions: set[str] | frozenset[str] | None = None,
        roles: set[str] | frozenset[str] | None = None,
        access_scope: dict[str, tuple[str, ...]] | None = None,
        is_platform_administrator: bool = False,
    ) -> PlatformBootstrapResult:
        """
        Bootstrap the DatavionOS runtime.

        Resolution order:

        1. Validate runtime tenant context
        2. Resolve SaaS capabilities
        3. Resolve tenant-aware modules
        4. Resolve feature flags
        5. Build navigation
        6. Build dashboard
        7. Resolve branding
        8. Return immutable bootstrap result

        Subscription and billing rules are delegated to
        EntitlementResolver.

        Module entitlement resolution is performed once and the
        resulting capability snapshot is passed into
        ModuleAvailabilitySelector.
        """

        self._bootstrap_rbac(
            tenant,
        )

        resolved_permissions = self._resolve_permissions(
            permissions,
        )

        capabilities = self._resolve_capabilities(
            user=user,
            organization=organization,
        )

        departments: set[str] = set()
        ai_capabilities: dict[str, bool] = {}
        if organization is not None:
            capabilities = dict(capabilities)
            capabilities["modules"] = (
                SaaSCapabilityProvider.resolve_organization_modules(
                    organization=organization,
                    entitled_modules=capabilities.get("modules", {}),
                )
            )
            # Core organization administration is available for every
            # organization and must also be present in the effective context;
            # navigation and dashboard builders fail closed against it.
            capabilities["modules"] = {
                **capabilities["modules"],
                **dict.fromkeys(CORE_ORGANIZATION_MODULES, True),
            }
            capabilities["features"] = (
                SaaSCapabilityProvider.resolve_organization_features(
                    organization=organization,
                    entitled_features=capabilities.get("features", {}),
                )
            )
            departments, ai_capabilities = (
                SaaSCapabilityProvider.resolve_organization_scopes(
                    organization=organization,
                    entitled_modules=capabilities.get("modules", {}),
                    entitled_features=capabilities.get("features", {}),
                )
            )

        # A platform administrator is a control-plane role.  It can inspect
        # every active product module regardless of the selected
        # organization's plan or tenant type. Endpoint authorization remains
        # enforced by the normal RBAC permission checks.
        if is_platform_administrator:
            available_modules = module_registry.available_modules()
            capabilities = dict(capabilities)
            capabilities["modules"] = {
                module.identifier: True for module in available_modules
            }
            capabilities["features"] = {
                feature: True
                for module in available_modules
                for feature in module.feature_flags
            }

        feature_flags = self._bootstrap_feature_flags(
            capabilities,
        )

        effective_context = build_effective_capability_context(
            user_id=str(getattr(user, "id", "")) or None,
            organization_id=getattr(
                organization,
                "id",
                None,
            ),
            tenant_id=getattr(
                tenant,
                "id",
                None,
            ),
            modules=capabilities.get(
                "modules",
                {},
            ),
            features=feature_flags,
            permissions=resolved_permissions,
            roles=set(roles or set()),
            departments=departments,
            data_scopes=dict(access_scope or {}),
            ai_capabilities=ai_capabilities,
            limits=capabilities.get(
                "limits",
                {},
            ),
        )

        modules = (
            list(module_registry.available_modules())
            if is_platform_administrator
            else self._bootstrap_modules(
                tenant=tenant,
                capabilities=capabilities,
            )
        )

        navigation = self._bootstrap_navigation(
            modules=modules,
            permissions=resolved_permissions,
            feature_flags=feature_flags,
            effective_context=effective_context,
        )

        dashboard = self._bootstrap_dashboard(
            modules=modules,
            permissions=resolved_permissions,
            feature_flags=feature_flags,
            effective_context=effective_context,
        )

        branding = self._bootstrap_branding(
            organization=organization,
        )

        return PlatformBootstrapResult(
            tenant=tenant,
            organization=organization,
            branding=branding,
            feature_flags=feature_flags,
            navigation=navigation,
            dashboard=dashboard,
            modules=modules,
            capabilities=capabilities,
        )

    # ==================================================================
    # Permissions
    # ==================================================================

    @staticmethod
    def _resolve_permissions(
        permissions: set[str] | frozenset[str] | None,
    ) -> set[str]:
        """
        Normalize effective runtime permissions.

        RBAC resolution belongs to PlatformBootstrapSelector.

        The bootstrap service only consumes the already-resolved
        permission set.
        """

        if permissions is None:
            return set()

        return set(
            permissions,
        )

    # ==================================================================
    # SaaS Entitlements
    # ==================================================================

    @staticmethod
    @staticmethod
    def _resolve_capabilities(
        *,
        user: Any | None,
        organization: Any | None,
    ) -> dict[str, Any]:
        """Resolve the canonical effective SaaS capability snapshot."""
        if organization is None:
            return {
                "modules": {},
                "features": {},
                "permissions": set(),
                "limits": {},
                "capabilities": {},
            }

        snapshot = get_provider().resolve(
            user=user,
            organization=organization,
        )

        return {
            "modules": dict(snapshot.modules),
            "features": dict(snapshot.features),
            "permissions": set(snapshot.permissions),
            "limits": {},
            "capabilities": {},
        }

    # ==================================================================
    # RBAC
    # ==================================================================

    def _bootstrap_rbac(
        self,
        tenant: Any,
    ) -> None:
        """
        Initialize tenant RBAC integration.

        RBAC resolution remains inside PlatformBootstrapSelector
        and the platform RBAC domain.

        This hook intentionally performs no resolution itself.
        """

        return

    # ==================================================================
    # Branding
    # ==================================================================

    def _bootstrap_branding(
        self,
        organization: Any | None,
    ) -> dict[str, Any]:
        """
        Resolve organization branding.

        Branding resolution is delegated to BrandingResolver.

        The resolver owns the branding defaults and organization-specific
        branding policy. The bootstrap service only orchestrates it.
        """

        branding = self._branding_resolver.resolve(
            organization=organization,
        )

        if not isinstance(
            branding,
            dict,
        ):
            return {}

        return dict(
            branding,
        )

    # ==================================================================
    # Feature Flags
    # ==================================================================

    @staticmethod
    def _bootstrap_feature_flags(
        capabilities: dict[str, Any],
    ) -> dict[str, bool]:
        """
        Resolve enabled runtime feature flags.

        Missing or malformed feature payloads fail closed.
        """

        features = capabilities.get(
            "features",
            {},
        )

        if not isinstance(
            features,
            dict,
        ):
            return {}

        return {str(feature): bool(enabled) for feature, enabled in features.items()}

    # ==================================================================
    # Modules
    # ==================================================================

    def _bootstrap_modules(
        self,
        *,
        tenant: Any,
        capabilities: dict[str, Any],
    ) -> list[Any]:
        """
        Resolve tenant-aware runtime modules.

        Flow:

            SaaS EntitlementResolver
                        |
                        v
                    capabilities
                        |
                        v
            ModuleAvailabilitySelector
                        |
                  +-----+-----+
                  |           |
            ModuleRegistry  Tenant Type
                  |           |
                  +-----+-----+
                        |
                        v
                  ModuleContract[]
        """

        if tenant is None:
            return []

        return self._module_selector.get(
            tenant=tenant,
            capabilities=capabilities,
        )

    # ==================================================================
    # Navigation
    # ==================================================================

    def _bootstrap_navigation(
        self,
        *,
        modules: list[Any],
        permissions: set[str],
        feature_flags: dict[str, bool],
        effective_context: EffectiveCapabilityContext,
    ) -> list[NavigationItem]:
        """
        Build runtime navigation.

        NavigationBuilder receives only already-resolved runtime
        modules and access context.

        It does not perform subscription or billing resolution.
        """

        return self._navigation_builder.build(
            modules=modules,
            permissions=permissions,
            feature_flags=feature_flags,
            effective_context=effective_context,
        )

    # ==================================================================
    # Dashboard
    # ==================================================================

    def _bootstrap_dashboard(
        self,
        *,
        modules: list[Any],
        permissions: set[str],
        feature_flags: dict[str, bool],
        effective_context: EffectiveCapabilityContext,
    ) -> list[DashboardCard]:
        """
        Build runtime dashboard.

        DashboardBuilder receives only already-resolved runtime
        modules and access context.

        It does not perform subscription or billing resolution.
        """

        return self._dashboard_builder.build(
            modules=modules,
            permissions=permissions,
            feature_flags=feature_flags,
            effective_context=effective_context,
        )


__all__ = (
    "PlatformBootstrapResult",
    "PlatformBootstrapService",
)
