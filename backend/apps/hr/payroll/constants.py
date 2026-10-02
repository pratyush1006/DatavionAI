"""
Payroll constants.
"""

from __future__ import annotations

from django.db.models import TextChoices


class PayslipStatus(TextChoices):
    """
    Payslip workflow status choices.
    """

    DRAFT = "draft", "Draft"
    PROCESSED = "processed", "Processed"
    PAID = "paid", "Paid"
    CANCELLED = "cancelled", "Cancelled"


DEFAULT_PAYSLIP_STATUS = PayslipStatus.DRAFT


__all__ = [
    "PayslipStatus",
    "DEFAULT_PAYSLIP_STATUS",
]
