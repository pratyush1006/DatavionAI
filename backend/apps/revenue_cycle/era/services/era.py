"""
Remittance Advice services.
"""

from __future__ import annotations

from apps.revenue_cycle.components import RcmService
from apps.revenue_cycle.era.models import RemittanceAdvice

create_remittance = None
update_remittance = None
delete_remittance = None


class RemittanceAdviceService(RcmService):
    """
    Write-side operations for remittance advice records.
    """

    model = RemittanceAdvice


create_remittance = RemittanceAdviceService.create
update_remittance = RemittanceAdviceService.update
delete_remittance = RemittanceAdviceService.delete


__all__ = [
    "RemittanceAdviceService",
    "create_remittance",
    "delete_remittance",
    "update_remittance",
]
