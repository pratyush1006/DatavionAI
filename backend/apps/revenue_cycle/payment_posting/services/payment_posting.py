"""
Payment Posting services.
"""

from __future__ import annotations

from apps.revenue_cycle.components import RcmService
from apps.revenue_cycle.payment_posting.models import PaymentPosting

create_posting = None
update_posting = None
delete_posting = None


class PaymentPostingService(RcmService):
    """
    Write-side operations for payment posting records.
    """

    model = PaymentPosting


create_posting = PaymentPostingService.create
update_posting = PaymentPostingService.update
delete_posting = PaymentPostingService.delete


__all__ = [
    "PaymentPostingService",
    "create_posting",
    "delete_posting",
    "update_posting",
]
