"""
Financial Management permission exports.
"""

from __future__ import annotations

from .financial_management import (
    CanCreateFinancialManagement,
    CanDeleteFinancialManagement,
    CanUpdateFinancialManagement,
    CanViewFinancialManagement,
    FinancialManagementPermission,
)

__all__ = [
    "FinancialManagementPermission",
    "CanViewFinancialManagement",
    "CanCreateFinancialManagement",
    "CanUpdateFinancialManagement",
    "CanDeleteFinancialManagement",
]
