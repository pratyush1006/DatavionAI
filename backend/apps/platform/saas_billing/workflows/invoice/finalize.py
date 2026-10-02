"""
Invoice finalize workflow.

Finalizes DatavionOS SaaS invoices
before payment collection.

Workflow:

Issued Invoice
        |
Validate Invoice
        |
Invoice Service
        |
Publish InvoiceFinalized Event
        |
Prepare Payment Collection
"""

from __future__ import annotations

from apps.platform.saas_billing.events import (
    InvoiceFinalized,
)
from apps.platform.saas_billing.models import (
    Invoice,
)
from apps.platform.saas_billing.services import (
    InvoiceService,
)
from apps.platform.saas_billing.workflows import (
    BaseWorkflow,
)


class FinalizeInvoiceWorkflow(
    BaseWorkflow,
):
    """
    Enterprise invoice finalization workflow.
    """

    def handle(
        self,
        *,
        invoice: Invoice,
    ) -> Invoice:
        """
        Finalize invoice.

        Used before:

        - Payment processing
        - Customer notification
        - Accounting sync
        """

        if not invoice:
            raise ValueError(
                "Invoice is required.",
            )

        # --------------------------------------------------------------
        # Validate invoice state
        # --------------------------------------------------------------

        if invoice.status not in [
            Invoice.Status.ISSUED,
            Invoice.Status.SENT,
        ]:
            raise ValueError(
                "Only issued invoices can be finalized.",
            )

        # --------------------------------------------------------------
        # Validate amount
        # --------------------------------------------------------------

        if invoice.total_amount <= 0:
            raise ValueError(
                "Invoice amount must be greater than zero.",
            )

        # --------------------------------------------------------------
        # Finalize invoice
        # --------------------------------------------------------------

        invoice = InvoiceService.issue_invoice(
            invoice=invoice,
        )

        # --------------------------------------------------------------
        # Publish event
        # --------------------------------------------------------------

        self.publish_event(
            InvoiceFinalized(
                aggregate_id=(invoice.id),
                metadata={
                    "organization_id": (str(invoice.organization.id)),
                    "invoice_number": (invoice.invoice_number),
                    "amount": (str(invoice.total_amount)),
                },
            )
        )

        return invoice


__all__ = [
    "FinalizeInvoiceWorkflow",
]
