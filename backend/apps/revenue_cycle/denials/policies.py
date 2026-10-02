"""Authorization policies for Denials."""

from __future__ import annotations

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
    DENIALS_CREATE,
    DENIALS_DELETE,
    DENIALS_LIST,
    DENIALS_RESTORE,
    DENIALS_TRANSITION,
    DENIALS_UPDATE,
)


def _allowed(*, actor, organization, permission: str) -> bool:
    """Check platform RBAC for the organization."""
    return bool(
        organization
        and _has_permission(
            user=actor, permission=permission, organization=organization
        )
    )


def can_list(*, actor, organization) -> bool:
    """Authorize listing."""
    return _allowed(actor=actor, organization=organization, permission=DENIALS_LIST)


def can_create(*, actor, organization) -> bool:
    """Authorize creation."""
    return _allowed(actor=actor, organization=organization, permission=DENIALS_CREATE)


def can_update(*, actor, organization) -> bool:
    """Authorize updates."""
    return _allowed(actor=actor, organization=organization, permission=DENIALS_UPDATE)


def can_delete(*, actor, organization) -> bool:
    """Authorize deletion."""
    return _allowed(actor=actor, organization=organization, permission=DENIALS_DELETE)


def can_restore(*, actor, organization) -> bool:
    """Authorize restoration."""
    return _allowed(actor=actor, organization=organization, permission=DENIALS_RESTORE)


def can_transition(*, actor, organization) -> bool:
    """Authorize lifecycle transitions."""
    return _allowed(
        actor=actor, organization=organization, permission=DENIALS_TRANSITION
    )


__all__ = (
    "can_list",
    "can_create",
    "can_update",
    "can_delete",
    "can_restore",
    "can_transition",
)
