"""
Permission classes for the AR Record module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class AccountsReceivablePermission:
    VIEW = "ar.view"
    CREATE = "ar.create"
    UPDATE = "ar.update"
    DELETE = "ar.delete"


class CanViewAccountsReceivable(BasePermission):
    permission_code = AccountsReceivablePermission.VIEW


class CanCreateAccountsReceivable(BasePermission):
    permission_code = AccountsReceivablePermission.CREATE


class CanUpdateAccountsReceivable(BasePermission):
    permission_code = AccountsReceivablePermission.UPDATE


class CanDeleteAccountsReceivable(BasePermission):
    permission_code = AccountsReceivablePermission.DELETE


__all__ = [
    "CanCreateAccountsReceivable",
    "CanDeleteAccountsReceivable",
    "CanUpdateAccountsReceivable",
    "CanViewAccountsReceivable",
    "AccountsReceivablePermission",
]
