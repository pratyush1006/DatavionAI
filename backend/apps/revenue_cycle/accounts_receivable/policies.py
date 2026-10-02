"""Authorization policies for Revenue Cycle Accounts Receivable."""

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


from .permissions import ARPermission


class ARPolicy:
    """Evaluate RBAC permissions for Accounts Receivable operations."""

    @staticmethod
    def can_list(*, user: Any, organization: Any) -> bool:
        """Return whether the actor can view AR accounts."""

        return _has_permission(
            user=user,
            permission=ARPermission.LIST,
            organization=organization,
        )

    @staticmethod
    def can_create(*, user: Any, organization: Any) -> bool:
        """Return whether the actor can create AR accounts."""

        return _has_permission(
            user=user,
            permission=ARPermission.CREATE,
            organization=organization,
        )

    @staticmethod
    def can_update(*, user: Any, organization: Any) -> bool:
        """Return whether the actor can update AR accounts."""

        return _has_permission(
            user=user,
            permission=ARPermission.UPDATE,
            organization=organization,
        )

    @staticmethod
    def can_post(*, user: Any, organization: Any) -> bool:
        """Return whether the actor can post AR transactions."""

        return _has_permission(
            user=user,
            permission=ARPermission.POST,
            organization=organization,
        )

    @staticmethod
    def can_reverse(*, user: Any, organization: Any) -> bool:
        """Return whether the actor can reverse AR transactions."""

        return _has_permission(
            user=user,
            permission=ARPermission.REVERSE,
            organization=organization,
        )

    @staticmethod
    def can_write_off(*, user: Any, organization: Any) -> bool:
        """Return whether the actor can write off balances."""

        return _has_permission(
            user=user,
            permission=ARPermission.WRITE_OFF,
            organization=organization,
        )

    @staticmethod
    def can_hold(*, user: Any, organization: Any) -> bool:
        """Return whether the actor can place or release holds."""

        return _has_permission(
            user=user,
            permission=ARPermission.HOLD,
            organization=organization,
        )


__all__ = ("ARPolicy",)
