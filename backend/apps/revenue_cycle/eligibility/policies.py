"""Authorization policies for Revenue Cycle Eligibility."""

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


from apps.revenue_cycle.eligibility.permissions import EligibilityPermission


def _member(*, actor, organization) -> bool:
    """Return whether the actor has an organization role."""
    return actor.organization_roles.filter(organization_id=organization.pk).exists()


def _allowed(*, actor, organization, permission: str) -> bool:
    """Authorize through the canonical RBAC resolver.

    A platform role with the effective permission is intentionally valid for
    an organization-scoped operation. Requiring an OrganizationRole row here
    incorrectly locked platform administrators out of the selected
    organization and caused the API view to surface a server error.
    """
    return _has_permission(user=actor, permission=permission, organization=organization)


class EligibilityPolicy:
    """Centralize Eligibility authorization decisions."""

    @classmethod
    def can_list(cls, *, actor, organization) -> bool:
        """Authorize listing."""
        return _allowed(
            actor=actor,
            organization=organization,
            permission=EligibilityPermission.VIEW,
        )

    @classmethod
    def can_view(cls, *, actor, eligibility) -> bool:
        """Authorize retrieval."""
        return _allowed(
            actor=actor,
            organization=eligibility.organization,
            permission=EligibilityPermission.VIEW,
        )

    @classmethod
    def can_create(cls, *, actor, organization) -> bool:
        """Authorize creation."""
        return _allowed(
            actor=actor,
            organization=organization,
            permission=EligibilityPermission.CREATE,
        )

    @classmethod
    def can_update(cls, *, actor, eligibility) -> bool:
        """Authorize updates."""
        return _allowed(
            actor=actor,
            organization=eligibility.organization,
            permission=EligibilityPermission.UPDATE,
        )

    @classmethod
    def can_delete(cls, *, actor, eligibility) -> bool:
        """Authorize deletion."""
        return _allowed(
            actor=actor,
            organization=eligibility.organization,
            permission=EligibilityPermission.DELETE,
        )

    @classmethod
    def can_restore(cls, *, actor, organization) -> bool:
        """Authorize restoration."""
        return _allowed(
            actor=actor,
            organization=organization,
            permission=EligibilityPermission.RESTORE,
        )

    @classmethod
    def can_transition(cls, *, actor, eligibility) -> bool:
        """Authorize lifecycle transitions."""
        return _allowed(
            actor=actor,
            organization=eligibility.organization,
            permission=EligibilityPermission.LIFECYCLE,
        )


__all__ = ("EligibilityPolicy",)
