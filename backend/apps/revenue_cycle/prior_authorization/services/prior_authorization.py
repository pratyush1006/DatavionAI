"""
Prior Authorization services.
"""

from __future__ import annotations

from apps.revenue_cycle.components import RcmService
from apps.revenue_cycle.prior_authorization.models import PriorAuthorizationRequest

create_authorization = None
update_authorization = None
delete_authorization = None


class PriorAuthorizationRequestService(RcmService):
    """
    Write-side operations for prior authorization records.
    """

    model = PriorAuthorizationRequest


create_authorization = PriorAuthorizationRequestService.create
update_authorization = PriorAuthorizationRequestService.update
delete_authorization = PriorAuthorizationRequestService.delete


__all__ = [
    "PriorAuthorizationRequestService",
    "create_authorization",
    "delete_authorization",
    "update_authorization",
]
