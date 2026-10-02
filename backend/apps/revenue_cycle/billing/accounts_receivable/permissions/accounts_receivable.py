"""
Accounts Receivable permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class AccountsReceivablePermission:
    """
    Accounts Receivable permission codes.
    """

    VIEW = "accounts_receivable.view"
    CREATE = "accounts_receivable.create"
    UPDATE = "accounts_receivable.update"
    DELETE = "accounts_receivable.delete"


class CanViewAccountsReceivable(BasePermission):
    """
    Permission required to view accounts receivable.
    """

    permission_code = AccountsReceivablePermission.VIEW


class CanCreateAccountsReceivable(BasePermission):
    """
    Permission required to create accounts receivable.
    """

    permission_code = AccountsReceivablePermission.CREATE


class CanUpdateAccountsReceivable(BasePermission):
    """
    Permission required to update accounts receivable.
    """

    permission_code = AccountsReceivablePermission.UPDATE


class CanDeleteAccountsReceivable(BasePermission):
    """
    Permission required to delete accounts receivable.
    """

    permission_code = AccountsReceivablePermission.DELETE


__all__ = [
    "AccountsReceivablePermission",
    "CanViewAccountsReceivable",
    "CanCreateAccountsReceivable",
    "CanUpdateAccountsReceivable",
    "CanDeleteAccountsReceivable",
]
