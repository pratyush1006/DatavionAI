"""
Claim Appeal services.
"""

from __future__ import annotations

from apps.revenue_cycle.appeals.models import ClaimAppeal
from apps.revenue_cycle.components import RcmService

create_appeal = None
update_appeal = None
delete_appeal = None


class ClaimAppealService(RcmService):
    """
    Write-side operations for claim appeal records.
    """

    model = ClaimAppeal


create_appeal = ClaimAppealService.create
update_appeal = ClaimAppealService.update
delete_appeal = ClaimAppealService.delete


__all__ = [
    "ClaimAppealService",
    "create_appeal",
    "delete_appeal",
    "update_appeal",
]
