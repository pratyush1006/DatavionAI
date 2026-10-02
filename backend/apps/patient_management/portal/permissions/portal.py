"""
RBAC adapters for Patient Portal.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class CanListPatientPortal(RBACPermissionBase):
    """Require patient portal list permission."""

    permission_code = "patient_portal.list"
    message = "You do not have permission to list patient portal accounts."


class CanViewPatientPortal(RBACPermissionBase):
    """Require patient portal view permission."""

    permission_code = "patient_portal.view"
    message = "You do not have permission to view patient portal accounts."


class CanCreatePatientPortal(RBACPermissionBase):
    """Require patient portal create permission."""

    permission_code = "patient_portal.create"
    message = "You do not have permission to create patient portal accounts."


class CanUpdatePatientPortal(RBACPermissionBase):
    """Require patient portal update permission."""

    permission_code = "patient_portal.update"
    message = "You do not have permission to update patient portal accounts."


class CanDeletePatientPortal(RBACPermissionBase):
    """Require patient portal delete permission."""

    permission_code = "patient_portal.delete"
    message = "You do not have permission to delete patient portal accounts."


class CanRestorePatientPortal(RBACPermissionBase):
    """Require patient portal restore permission."""

    permission_code = "patient_portal.restore"
    message = "You do not have permission to restore patient portal accounts."


class CanTransitionPatientPortal(RBACPermissionBase):
    """Require patient portal transition permission."""

    permission_code = "patient_portal.transition"
    message = "You do not have permission to change portal account status."


class CanInvitePatientPortal(RBACPermissionBase):
    """Require patient portal invitation permission."""

    permission_code = "patient_portal.invite"
    message = "You do not have permission to issue portal invitations."


__all__ = (
    "CanCreatePatientPortal",
    "CanDeletePatientPortal",
    "CanInvitePatientPortal",
    "CanListPatientPortal",
    "CanRestorePatientPortal",
    "CanTransitionPatientPortal",
    "CanUpdatePatientPortal",
    "CanViewPatientPortal",
)
