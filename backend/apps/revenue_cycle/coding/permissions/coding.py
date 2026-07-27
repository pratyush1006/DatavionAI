"""
Permission classes for the Coding Entry module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class ChargeCodingPermission:
    VIEW = "coding.view"
    CREATE = "coding.create"
    UPDATE = "coding.update"
    DELETE = "coding.delete"


class CanViewChargeCoding(BasePermission):
    permission_code = ChargeCodingPermission.VIEW


class CanCreateChargeCoding(BasePermission):
    permission_code = ChargeCodingPermission.CREATE


class CanUpdateChargeCoding(BasePermission):
    permission_code = ChargeCodingPermission.UPDATE


class CanDeleteChargeCoding(BasePermission):
    permission_code = ChargeCodingPermission.DELETE


__all__ = [
    "CanCreateChargeCoding",
    "CanDeleteChargeCoding",
    "CanUpdateChargeCoding",
    "CanViewChargeCoding",
    "ChargeCodingPermission",
]
