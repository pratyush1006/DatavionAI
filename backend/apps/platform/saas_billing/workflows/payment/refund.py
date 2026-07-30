"""
Payment refund workflow.

Handles DatavionOS SaaS payment refunds.

Workflow:

Successful Payment
        |
Validate Refund
        |
Payment Service
        |
Update Invoice State
        |
Publish PaymentRefunded Event
"""

from __future__ import annotations

from decimal import Decimal

from apps.platform.saas_billing.events import (
    PaymentRefunded,
)
from apps.platform.saas_billing.models import (
    Payment,
)
from apps.platform.saas_billing.services import (
    PaymentService,
)
from apps.platform.saas_billing.workflows import (
    BaseWorkflow,
)


class RefundPaymentWorkflow(
    BaseWorkflow,
):
    """
    Enterprise payment refund workflow.
    """

    def handle(
        self,
        *,
        payment: Payment,
        refund_amount: Decimal | None = None,
    ) -> Payment:
        """
        Refund payment.

        Supports:

        - Full refund
        - Partial refund
        - Gateway refunds
        - Accounting reconciliation
        """

        if not payment:
            raise ValueError(
                "Payment is required.",
            )

        # --------------------------------------------------------------
        # Validate payment state
        # --------------------------------------------------------------

        if payment.status != (Payment.Status.SUCCESS):
            raise ValueError(
                "Only successful payments can be refunded.",
            )

        amount = refund_amount or payment.amount

        if amount <= 0:
            raise ValueError(
                "Refund amount must be greater than zero.",
            )

        if amount > payment.amount:
            raise ValueError(
                "Refund amount exceeds payment amount.",
            )

        # --------------------------------------------------------------
        # Refund payment
        # --------------------------------------------------------------

        payment = PaymentService.refund(
            payment=payment,
            amount=amount,
        )

        # --------------------------------------------------------------
        # Publish refund event
        # --------------------------------------------------------------

        self.publish_event(
            PaymentRefunded(
                aggregate_id=(payment.id),
                metadata={
                    "organization_id": (str(payment.organization.id)),
                    "invoice_id": (str(payment.invoice.id)),
                    "refund_amount": (str(amount)),
                },
            )
        )

        return payment


__all__ = [
    "RefundPaymentWorkflow",
]
