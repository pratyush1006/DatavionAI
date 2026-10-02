"""
DatavionOS tenant-aware module availability selector.

Resolution order:

Module Registry
        |
        v
Tenant Type Eligibility
        |
        v
Resolved SaaS Entitlements
        |
        v
Available DatavionOS Modules

Responsibilities
----------------
This selector determines which registered DatavionOS modules are available
to a tenant at runtime.

It is responsible for:

- Platform module availability
- Tenant-type compatibility
- Resolved SaaS module entitlement
- Deterministic module ordering

It does NOT handle:

- RBAC permissions
- Feature flags
- Navigation visibility
- Dashboard rendering
- Module lifecycle management
- Subscription business logic
- Subscription database queries

Architecture
------------
ModuleRegistry owns module definitions.

PlatformBootstrapService resolves SaaS capabilities once through
EntitlementResolver and passes the immutable runtime capability snapshot
into this selector.

ModuleAvailabilitySelector combines:

    ModuleRegistry
          +
    Tenant Type Eligibility
          +
    Resolved SaaS Module Entitlements

into the tenant-scoped runtime module set.

Security model
--------------
No tenant
    -> no modules

Missing tenant type
    -> no modules

Missing organization
    -> no modules

Missing capabilities
    -> no modules

Missing module entitlement
    -> module unavailable

Unavailable module
    -> module unavailable

Tenant-type mismatch
    -> module unavailable

This selector intentionally fails closed.
"""

from __future__ import annotations

from typing import Any

from apps.datavionos.contracts.module import (
    ModuleContract,
)
from apps.datavionos.registries.module import (
    module_registry,
)

# Every tenant needs these organization-management capabilities before any
# clinical or commercial module can operate. They are platform fundamentals,
# not optional paid-plan add-ons.
CORE_ORGANIZATION_MODULES = frozenset({"departments", "employees", "teams"})


class ModuleAvailabilitySelector:
    """
    Resolve modules available to a tenant.

    Availability is determined by:

    1. Module registry availability
    2. Tenant-type compatibility
    3. Already-resolved SaaS module entitlement

    Subscription business rules remain inside the entitlement layer.

    This selector must not perform SaaS subscription queries.
    """

    def get(
        self,
        *,
        tenant: Any,
        capabilities: dict[str, Any] | None = None,
    ) -> list[ModuleContract]:
        """
        Return modules available to the supplied tenant.

        The supplied capability snapshot must already have been resolved
        by the bootstrap orchestration layer.

        The result contains only modules that:

        - are registered
        - are enabled and active
        - are compatible with the tenant type
        - are enabled by the resolved SaaS entitlement snapshot

        Modules are returned in deterministic runtime order.
        """

        if tenant is None:
            return []

        tenant_type = getattr(
            tenant,
            "tenant_type",
            None,
        )

        if tenant_type is None:
            return []

        organization = self._get_organization(
            tenant=tenant,
        )

        if organization is None:
            return []

        if not isinstance(
            capabilities,
            dict,
        ):
            return []

        entitled_modules = self._get_entitled_modules(
            capabilities=capabilities,
        )

        if not entitled_modules:
            return []

        available_modules = module_registry.available_modules()

        if not available_modules:
            return []

        modules: list[ModuleContract] = []

        for module in available_modules:
            if not self._allowed_for_tenant_type(
                module=module,
                tenant_type=tenant_type,
            ):
                continue

            if (
                self._normalize_value(
                    module.identifier,
                )
                not in entitled_modules
            ):
                continue

            modules.append(
                module,
            )

        return sorted(
            modules,
            key=lambda module: (
                module.order,
                module.identifier,
            ),
        )

    # ==================================================================
    # Organization Resolution
    # ==================================================================

    @staticmethod
    def _get_organization(
        *,
        tenant: Any,
    ) -> Any | None:
        """
        Resolve the organization associated with the tenant.

        DatavionOS organizations use the reverse Django relation:

            tenant.organizations

        The selector supports a direct ``organization`` attribute as a
        compatibility path, but prefers the canonical reverse relation.

        Organization resolution is intentionally limited to the tenant
        relationship. No organization is inferred from unrelated data.
        """

        organization = getattr(
            tenant,
            "organization",
            None,
        )

        if organization is not None:
            return organization

        organizations = getattr(
            tenant,
            "organizations",
            None,
        )

        if organizations is None:
            return None

        try:
            return organizations.first()
        except (
            AttributeError,
            TypeError,
        ):
            return None

    # ==================================================================
    # SaaS Entitlements
    # ==================================================================

    @staticmethod
    def _get_entitled_modules(
        *,
        capabilities: dict[str, Any],
    ) -> set[str]:
        """
        Resolve enabled module identifiers from the already-resolved
        SaaS capability snapshot.

        Expected capability shape:

            {
                "modules": {
                    "patients": True,
                    "appointments": True,
                    "ai_assistant": False,
                },
                ...
            }

        This method intentionally performs no database access and does
        not invoke EntitlementResolver again.

        Subscription lifecycle, plan resolution, snapshots, and billing
        rules remain outside this selector.
        """

        modules = capabilities.get(
            "modules",
            {},
        )

        if not isinstance(
            modules,
            dict,
        ):
            return set()

        return {
            ModuleAvailabilitySelector._normalize_value(
                module_identifier,
            )
            for module_identifier, enabled in modules.items()
            if bool(enabled)
        } | CORE_ORGANIZATION_MODULES

    # ==================================================================
    # Tenant Eligibility
    # ==================================================================

    @staticmethod
    def _allowed_for_tenant_type(
        *,
        module: ModuleContract,
        tenant_type: Any,
    ) -> bool:
        """
        Determine whether a module is compatible with the tenant type.

        Non-tenant-scoped modules are available to every tenant type,
        subject to module availability and SaaS entitlement.

        Tenant-scoped modules may optionally declare supported tenant
        types through module metadata:

            metadata={
                "tenant_types": [
                    "hospital",
                    "clinic",
                ],
            }

        When no tenant types are declared, the module is considered
        compatible with all tenant types.
        """

        if not module.tenant_scoped:
            return True

        allowed_types = module.metadata.get(
            "tenant_types",
            (),
        )

        if not allowed_types:
            return True

        normalized_tenant_type = ModuleAvailabilitySelector._normalize_value(
            tenant_type,
        )

        if not normalized_tenant_type:
            return False

        normalized_allowed_types = {
            ModuleAvailabilitySelector._normalize_value(
                allowed_type,
            )
            for allowed_type in allowed_types
        }

        if normalized_tenant_type == "pharmacy":
            healthcare_equivalents = {"clinic", "hospital", "enterprise"}
            if normalized_allowed_types & healthcare_equivalents:
                return True

        return normalized_tenant_type in normalized_allowed_types

    # ==================================================================
    # Normalization
    # ==================================================================

    @staticmethod
    def _normalize_value(
        value: Any,
    ) -> str:
        """
        Normalize enum-backed or string-backed runtime identifiers.
        """

        if value is None:
            return ""

        value = getattr(
            value,
            "value",
            value,
        )

        if not isinstance(
            value,
            str,
        ):
            value = str(
                value,
            )

        return value.strip().lower()


module_availability_selector = ModuleAvailabilitySelector()


__all__ = (
    "ModuleAvailabilitySelector",
    "module_availability_selector",
)
