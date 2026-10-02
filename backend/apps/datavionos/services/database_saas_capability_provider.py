from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.datavionos.resolvers.entitlement import EntitlementResolver
from apps.datavionos.resolvers.permissions import PermissionResolver
from apps.platform.organizations.models import OrganizationFeature, OrganizationModule
from apps.platform.organizations.selectors.organization_module import (
    get_organization_modules,
)


def _code(value: object) -> str:
    return str(value or "").strip().lower()


def _enabled(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, Mapping):
        for key in ("enabled", "active", "included", "purchased"):
            if key in value:
                return bool(value[key])
        return str(value.get("status", "")).strip().lower() in {
            "enabled",
            "active",
            "included",
            "purchased",
            "trial",
        }
    if isinstance(value, str):
        return value.strip().lower() in {
            "true",
            "1",
            "enabled",
            "active",
            "included",
            "purchased",
            "trial",
        }
    return bool(value)


def _capability_map(value: object) -> dict[str, bool]:
    if not isinstance(value, Mapping):
        return {}
    result: dict[str, bool] = {}
    for key, item in value.items():
        code = _code(key)
        if code:
            result[code] = _enabled(item)
    return result


class DatabaseSaaSCapabilityProvider:
    """Compose subscription, organization overrides and RBAC."""

    def resolve(self, *, user: Any, organization: Any) -> dict[str, Any]:
        entitlement = EntitlementResolver.resolve(organization=organization)
        purchased_modules = _capability_map(entitlement.get("modules", {}))
        purchased_features = _capability_map(entitlement.get("features", {}))

        module_overrides: dict[str, bool] = {}
        for assignment in get_organization_modules(organization, enabled_only=False):
            code = _code(getattr(assignment, "module_code", ""))
            if code:
                module_overrides[code] = (
                    assignment.status == OrganizationModule.Status.ENABLED
                )

        effective_modules = {
            code: purchased and module_overrides.get(code, True)
            for code, purchased in purchased_modules.items()
        }

        feature_overrides: dict[str, bool] = {}
        rows = OrganizationFeature.objects.filter(
            organization=organization
        ).values_list("feature_code", "status")
        for feature_code, status in rows:
            code = _code(feature_code)
            if code:
                feature_overrides[code] = (
                    status == OrganizationFeature.FeatureStatus.ENABLED
                )

        effective_features = {
            code: purchased and feature_overrides.get(code, True)
            for code, purchased in purchased_features.items()
        }

        permissions = frozenset(
            PermissionResolver().resolve(user=user, organization=organization)
        )
        limits = entitlement.get("limits", {})
        if not isinstance(limits, Mapping):
            limits = {}

        return {
            "modules": effective_modules,
            "features": effective_features,
            "permissions": permissions,
            "limits": dict(limits),
            "user_id": str(getattr(user, "pk", "")),
            "organization_id": str(getattr(organization, "pk", "")),
            "tenant_id": str(getattr(organization, "tenant_id", "")),
        }


def register_database_provider() -> None:
    from apps.datavionos.services.saas_capability_control_plane import (
        SaaSCapabilitySnapshot,
        register_provider,
    )

    provider = DatabaseSaaSCapabilityProvider()

    class Adapter:
        def resolve(self, *, user: Any, organization: Any) -> SaaSCapabilitySnapshot:
            payload = provider.resolve(user=user, organization=organization)
            return SaaSCapabilitySnapshot(
                modules=payload["modules"],
                features=payload["features"],
                permissions=payload["permissions"],
                tenant_id=payload["tenant_id"],
                organization_id=payload["organization_id"],
                user_id=payload["user_id"],
            )

    register_provider(Adapter())
