from __future__ import annotations

from apps.datavionos.services.canonical_intersection import apply_canonical_intersection

"Canonical backend Effective Capability Context.\n\nThis module is the composition boundary for dynamic SaaS capabilities.\nDomain services remain authoritative for their own facts: SaaS entitlement,\norganization module/feature state, RBAC, data scope, and AI ownership.\n"
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from apps.platform.rbac.selectors.user_role import get_user_roles_for_user
from apps.platform.saas_billing.selectors.subscription_selector import (
    SubscriptionSelector,
)
from apps.platform.saas_billing.services.entitlement_service import EntitlementService


@dataclass(frozen=True, slots=True)
class EffectiveCapabilityContext:
    """Immutable effective capability state for one authenticated request."""

    user_id: str | None
    organization_id: str | None
    tenant_id: str | None
    modules: Mapping[str, bool] = field(default_factory=dict)
    features: Mapping[str, bool] = field(default_factory=dict)
    permissions: frozenset[str] = frozenset()
    roles: frozenset[str] = frozenset()
    facilities: frozenset[str] = frozenset()
    departments: frozenset[str] = frozenset()
    data_scopes: Mapping[str, Any] = field(default_factory=dict)
    ai_capabilities: Mapping[str, bool] = field(default_factory=dict)
    limits: Mapping[str, Any] = field(default_factory=dict)

    def module_enabled(self, key: str) -> bool:
        return bool(self.modules.get(key, False))

    def feature_enabled(self, key: str) -> bool:
        return bool(self.features.get(key, False))

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions

    def has_any_permission(self, permissions: set[str] | frozenset[str]) -> bool:
        return bool(self.permissions.intersection(permissions))

    def has_all_permissions(self, permissions: set[str] | frozenset[str]) -> bool:
        return permissions.issubset(self.permissions)

    def ai_enabled(self, key: str) -> bool:
        return bool(self.ai_capabilities.get(key, False))

    def can_access_module(self, module: str, permission: str | None = None) -> bool:
        if not self.module_enabled(module):
            return False
        return permission is None or self.has_permission(permission)

    def as_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "organization_id": self.organization_id,
            "tenant_id": self.tenant_id,
            "modules": dict(self.modules),
            "features": dict(self.features),
            "permissions": sorted(self.permissions),
            "roles": sorted(self.roles),
            "facilities": sorted(self.facilities),
            "departments": sorted(self.departments),
            "data_scopes": dict(self.data_scopes),
            "ai_capabilities": dict(self.ai_capabilities),
            "limits": dict(self.limits),
        }


def build_effective_capability_context(
    *,
    user_id: str | None,
    organization_id: str | None,
    tenant_id: str | None,
    modules: Mapping[str, bool] | None = None,
    features: Mapping[str, bool] | None = None,
    permissions: set[str] | frozenset[str] | None = None,
    roles: set[str] | frozenset[str] | None = None,
    facilities: set[str] | frozenset[str] | None = None,
    departments: set[str] | frozenset[str] | None = None,
    data_scopes: Mapping[str, Any] | None = None,
    ai_capabilities: Mapping[str, bool] | None = None,
    limits: Mapping[str, Any] | None = None,
) -> EffectiveCapabilityContext:
    """Normalize already-resolved domain facts into one backend context."""
    return apply_canonical_intersection(
        EffectiveCapabilityContext(
            user_id=user_id,
            organization_id=organization_id,
            tenant_id=tenant_id,
            modules=dict(modules or {}),
            features=dict(features or {}),
            permissions=frozenset(permissions or set()),
            roles=frozenset(roles or set()),
            facilities=frozenset(facilities or set()),
            departments=frozenset(departments or set()),
            data_scopes=dict(data_scopes or {}),
            ai_capabilities=dict(ai_capabilities or {}),
            limits=dict(limits or {}),
        )
    )


def _datavionos_get_active_subscription(organization):
    """Return the canonical active subscription."""
    return SubscriptionSelector.get_active_subscription(organization=organization)


def _datavionos_get_enabled_modules(organization):
    """Return canonical SaaS-enabled modules."""
    return EntitlementService.get_enabled_modules(organization=organization)


def _datavionos_get_entitlement_snapshot(organization):
    """Return canonical SaaS entitlement snapshot."""
    return EntitlementService.get_snapshot(organization=organization)


def _datavionos_get_user_roles(user):
    """Return canonical UserRole assignments."""
    return get_user_roles_for_user(user=user)


def _datavionos_get_active_roles(user):
    """
    Resolve active canonical Role records assigned to the user.
    """
    assignments = _datavionos_get_user_roles(user)
    roles = []
    for assignment in assignments:
        if not getattr(assignment, "is_active", True):
            continue
        role = getattr(assignment, "role", None)
        if role is None:
            continue
        if not getattr(role, "is_active", True):
            continue
        roles.append(role)
    return roles


def _datavionos_get_role_codes(user):
    """Return active canonical role codes."""
    return frozenset(
        str(role.code)
        for role in _datavionos_get_active_roles(user)
        if getattr(role, "code", None)
    )


def _datavionos_build_subscription_authority(organization):
    """
    Build subscription authority context.

    Subscription remains the SaaS billing authority.
    """
    subscription = _datavionos_get_active_subscription(organization)
    if subscription is None:
        return {
            "active": False,
            "subscription_id": None,
            "plan_id": None,
            "plan_code": None,
            "modules": {},
            "enabled_modules": [],
        }
    plan = getattr(subscription, "plan", None)
    enabled_modules = _datavionos_get_enabled_modules(organization)
    return {
        "active": True,
        "subscription_id": str(getattr(subscription, "id", "")),
        "plan_id": str(getattr(plan, "id", "")) if plan is not None else None,
        "plan_code": getattr(plan, "code", None) if plan is not None else None,
        "modules": {str(module): True for module in enabled_modules},
        "enabled_modules": list(enabled_modules),
    }


def _datavionos_build_rbac_authority(user):
    """
    Build RBAC authority context.

    Role and permission authority remains in the canonical RBAC
    application.
    """
    roles = _datavionos_get_active_roles(user)
    return {
        "roles": frozenset(
            str(role.code) for role in roles if getattr(role, "code", None)
        ),
        "role_ids": frozenset(
            str(role.id) for role in roles if getattr(role, "id", None)
        ),
    }


def _datavionos_build_canonical_authority_context(*, user, organization):
    """
    Compose canonical SaaS Billing + RBAC authority.

    This function intentionally does not decide dashboard layout.
    Dashboard/navigation remain downstream consumers of the effective
    capability context.
    """
    return {
        "subscription": _datavionos_build_subscription_authority(organization),
        "rbac": _datavionos_build_rbac_authority(user),
    }
