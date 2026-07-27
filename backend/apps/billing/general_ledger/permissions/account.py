"""
General Ledger permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class GeneralLedgerPermission:
    """
    General Ledger permission codes.
    """

    VIEW = "general_ledger.view"
    CREATE = "general_ledger.create"
    UPDATE = "general_ledger.update"
    DELETE = "general_ledger.delete"


class CanViewGeneralLedgerAccount(BasePermission):
    """
    Permission required to view general ledger accounts.
    """

    permission_code = GeneralLedgerPermission.VIEW


class CanCreateGeneralLedgerAccount(BasePermission):
    """
    Permission required to create general ledger accounts.
    """

    permission_code = GeneralLedgerPermission.CREATE


class CanUpdateGeneralLedgerAccount(BasePermission):
    """
    Permission required to update general ledger accounts.
    """

    permission_code = GeneralLedgerPermission.UPDATE


class CanDeleteGeneralLedgerAccount(BasePermission):
    """
    Permission required to delete general ledger accounts.
    """

    permission_code = GeneralLedgerPermission.DELETE


__all__ = [
    "GeneralLedgerPermission",
    "CanCreateGeneralLedgerAccount",
    "CanDeleteGeneralLedgerAccount",
    "CanUpdateGeneralLedgerAccount",
    "CanViewGeneralLedgerAccount",
]
