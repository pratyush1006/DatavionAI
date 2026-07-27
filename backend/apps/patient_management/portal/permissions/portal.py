"""
Permission classes for the Portal Account module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class PatientPortalAccountPermission:
    VIEW = "portal.view"
    CREATE = "portal.create"
    UPDATE = "portal.update"
    DELETE = "portal.delete"


class CanViewPatientPortalAccount(BasePermission):
    permission_code = PatientPortalAccountPermission.VIEW


class CanCreatePatientPortalAccount(BasePermission):
    permission_code = PatientPortalAccountPermission.CREATE


class CanUpdatePatientPortalAccount(BasePermission):
    permission_code = PatientPortalAccountPermission.UPDATE


class CanDeletePatientPortalAccount(BasePermission):
    permission_code = PatientPortalAccountPermission.DELETE


__all__ = [
    "CanCreatePatientPortalAccount",
    "CanDeletePatientPortalAccount",
    "CanUpdatePatientPortalAccount",
    "CanViewPatientPortalAccount",
    "PatientPortalAccountPermission",
]
