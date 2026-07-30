"""
Invoice issue workflow.

Moves DatavionOS invoices from draft
to issued state.

Workflow:

Draft Invoice
      |
Validate Invoice
      |
Invoice Service
      |
Publish InvoiceIssued Event
      |
Return Invoice
"""

from __future__ import annotations

from apps.platform.saas_billing.events import (
    InvoiceIssued,
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


class IssueInvoiceWorkflow(
    BaseWorkflow,
):
    """
    Enterprise invoice issuing workflow.
    """

    def handle(
        self,
        *,
        invoice: Invoice,
    ) -> Invoice:
        """
        Issue invoice.

        Used for:

        - Subscription invoices
        - Usage invoices
        - Enterprise billing cycles
        """

        if not invoice:
            raise ValueError(
                "Invoice is required.",
            )

        # --------------------------------------------------------------
        # Validate invoice state
        # --------------------------------------------------------------

        if invoice.status != (Invoice.Status.DRAFT):
            raise ValueError(
                "Only draft invoices can be issued.",
            )

        # --------------------------------------------------------------
        # Issue invoice
        # --------------------------------------------------------------

        invoice = InvoiceService.issue_invoice(
            invoice=invoice,
        )

        # --------------------------------------------------------------
        # Publish domain event
        # --------------------------------------------------------------

        self.publish_event(
            InvoiceIssued(
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
    "IssueInvoiceWorkflow",
]
