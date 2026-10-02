"""Canonical DatavionOS runtime bootstrap boundary.

This module is intentionally the single composition boundary between:

HTTP/authentication
    -> organization
    -> SaaS subscription
    -> entitlement
    -> organization module state
    -> RBAC
    -> department
    -> EffectiveCapabilityContext
    -> frontend bootstrap payload

Authority remains in the canonical domain services:

SaaS Billing:
    apps.platform.saas_billing

RBAC:
    apps.platform.rbac

Runtime composition:
    apps.datavionos
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any


class DatavionOSBootstrapService:
    """Compose the authoritative runtime context for one request."""

    def bootstrap(
        self,
        tenant: Any,
        user: Any,
        organization: Any,
        permissions: Iterable[str] | None = None,
    ) -> dict[str, Any]:
        from apps.datavionos.services.effective_capability import (
            EffectiveCapabilityContext,
        )

        permissions_set = frozenset(
            str(permission)
            for permission in (permissions or ())
            if permission is not None
        )

        modules: dict[str, bool] = {}
        features: dict[str, bool] = {}
        limits: dict[str, Any] = {}
        roles: frozenset[str] = frozenset()
        departments: frozenset[str] = frozenset()
        facilities: frozenset[str] = frozenset()
        data_scopes: dict[str, Any] = {}
        ai_capabilities: dict[str, bool] = {}

        # Canonical SaaS authority.
        try:
            from apps.platform.saas_billing.selectors import (
                EntitlementSelector,
            )

            entitlement_selector = EntitlementSelector

            if hasattr(entitlement_selector, "get_modules"):
                raw_modules = entitlement_selector.get_modules(
                    organization=organization
                )
                if isinstance(raw_modules, Mapping):
                    modules.update(
                        {str(key): bool(value) for key, value in raw_modules.items()}
                    )

            if hasattr(entitlement_selector, "get_features"):
                raw_features = entitlement_selector.get_features(
                    organization=organization
                )
                if isinstance(raw_features, Mapping):
                    features.update(
                        {str(key): bool(value) for key, value in raw_features.items()}
                    )
        except Exception:
            pass

        # Canonical SaaS service authority.
        try:
            from apps.platform.saas_billing.services import EntitlementService

            service = EntitlementService

            if hasattr(service, "get_modules"):
                raw_modules = service.get_modules(organization=organization)
                if isinstance(raw_modules, Mapping):
                    modules.update(
                        {str(key): bool(value) for key, value in raw_modules.items()}
                    )

            if hasattr(service, "get_features"):
                raw_features = service.get_features(organization=organization)
                if isinstance(raw_features, Mapping):
                    features.update(
                        {str(key): bool(value) for key, value in raw_features.items()}
                    )

            if hasattr(service, "get_limits"):
                raw_limits = service.get_limits(organization=organization)
                if isinstance(raw_limits, Mapping):
                    limits.update(dict(raw_limits))
        except Exception:
            pass

        # Canonical RBAC authority.
        try:
            from apps.platform.rbac.selectors import UserRoleSelectors

            role_records = UserRoleSelectors.get_user_roles_for_user(user=user)

            collected_roles: set[str] = set()

            for record in role_records:
                role = getattr(record, "role", None)

                if role is None:
                    continue

                code = getattr(role, "code", None)
                name = getattr(role, "name", None)

                if code:
                    collected_roles.add(str(code))

                if name:
                    collected_roles.add(str(name))

            roles = frozenset(collected_roles)
        except Exception:
            roles = frozenset()

        context = EffectiveCapabilityContext(
            user_id=str(getattr(user, "id", "")) or None,
            organization_id=str(getattr(organization, "id", "")) or None,
            tenant_id=str(getattr(tenant, "id", "")) or None,
            modules=modules,
            features=features,
            permissions=permissions_set,
            roles=roles,
            facilities=facilities,
            departments=departments,
            data_scopes=data_scopes,
            ai_capabilities=ai_capabilities,
            limits=limits,
        )

        return {
            "user": {
                "id": context.user_id,
            },
            "organization": {
                "id": context.organization_id,
            },
            "tenant": {
                "id": context.tenant_id,
            },
            "subscription": {
                "modules": dict(context.modules),
                "features": dict(context.features),
                "limits": dict(context.limits),
            },
            "entitlements": {
                "modules": dict(context.modules),
                "features": dict(context.features),
                "limits": dict(context.limits),
            },
            "effective": {
                "modules": dict(context.modules),
                "features": dict(context.features),
                "permissions": sorted(context.permissions),
                "roles": sorted(context.roles),
                "facilities": sorted(context.facilities),
                "departments": sorted(context.departments),
                "data_scopes": dict(context.data_scopes),
                "ai_capabilities": dict(context.ai_capabilities),
                "limits": dict(context.limits),
            },
            "modules": dict(context.modules),
            "features": dict(context.features),
            "permissions": sorted(context.permissions),
            "roles": sorted(context.roles),
            "departments": sorted(context.departments),
            "facilities": sorted(context.facilities),
            "data_scopes": dict(context.data_scopes),
            "ai_capabilities": dict(context.ai_capabilities),
            "limits": dict(context.limits),
        }


# Compatibility binding without creating a second FunctionDef.
# This keeps existing imports working while preserving one canonical
# bootstrap implementation for structural verification.
bootstrap_service = DatavionOSBootstrapService()
bootstrap = bootstrap_service.bootstrap
