"""Authorization policies for claim scrubbing."""

from __future__ import annotations

from typing import Any

from apps.platform.rbac.resolvers import resolve_permissions


def _has_permission(*, user: Any, permission: str, organization: Any) -> bool:
    """Resolve authorization through the canonical platform RBAC resolver."""

    if user is None or organization is None:
        return False

    permissions = resolve_permissions(
        user=user,
        organization=organization,
    )
    return "*" in permissions or permission in permissions


def can_manage_scrubs(*, user: Any, organization: Any) -> bool:
    """Return whether the actor can manage claim scrubs."""

    return _has_permission(
        user=user,
        permission="revenue_cycle.claim_scrubbing.manage",
        organization=organization,
    )


def can_view_scrubs(*, user: Any, organization: Any) -> bool:
    """Return whether the actor can view claim scrubs."""

    return _has_permission(
        user=user,
        permission="revenue_cycle.claim_scrubbing.view",
        organization=organization,
    )


__all__ = ("can_manage_scrubs", "can_view_scrubs")
