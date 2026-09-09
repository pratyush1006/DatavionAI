"""Authorization policies for payment posting."""

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


from .permissions import (
    PAYMENT_POSTING_DELETE,
    PAYMENT_POSTING_READ,
    PAYMENT_POSTING_RESTORE,
    PAYMENT_POSTING_REVERSE,
    PAYMENT_POSTING_WRITE,
)


def _allowed(*, user, organization_id: UUID, permission: str) -> bool:
    """Check organization membership and platform RBAC permission."""

    if not user or not user.is_authenticated:
        return False
    return _has_permission(
        user=user,
        permission=permission,
        organization_id=organization_id,
    )


def can_read(*, user, organization_id: UUID) -> bool:
    """Return whether the actor may read payment postings."""

    return _allowed(
        user=user, organization_id=organization_id, permission=PAYMENT_POSTING_READ
    )


def can_write(*, user, organization_id: UUID) -> bool:
    """Return whether the actor may create or update payment postings."""

    return _allowed(
        user=user, organization_id=organization_id, permission=PAYMENT_POSTING_WRITE
    )


def can_reverse(*, user, organization_id: UUID) -> bool:
    """Return whether the actor may reverse a payment posting."""

    return _allowed(
        user=user, organization_id=organization_id, permission=PAYMENT_POSTING_REVERSE
    )


def can_delete(*, user, organization_id: UUID) -> bool:
    """Return whether the actor may delete a payment posting."""

    return _allowed(
        user=user, organization_id=organization_id, permission=PAYMENT_POSTING_DELETE
    )


def can_restore(*, user, organization_id: UUID) -> bool:
    """Return whether the actor may restore a payment posting."""

    return _allowed(
        user=user, organization_id=organization_id, permission=PAYMENT_POSTING_RESTORE
    )


__all__ = ("can_delete", "can_read", "can_restore", "can_reverse", "can_write")
