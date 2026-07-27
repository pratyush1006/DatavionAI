"""
Accounts Payable permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class AccountsPayablePermission:
    """
    Accounts Payable permission codes.
    """

    VIEW = "accounts_payable.view"
    CREATE = "accounts_payable.create"
    UPDATE = "accounts_payable.update"
    DELETE = "accounts_payable.delete"


class CanViewAccountsPayable(BasePermission):
    """
    Permission required to view accounts payable.
    """

    permission_code = AccountsPayablePermission.VIEW


class CanCreateAccountsPayable(BasePermission):
    """
    Permission required to create accounts payable.
    """

    permission_code = AccountsPayablePermission.CREATE


class CanUpdateAccountsPayable(BasePermission):
    """
    Permission required to update accounts payable.
    """

    permission_code = AccountsPayablePermission.UPDATE


class CanDeleteAccountsPayable(BasePermission):
    """
    Permission required to delete accounts payable.
    """

    permission_code = AccountsPayablePermission.DELETE


__all__ = [
    "AccountsPayablePermission",
    "CanViewAccountsPayable",
    "CanCreateAccountsPayable",
    "CanUpdateAccountsPayable",
    "CanDeleteAccountsPayable",
]
