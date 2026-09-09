"""Authorization policies for ERA."""

from __future__ import annotations

from uuid import UUID

from .permissions import (
    ERA_DELETE,
    ERA_POST,
    ERA_READ,
    ERA_RESTORE,
    ERA_REVERSE,
    ERA_VALIDATE,
    ERA_WRITE,
)
from .rbac import has_era_permission


def _allowed(*, user, organization_id: UUID, permission: str) -> bool:
    """Check an ERA permission through platform RBAC."""

    return has_era_permission(
        user=user, organization_id=organization_id, permission=permission
    )


def can_read(*, user, organization_id: UUID) -> bool:
    """Return whether the actor may read ERAs."""

    return _allowed(user=user, organization_id=organization_id, permission=ERA_READ)


def can_write(*, user, organization_id: UUID) -> bool:
    """Return whether the actor may create or update ERAs."""

    return _allowed(user=user, organization_id=organization_id, permission=ERA_WRITE)


def can_validate(*, user, organization_id: UUID) -> bool:
    """Return whether the actor may validate an ERA."""

    return _allowed(user=user, organization_id=organization_id, permission=ERA_VALIDATE)


def can_post(*, user, organization_id: UUID) -> bool:
    """Return whether the actor may post an ERA."""

    return _allowed(user=user, organization_id=organization_id, permission=ERA_POST)


def can_reverse(*, user, organization_id: UUID) -> bool:
    """Return whether the actor may reverse an ERA."""

    return _allowed(user=user, organization_id=organization_id, permission=ERA_REVERSE)


def can_delete(*, user, organization_id: UUID) -> bool:
    """Return whether the actor may delete an ERA."""

    return _allowed(user=user, organization_id=organization_id, permission=ERA_DELETE)


def can_restore(*, user, organization_id: UUID) -> bool:
    """Return whether the actor may restore an ERA."""

    return _allowed(user=user, organization_id=organization_id, permission=ERA_RESTORE)


__all__ = (
    "can_delete",
    "can_post",
    "can_read",
    "can_restore",
    "can_reverse",
    "can_validate",
    "can_write",
)
