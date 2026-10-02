"""
Permission classes for the Patient Profile module.
"""

from __future__ import annotations

from apps.platform.rbac.permissions.base import RBACPermissionBase


class ProfilePermission:
    """
    Canonical permission codes for Patient Profile operations.
    """

    VIEW = "patient_profile.view"
    CREATE = "patient_profile.create"
    UPDATE = "patient_profile.update"
    DELETE = "patient_profile.delete"


class CanViewProfile(RBACPermissionBase):
    """
    Permission required to view patient profiles.
    """

    permission_code = ProfilePermission.VIEW


class CanCreateProfile(RBACPermissionBase):
    """
    Permission required to create patient profiles.
    """

    permission_code = ProfilePermission.CREATE


class CanUpdateProfile(RBACPermissionBase):
    """
    Permission required to update patient profiles.
    """

    permission_code = ProfilePermission.UPDATE


class CanDeleteProfile(RBACPermissionBase):
    """
    Permission required to delete patient profiles.
    """

    permission_code = ProfilePermission.DELETE


__all__ = [
    "CanCreateProfile",
    "CanDeleteProfile",
    "CanUpdateProfile",
    "CanViewProfile",
    "ProfilePermission",
]
