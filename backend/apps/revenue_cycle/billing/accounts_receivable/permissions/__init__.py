"""
Accounts Receivable permission exports.
"""

from __future__ import annotations

from .accounts_receivable import (
    AccountsReceivablePermission,
    CanCreateAccountsReceivable,
    CanDeleteAccountsReceivable,
    CanUpdateAccountsReceivable,
    CanViewAccountsReceivable,
)

__all__ = [
    "AccountsReceivablePermission",
    "CanViewAccountsReceivable",
    "CanCreateAccountsReceivable",
    "CanUpdateAccountsReceivable",
    "CanDeleteAccountsReceivable",
]
