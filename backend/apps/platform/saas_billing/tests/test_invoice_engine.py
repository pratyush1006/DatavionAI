"""
DatavionOS invoice engine tests.

Validates:

- Invoice generation
- Subscription billing invoice
- Usage amount addition
- Invoice issue lifecycle
- Invoice finalization workflow
"""

from __future__ import annotations

from decimal import Decimal

from apps.platform.saas_billing.models import (
    Invoice,
)
from apps.platform.saas_billing.workflows.invoice.finalize import (
    FinalizeInvoiceWorkflow,
)
from apps.platform.saas_billing.workflows.invoice.generate import (
    GenerateInvoiceWorkflow,
)
from apps.platform.saas_billing.workflows.invoice.issue import (
    IssueInvoiceWorkflow,
)

from .base import (
    SaaSBillingTestBase,
)


class InvoiceEngineTest(
    SaaSBillingTestBase,
):
    """
    Invoice workflow tests.
    """

    def test_generate_invoice(
        self,
    ):
        """
        Validate invoice generation.
        """

        invoice = GenerateInvoiceWorkflow().handle(
            subscription=self.subscription,
        )

        self.assertIsNotNone(invoice.id)

        self.assertEqual(
            invoice.organization,
            self.organization,
        )

        self.assertEqual(
            invoice.subscription,
            self.subscription,
        )

        self.assertEqual(
            invoice.invoice_type,
            Invoice.InvoiceType.SUBSCRIPTION,
        )

        self.assertGreater(
            invoice.total_amount,
            Decimal("0"),
        )

    def test_generate_invoice_with_usage_amount(
        self,
    ):
        """
        Validate usage billing addition.
        """

        invoice = GenerateInvoiceWorkflow().handle(
            subscription=self.subscription,
            usage_amount=Decimal("250"),
        )

        self.assertEqual(
            invoice.total_amount,
            Decimal("10249.00"),
        )

        self.assertEqual(
            invoice.invoice_data.get("usage_amount"),
            "250",
        )

    def test_issue_invoice(
        self,
    ):
        """
        Validate invoice issue lifecycle.
        """

        invoice = GenerateInvoiceWorkflow().handle(
            subscription=self.subscription,
        )

        issued = IssueInvoiceWorkflow().handle(
            invoice=invoice,
        )

        issued.refresh_from_db()

        self.assertEqual(
            issued.status,
            Invoice.Status.ISSUED,
        )

        self.assertIsNotNone(
            issued.issued_at,
        )

    def test_finalize_invoice(
        self,
    ):
        """
        Validate invoice finalization.
        """

        invoice = GenerateInvoiceWorkflow().handle(
            subscription=self.subscription,
        )

        issued = IssueInvoiceWorkflow().handle(
            invoice=invoice,
        )

        finalized = FinalizeInvoiceWorkflow().handle(
            invoice=issued,
        )

        finalized.refresh_from_db()

        self.assertEqual(
            finalized.status,
            Invoice.Status.ISSUED,
        )

        self.assertEqual(
            finalized.invoice_number,
            invoice.invoice_number,
        )

        self.assertGreater(
            finalized.total_amount,
            Decimal("0"),
        )
