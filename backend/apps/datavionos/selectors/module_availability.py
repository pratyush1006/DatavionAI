"""
Tenant aware module availability selector.

Resolution order:

Module Registry
        |
        v
Tenant Type Eligibility
        |
        v
Subscription Entitlements
        |
        v
Available DatavionOS Modules
"""

from __future__ import annotations

from apps.datavionos.contracts.module import (
    ModuleContract,
)
from apps.datavionos.registries.module import (
    module_registry,
)
from apps.platform.subscriptions.models import (
    ModuleEntitlement,
)


class ModuleAvailabilitySelector:
    """
    Resolve modules available for a tenant.

    This selector is responsible for
    tenant runtime module availability.

    It does NOT handle:
    - permissions
    - feature flags
    - navigation
    - dashboard rendering
    """

    def get(
        self,
        *,
        tenant,
    ) -> list[ModuleContract]:
        """
        Return available modules for tenant.
        """

        if tenant is None:
            return []

        modules = [
            module
            for module in module_registry.enabled_modules()
            if self._allowed_for_tenant_type(
                module=module,
                tenant_type=tenant.tenant_type,
            )
        ]

        entitled_modules = self._get_subscription_modules(
            tenant=tenant,
        )

        return sorted(
            [module for module in modules if module.identifier in entitled_modules],
            key=lambda module: module.order,
        )

    def _allowed_for_tenant_type(
        self,
        *,
        module: ModuleContract,
        tenant_type: str,
    ) -> bool:
        """
        Validate tenant type compatibility.
        """

        if not module.tenant_scoped:
            return True

        allowed_types = module.metadata.get(
            "tenant_types",
            [],
        )

        if not allowed_types:
            return True

        return tenant_type in allowed_types

    def _get_subscription_modules(
        self,
        *,
        tenant,
    ) -> set[str]:
        """
        Resolve subscription module entitlements.
        """

        subscription = getattr(
            tenant,
            "subscription",
            None,
        )

        #
        # Development fallback.
        #
        # Replace with strict denial
        # when billing enforcement starts.
        #
        if subscription is None:
            return {module.identifier for module in module_registry.enabled_modules()}

        return set(
            ModuleEntitlement.objects.filter(
                plan=subscription.plan,
                enabled=True,
            ).values_list(
                "module_identifier",
                flat=True,
            )
        )


module_availability_selector = ModuleAvailabilitySelector()


__all__ = (
    "ModuleAvailabilitySelector",
    "module_availability_selector",
)
