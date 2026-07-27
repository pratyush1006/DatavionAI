"""
Eligibility Check services.
"""

from __future__ import annotations

from apps.revenue_cycle.components import RcmService
from apps.revenue_cycle.eligibility.models import EligibilityCheck

create_eligibility = None
update_eligibility = None
delete_eligibility = None


class EligibilityCheckService(RcmService):
    """
    Write-side operations for eligibility check records.
    """

    model = EligibilityCheck


create_eligibility = EligibilityCheckService.create
update_eligibility = EligibilityCheckService.update
delete_eligibility = EligibilityCheckService.delete


__all__ = [
    "EligibilityCheckService",
    "create_eligibility",
    "delete_eligibility",
    "update_eligibility",
]
