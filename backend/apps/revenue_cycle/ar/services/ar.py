"""
AR Record services.
"""

from __future__ import annotations

from apps.revenue_cycle.ar.models import AccountsReceivable
from apps.revenue_cycle.components import RcmService

create_ar = None
update_ar = None
delete_ar = None


class AccountsReceivableService(RcmService):
    """
    Write-side operations for ar record records.
    """

    model = AccountsReceivable


create_ar = AccountsReceivableService.create
update_ar = AccountsReceivableService.update
delete_ar = AccountsReceivableService.delete


__all__ = [
    "AccountsReceivableService",
    "create_ar",
    "delete_ar",
    "update_ar",
]
