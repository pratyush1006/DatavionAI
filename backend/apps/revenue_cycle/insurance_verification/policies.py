"""Authorization policies for Insurance Verification."""

from __future__ import annotations

from uuid import UUID

from apps.platform.organizations.models import Organization
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


from apps.revenue_cycle.insurance_verification.permissions import (
    InsuranceVerificationPermission,
)


def _authorized(
    *, user, permission: InsuranceVerificationPermission, organization_id: UUID
) -> bool:
    """Return whether the user has a permission in the organization."""

    if not user or not user.is_authenticated:
        return False
    organization = Organization.objects.filter(pk=organization_id).first()
    if organization is None:
        return False
    return bool(
        _has_permission(
            user=user,
            permission=permission.value,
            organization=organization,
        )
    )


def can_view(*, user, organization_id: UUID) -> bool:
    """Check view authorization."""

    return _authorized(
        user=user,
        permission=InsuranceVerificationPermission.VIEW,
        organization_id=organization_id,
    )


def can_create(*, user, organization_id: UUID) -> bool:
    """Check create authorization."""

    return _authorized(
        user=user,
        permission=InsuranceVerificationPermission.CREATE,
        organization_id=organization_id,
    )


def can_update(*, user, organization_id: UUID) -> bool:
    """Check update authorization."""

    return _authorized(
        user=user,
        permission=InsuranceVerificationPermission.UPDATE,
        organization_id=organization_id,
    )


def can_delete(*, user, organization_id: UUID) -> bool:
    """Check delete authorization."""

    return _authorized(
        user=user,
        permission=InsuranceVerificationPermission.DELETE,
        organization_id=organization_id,
    )


def can_restore(*, user, organization_id: UUID) -> bool:
    """Check restore authorization."""

    return _authorized(
        user=user,
        permission=InsuranceVerificationPermission.RESTORE,
        organization_id=organization_id,
    )


def can_transition(*, user, organization_id: UUID) -> bool:
    """Check lifecycle authorization."""

    return _authorized(
        user=user,
        permission=InsuranceVerificationPermission.LIFECYCLE,
        organization_id=organization_id,
    )


__all__ = (
    "can_create",
    "can_delete",
    "can_restore",
    "can_transition",
    "can_update",
    "can_view",
)
