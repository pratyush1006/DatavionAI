"""
Diagnosis permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class CanViewDiagnosis(BasePermission):
    """
    Permission required to view diagnoses.
    """

    permission_code = "diagnosis.view"


class CanCreateDiagnosis(BasePermission):
    """
    Permission required to create diagnoses.
    """

    permission_code = "diagnosis.create"


class CanUpdateDiagnosis(BasePermission):
    """
    Permission required to update diagnoses.
    """

    permission_code = "diagnosis.update"


class CanDeleteDiagnosis(BasePermission):
    """
    Permission required to delete diagnoses.
    """

    permission_code = "diagnosis.delete"


__all__ = [
    "CanCreateDiagnosis",
    "CanDeleteDiagnosis",
    "CanUpdateDiagnosis",
    "CanViewDiagnosis",
]
