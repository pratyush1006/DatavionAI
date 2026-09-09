"""RBAC permissions for patient emergency management."""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class EmergencyPermission(RBACPermissionBase):
    """Define permission metadata for emergency operations."""

    code_prefix = "patient_emergency"

    def has_permission(self, user, permission: str, organization=None) -> bool:
        """Return whether the actor has the requested permission."""

        return self.user_has_permission(
            user=user,
            permission=permission,
            organization=organization,
        )


PERMISSION_CODES = (
    "patient_emergency.view",
    "patient_emergency.create",
    "patient_emergency.update",
    "patient_emergency.delete",
    "patient_emergency.activate",
    "patient_emergency.deactivate",
    "patient_emergency.set_primary",
)


__all__ = (
    "EmergencyPermission",
    "PERMISSION_CODES",
)
