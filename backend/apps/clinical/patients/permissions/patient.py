"""
Patient permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class PatientPermission:
    """
    Patient permission codes.
    """

    VIEW = "patient.view"
    CREATE = "patient.create"
    UPDATE = "patient.update"
    DELETE = "patient.delete"


class CanViewPatient(BasePermission):
    """
    Permission required to view patients.
    """

    permission_code = PatientPermission.VIEW


class CanCreatePatient(BasePermission):
    """
    Permission required to create patients.
    """

    permission_code = PatientPermission.CREATE


class CanUpdatePatient(BasePermission):
    """
    Permission required to update patients.
    """

    permission_code = PatientPermission.UPDATE


class CanDeletePatient(BasePermission):
    """
    Permission required to delete patients.
    """

    permission_code = PatientPermission.DELETE


__all__ = [
    "PatientPermission",
    "CanCreatePatient",
    "CanDeletePatient",
    "CanUpdatePatient",
    "CanViewPatient",
]
