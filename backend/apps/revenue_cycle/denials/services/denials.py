"""
Claim Denial services.
"""

from __future__ import annotations

from apps.revenue_cycle.components import RcmService
from apps.revenue_cycle.denials.models import ClaimDenial

create_denial = None
update_denial = None
delete_denial = None


class ClaimDenialService(RcmService):
    """
    Write-side operations for claim denial records.
    """

    model = ClaimDenial


create_denial = ClaimDenialService.create
update_denial = ClaimDenialService.update
delete_denial = ClaimDenialService.delete


__all__ = [
    "ClaimDenialService",
    "create_denial",
    "delete_denial",
    "update_denial",
]
