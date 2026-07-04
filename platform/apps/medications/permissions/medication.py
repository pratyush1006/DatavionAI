"""
Medication permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class CanViewMedication(BasePermission):
    """
    Permission required to view medications.
    """

    permission_code = "medication.view"


class CanCreateMedication(BasePermission):
    """
    Permission required to create medications.
    """

    permission_code = "medication.create"


class CanUpdateMedication(BasePermission):
    """
    Permission required to update medications.
    """

    permission_code = "medication.update"


class CanDeleteMedication(BasePermission):
    """
    Permission required to delete medications.
    """

    permission_code = "medication.delete"


__all__ = [
    "CanCreateMedication",
    "CanDeleteMedication",
    "CanUpdateMedication",
    "CanViewMedication",
]
