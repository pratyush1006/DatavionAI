"""
Permission classes for the Patient Profile module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class ProfilePermission:
    VIEW = "patient_profile.view"
    CREATE = "patient_profile.create"
    UPDATE = "patient_profile.update"
    DELETE = "patient_profile.delete"


class CanViewProfile(BasePermission):
    permission_code = ProfilePermission.VIEW


class CanCreateProfile(BasePermission):
    permission_code = ProfilePermission.CREATE


class CanUpdateProfile(BasePermission):
    permission_code = ProfilePermission.UPDATE


class CanDeleteProfile(BasePermission):
    permission_code = ProfilePermission.DELETE


__all__ = [
    "CanCreateProfile",
    "CanDeleteProfile",
    "CanUpdateProfile",
    "CanViewProfile",
    "ProfilePermission",
]
