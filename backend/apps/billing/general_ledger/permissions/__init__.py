"""
General Ledger permission exports.
"""

from __future__ import annotations

from .account import (
    CanCreateGeneralLedgerAccount,
    CanDeleteGeneralLedgerAccount,
    CanUpdateGeneralLedgerAccount,
    CanViewGeneralLedgerAccount,
    GeneralLedgerPermission,
)

__all__ = [
    "GeneralLedgerPermission",
    "CanCreateGeneralLedgerAccount",
    "CanDeleteGeneralLedgerAccount",
    "CanUpdateGeneralLedgerAccount",
    "CanViewGeneralLedgerAccount",
]
