"""
Cash Management permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class CashManagementPermission:
    """
    Cash Management permission codes.
    """

    VIEW = "cash_management.view"
    CREATE = "cash_management.create"
    UPDATE = "cash_management.update"
    DELETE = "cash_management.delete"


class CanViewCashManagement(BasePermission):
    """
    Permission required to view cash management.
    """

    permission_code = CashManagementPermission.VIEW


class CanCreateCashManagement(BasePermission):
    """
    Permission required to create cash management.
    """

    permission_code = CashManagementPermission.CREATE


class CanUpdateCashManagement(BasePermission):
    """
    Permission required to update cash management.
    """

    permission_code = CashManagementPermission.UPDATE


class CanDeleteCashManagement(BasePermission):
    """
    Permission required to delete cash management.
    """

    permission_code = CashManagementPermission.DELETE


__all__ = [
    "CashManagementPermission",
    "CanViewCashManagement",
    "CanCreateCashManagement",
    "CanUpdateCashManagement",
    "CanDeleteCashManagement",
]
