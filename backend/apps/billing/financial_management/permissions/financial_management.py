"""
Financial Management permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class FinancialManagementPermission:
    """
    Financial Management permission codes.
    """

    VIEW = "financial_management.view"
    CREATE = "financial_management.create"
    UPDATE = "financial_management.update"
    DELETE = "financial_management.delete"


class CanViewFinancialManagement(BasePermission):
    """
    Permission required to view financial management.
    """

    permission_code = FinancialManagementPermission.VIEW


class CanCreateFinancialManagement(BasePermission):
    """
    Permission required to create financial management.
    """

    permission_code = FinancialManagementPermission.CREATE


class CanUpdateFinancialManagement(BasePermission):
    """
    Permission required to update financial management.
    """

    permission_code = FinancialManagementPermission.UPDATE


class CanDeleteFinancialManagement(BasePermission):
    """
    Permission required to delete financial management.
    """

    permission_code = FinancialManagementPermission.DELETE


__all__ = [
    "FinancialManagementPermission",
    "CanViewFinancialManagement",
    "CanCreateFinancialManagement",
    "CanUpdateFinancialManagement",
    "CanDeleteFinancialManagement",
]
