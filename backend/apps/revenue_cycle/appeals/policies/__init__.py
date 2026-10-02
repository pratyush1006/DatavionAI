"""
Revenue Cycle Appeals authorization policies.
"""

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


from apps.revenue_cycle.appeals.models import Appeal


class AppealPolicy:
    """Centralize organization-scoped appeal authorization."""

    @staticmethod
    def can_list(*, actor: Any, organization: Any) -> bool:
        """Return whether the actor may list appeals."""
        return _has_permission(
            user=actor,
            permission="revenue_cycle.appeals.read",
            organization=organization,
        )

    @staticmethod
    def can_create(*, actor: Any, organization: Any) -> bool:
        """Return whether the actor may create appeals."""
        return _has_permission(
            user=actor,
            permission="revenue_cycle.appeals.manage",
            organization=organization,
        )

    @staticmethod
    def can_mutate(
        *,
        actor: Any,
        organization: Any,
        appeal: Appeal,
    ) -> bool:
        """Return whether the actor may mutate an appeal."""
        return appeal.organization_id == organization.id and _has_permission(
            user=actor,
            permission="revenue_cycle.appeals.manage",
            organization=organization,
        )


__all__ = ("AppealPolicy",)
