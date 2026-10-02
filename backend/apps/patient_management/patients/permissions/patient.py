"""
Patient Core RBAC permissions.

Patient bounded context permission adapters.

Uses the centralized DatavionOS RBAC engine.

Permission naming convention:

    patients.<action>
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import (
    RBACPermissionBase,
)


class CanViewPatient(RBACPermissionBase):
    """Allows viewing patients."""

    message = "You do not have permission to view patients."

    permission_code = "patients.view"


class CanCreatePatient(RBACPermissionBase):
    """Allows creating patients."""

    message = "You do not have permission to create patients."

    permission_code = "patients.create"


class CanUpdatePatient(RBACPermissionBase):
    """Allows updating patients."""

    message = "You do not have permission to update patients."

    permission_code = "patients.update"


class CanDeletePatient(RBACPermissionBase):
    """Allows deleting patients."""

    message = "You do not have permission to delete patients."

    permission_code = "patients.delete"


class CanActivatePatient(RBACPermissionBase):
    """Allows activating patients."""

    message = "You do not have permission to activate patients."

    permission_code = "patients.activate"


class CanDeactivatePatient(RBACPermissionBase):
    """Allows deactivating patients."""

    message = "You do not have permission to deactivate patients."

    permission_code = "patients.deactivate"


class CanArchivePatient(RBACPermissionBase):
    """Allows archiving patients."""

    message = "You do not have permission to archive patients."

    permission_code = "patients.archive"


class CanRestorePatient(RBACPermissionBase):
    """Allows restoring patients."""

    message = "You do not have permission to restore patients."

    permission_code = "patients.restore"


__all__ = (
    "CanViewPatient",
    "CanCreatePatient",
    "CanUpdatePatient",
    "CanDeletePatient",
    "CanActivatePatient",
    "CanDeactivatePatient",
    "CanArchivePatient",
    "CanRestorePatient",
)
