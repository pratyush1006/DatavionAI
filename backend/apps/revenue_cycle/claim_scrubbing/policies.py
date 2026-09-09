"""Authorization policies for claim scrubbing."""

from __future__ import annotations

from .rbac import has_permission


def can_manage_scrubs(*, user, organization) -> bool:
    """Return whether the actor can manage claim scrubs."""

    return bool(
        has_permission(
            user=user,
            permission="revenue_cycle.claim_scrubbing.manage",
            organization=organization,
        )
    )


def can_view_scrubs(*, user, organization) -> bool:
    """Return whether the actor can view claim scrubs."""

    return bool(
        has_permission(
            user=user,
            permission="revenue_cycle.claim_scrubbing.view",
            organization=organization,
        )
    )


__all__ = ("can_manage_scrubs", "can_view_scrubs")
