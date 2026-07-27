"""
Billing Batch services.
"""

from __future__ import annotations

from apps.revenue_cycle.billing.models import BillingBatch
from apps.revenue_cycle.components import RcmService

create_batch = None
update_batch = None
delete_batch = None


class BillingBatchService(RcmService):
    """
    Write-side operations for billing batch records.
    """

    model = BillingBatch


create_batch = BillingBatchService.create
update_batch = BillingBatchService.update
delete_batch = BillingBatchService.delete


__all__ = [
    "BillingBatchService",
    "create_batch",
    "delete_batch",
    "update_batch",
]
