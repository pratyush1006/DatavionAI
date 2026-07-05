"""
Prescription permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class CanViewPrescription(BasePermission):
    """
    Permission required to view prescriptions.
    """

    permission_code = "prescription.view"


class CanCreatePrescription(BasePermission):
    """
    Permission required to create prescriptions.
    """

    permission_code = "prescription.create"


class CanUpdatePrescription(BasePermission):
    """
    Permission required to update prescriptions.
    """

    permission_code = "prescription.update"


class CanDeletePrescription(BasePermission):
    """
    Permission required to delete prescriptions.
    """

    permission_code = "prescription.delete"


__all__ = [
    "CanCreatePrescription",
    "CanDeletePrescription",
    "CanUpdatePrescription",
    "CanViewPrescription",
]