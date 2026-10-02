"""Authorization policies for Revenue Analytics."""

from __future__ import annotations

from typing import Any

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


from .permissions import RevenueAnalyticsPermission


class RevenueAnalyticsPolicy:
    """Evaluate organization-scoped analytics permissions."""

    @staticmethod
    def can_list(*, user: Any, organization: Any) -> bool:
        """Return whether the actor can list analytics."""

        return _has_permission(
            user=user,
            permission=RevenueAnalyticsPermission.LIST,
            organization=organization,
        )

    @staticmethod
    def can_view(*, user: Any, organization: Any) -> bool:
        """Return whether the actor can view analytics."""

        return _has_permission(
            user=user,
            permission=RevenueAnalyticsPermission.VIEW,
            organization=organization,
        )

    @staticmethod
    def can_generate(*, user: Any, organization: Any) -> bool:
        """Return whether the actor can generate analytics snapshots."""

        return _has_permission(
            user=user,
            permission=RevenueAnalyticsPermission.GENERATE,
            organization=organization,
        )


__all__ = ("RevenueAnalyticsPolicy",)
