"""
Invoice generation workflow.

Creates DatavionOS SaaS invoices
from subscription and usage data.

Workflow:

Subscription
      |
Validate Billing Eligibility
      |
Invoice Service
      |
Publish InvoiceGenerated Event
      |
Return Invoice
"""

from __future__ import annotations

from decimal import Decimal

from apps.platform.saas_billing.events import (
    InvoiceGenerated,
)
from apps.platform.saas_billing.models import (
    Invoice,
    Subscription,
)
from apps.platform.saas_billing.services import (
    InvoiceService,
)
from apps.platform.saas_billing.workflows import (
    BaseWorkflow,
)


class GenerateInvoiceWorkflow(
    BaseWorkflow,
):
    """
    Enterprise invoice generation workflow.
    """

    def handle(
        self,
        *,
        subscription: Subscription,
        usage_amount: Decimal = Decimal("0"),
    ) -> Invoice:
        """
        Generate SaaS invoice.

        Supports:

        - Subscription billing
        - Usage billing
        - Healthcare modules
        - AI usage
        """

        if not subscription:
            raise ValueError(
                "Subscription is required.",
            )

        # --------------------------------------------------------------
        # Validate subscription
        # --------------------------------------------------------------

        if subscription.status in [
            Subscription.Status.CANCELLED,
            Subscription.Status.EXPIRED,
        ]:
            raise ValueError(
                "Cannot generate invoice for inactive subscription.",
            )

        # --------------------------------------------------------------
        # Generate invoice
        # --------------------------------------------------------------

        invoice = InvoiceService.create_subscription_invoice(
            subscription=subscription,
        )

        # --------------------------------------------------------------
        # Add usage charges
        # --------------------------------------------------------------

        if usage_amount > 0:
            invoice.subtotal += usage_amount

            invoice.total_amount += usage_amount

            invoice.invoice_data.update({"usage_amount": str(usage_amount)})

            invoice.save(
                update_fields=[
                    "subtotal",
                    "total_amount",
                    "invoice_data",
                    "updated_at",
                ],
            )

        # --------------------------------------------------------------
        # Publish event
        # --------------------------------------------------------------

        self.publish_event(
            InvoiceGenerated(
                aggregate_id=(invoice.id),
                metadata={
                    "organization_id": (str(subscription.organization.id)),
                    "invoice_number": (invoice.invoice_number),
                    "subscription_id": (str(subscription.id)),
                },
            )
        )

        return invoice


__all__ = [
    "GenerateInvoiceWorkflow",
]
