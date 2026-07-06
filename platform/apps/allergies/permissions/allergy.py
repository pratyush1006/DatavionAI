"""
Allergy permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class CanViewAllergy(BasePermission):
    """
    Permission required to view allergies.
    """

    permission_code = "allergy.view"


class CanCreateAllergy(BasePermission):
    """
    Permission required to create allergies.
    """

    permission_code = "allergy.create"


class CanUpdateAllergy(BasePermission):
    """
    Permission required to update allergies.
    """

    permission_code = "allergy.update"


class CanDeleteAllergy(BasePermission):
    """
    Permission required to delete allergies.
    """

    permission_code = "allergy.delete"


__all__ = [
    "CanCreateAllergy",
    "CanDeleteAllergy",
    "CanUpdateAllergy",
    "CanViewAllergy",
]
