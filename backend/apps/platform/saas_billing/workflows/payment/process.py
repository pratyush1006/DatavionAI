"""
Payment processing workflow.

Handles DatavionOS SaaS payment lifecycle.

Workflow:

Invoice
   |
Validate Invoice
   |
Create Payment
   |
Publish PaymentCreated Event
   |
Gateway Processing
"""

from __future__ import annotations

from apps.platform.saas_billing.events import (
    PaymentCreated,
)
from apps.platform.saas_billing.models import (
    Invoice,
    Payment,
)
from apps.platform.saas_billing.services import (
    PaymentService,
)
from apps.platform.saas_billing.workflows import (
    BaseWorkflow,
)


class ProcessPaymentWorkflow(
    BaseWorkflow,
):
    """
    Enterprise payment processing workflow.
    """

    def handle(
        self,
        *,
        invoice: Invoice,
        provider: str | None = None,
        transaction_id: str | None = None,
    ) -> Payment:
        """
        Process invoice payment.

        Supports:

        - Stripe
        - Razorpay
        - PayPal
        - Bank transfer
        - Manual payments
        """

        if not invoice:
            raise ValueError(
                "Invoice is required.",
            )

        # --------------------------------------------------------------
        # Validate invoice
        # --------------------------------------------------------------

        if invoice.status in [
            Invoice.Status.CANCELLED,
            Invoice.Status.REFUNDED,
        ]:
            raise ValueError(
                "Payment cannot be processed.",
            )

        # --------------------------------------------------------------
        # Create payment
        # --------------------------------------------------------------

        payment = PaymentService.create_payment(
            invoice=invoice,
            amount=invoice.total_amount,
            provider=(provider or ""),
            transaction_id=(transaction_id or ""),
        )

        # --------------------------------------------------------------
        # Publish domain event
        # --------------------------------------------------------------

        self.publish_event(
            PaymentCreated(
                aggregate_id=(payment.id),
                metadata={
                    "organization_id": (str(invoice.organization.id)),
                    "invoice_id": (str(invoice.id)),
                    "amount": (str(payment.amount)),
                    "provider": (payment.provider),
                },
            )
        )

        return payment


__all__ = [
    "ProcessPaymentWorkflow",
]
