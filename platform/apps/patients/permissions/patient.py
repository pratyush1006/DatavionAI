"""
Patient permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class CanViewPatient(BasePermission):
    """
    Permission required to view patients.
    """

    permission_code = "patient.view"


class CanCreatePatient(BasePermission):
    """
    Permission required to create patients.
    """

    permission_code = "patient.create"


class CanUpdatePatient(BasePermission):
    """
    Permission required to update patients.
    """

    permission_code = "patient.update"


class CanDeletePatient(BasePermission):
    """
    Permission required to delete patients.
    """

    permission_code = "patient.delete"


__all__ = [
    "CanCreatePatient",
    "CanDeletePatient",
    "CanUpdatePatient",
    "CanViewPatient",
]
