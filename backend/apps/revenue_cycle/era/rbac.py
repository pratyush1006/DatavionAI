"""RBAC adapter for ERA."""

from __future__ import annotations

from uuid import UUID

from apps.platform.rbac.resolvers import resolve_permissions


def _has_permission(
    *, user, permission, organization=None, organization_id=None
) -> bool:
    """Evaluate a permission through the canonical platform RBAC resolver."""
    if user is None or not getattr(user, "is_authenticated", True):
        return False

    if organization is None:
        if organization_id is None:
            return False
        from apps.platform.organizations.models import Organization

        organization = Organization.objects.filter(pk=organization_id).first()

    if organization is None:
        return False

    permissions = resolve_permissions(user=user, organization=organization)
    return "*" in permissions or permission in permissions


def has_era_permission(*, user, organization_id: UUID, permission: str) -> bool:
    """Evaluate an ERA permission through the canonical platform engine."""

    if not user or not user.is_authenticated:
        return False
    return _has_permission(
        user=user,
        permission=permission,
        organization_id=organization_id,
    )


__all__ = ("has_era_permission",)
