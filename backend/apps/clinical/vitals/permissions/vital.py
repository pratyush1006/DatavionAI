"""
Vital permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class CanViewVital(BasePermission):
    """
    Permission required to view vitals.
    """

    permission_code = "vital.view"


class CanCreateVital(BasePermission):
    """
    Permission required to create vitals.
    """

    permission_code = "vital.create"


class CanUpdateVital(BasePermission):
    """
    Permission required to update vitals.
    """

    permission_code = "vital.update"


class CanDeleteVital(BasePermission):
    """
    Permission required to delete vitals.
    """

    permission_code = "vital.delete"


__all__ = [
    "CanCreateVital",
    "CanDeleteVital",
    "CanUpdateVital",
    "CanViewVital",
]
