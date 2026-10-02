"""Authorization policies for claim submission."""

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


def can_view_submissions(*, user, organization):
    """Return whether the actor can view submissions in the organization."""

    return _has_permission(
        user=user,
        permission="revenue_cycle.claim_submission.view",
        organization=organization,
    )


def can_manage_submissions(*, user, organization):
    """Return whether the actor can manage submissions in the organization."""

    return _has_permission(
        user=user,
        permission="revenue_cycle.claim_submission.manage",
        organization=organization,
    )


__all__ = ("can_view_submissions", "can_manage_submissions")
