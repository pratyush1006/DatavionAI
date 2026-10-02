"""Authorization policies for Charge Capture."""

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


from ..permissions import (
    ChargeCaptureCreatePermission,
    ChargeCaptureReadPermission,
    ChargeCaptureUpdatePermission,
    ChargeCaptureVoidPermission,
)

__all__ = ("ChargeCapturePolicy",)


class ChargeCapturePolicy:
    """Evaluate scoped RBAC permissions for Charge Capture."""

    @staticmethod
    def can_create(*, actor, organization) -> bool:
        """Return whether the actor may create a charge."""

        return _has_permission(
            user=actor,
            permission=ChargeCaptureCreatePermission.codename,
            organization=organization,
        )

    @staticmethod
    def can_read(*, actor, organization) -> bool:
        """Return whether the actor may read charges."""

        return _has_permission(
            user=actor,
            permission=ChargeCaptureReadPermission.codename,
            organization=organization,
        )

    @staticmethod
    def can_update(*, actor, organization) -> bool:
        """Return whether the actor may update charges."""

        return _has_permission(
            user=actor,
            permission=ChargeCaptureUpdatePermission.codename,
            organization=organization,
        )

    @staticmethod
    def can_void(*, actor, organization) -> bool:
        """Return whether the actor may void charges."""

        return _has_permission(
            user=actor,
            permission=ChargeCaptureVoidPermission.codename,
            organization=organization,
        )
