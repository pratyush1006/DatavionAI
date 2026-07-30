"""
DatavionOS payment engine tests.

Validates:

- Payment creation
- Payment reconciliation
- Payment success lifecycle
- Partial refund
- Refund validation
"""

from __future__ import annotations

from decimal import Decimal

from django.utils import timezone

from apps.platform.saas_billing.models import (
    Payment,
)
from apps.platform.saas_billing.workflows.invoice.generate import (
    GenerateInvoiceWorkflow,
)
from apps.platform.saas_billing.workflows.invoice.issue import (
    IssueInvoiceWorkflow,
)
from apps.platform.saas_billing.workflows.payment.reconcile import (
    ReconcilePaymentWorkflow,
)
from apps.platform.saas_billing.workflows.payment.refund import (
    RefundPaymentWorkflow,
)

from .base import (
    SaaSBillingTestBase,
)


class PaymentEngineTest(
    SaaSBillingTestBase,
):
    """
    Payment lifecycle tests.
    """

    def create_paid_invoice(
        self,
    ):
        """
        Create invoice ready for payment.
        """

        invoice = GenerateInvoiceWorkflow().handle(
            subscription=self.subscription,
        )

        return IssueInvoiceWorkflow().handle(
            invoice=invoice,
        )

    def create_payment(
        self,
        invoice,
    ):
        """
        Create successful payment.
        """

        return Payment.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            invoice=invoice,
            provider=(Payment.Provider.MANUAL),
            payment_method=(Payment.PaymentMethod.BANK_TRANSFER),
            amount=(invoice.total_amount),
            currency="INR",
            status=(Payment.Status.SUCCESS),
            transaction_id="DATAVION-PAY-E2E-001",
            paid_at=timezone.now(),
        )

    def test_payment_creation(
        self,
    ):
        """
        Validate payment creation.
        """

        invoice = self.create_paid_invoice()

        payment = self.create_payment(
            invoice,
        )

        self.assertIsNotNone(payment.id)

        self.assertEqual(
            payment.status,
            Payment.Status.SUCCESS,
        )

        self.assertEqual(
            payment.amount,
            invoice.total_amount,
        )

    def test_payment_reconciliation(
        self,
    ):
        """
        Validate gateway reconciliation.
        """

        invoice = self.create_paid_invoice()

        payment = self.create_payment(
            invoice,
        )

        reconciled = ReconcilePaymentWorkflow().handle(
            payment=payment,
            gateway_response={
                "status": "SUCCESS",
                "gateway": "MANUAL",
                "transaction_id": "RECON-E2E-001",
            },
        )

        reconciled.refresh_from_db()

        self.assertEqual(
            reconciled.status,
            Payment.Status.SUCCESS,
        )

        self.assertEqual(
            reconciled.reconciliation_data.get("gateway_status"),
            "SUCCESS",
        )

    def test_partial_refund(
        self,
    ):
        """
        Validate partial refund.
        """

        invoice = self.create_paid_invoice()

        payment = self.create_payment(
            invoice,
        )

        refunded = RefundPaymentWorkflow().handle(
            payment=payment,
            refund_amount=Decimal("1000.00"),
        )

        refunded.refresh_from_db()

        self.assertEqual(
            refunded.status,
            Payment.Status.PARTIALLY_REFUNDED,
        )

        self.assertEqual(
            refunded.refunded_amount,
            Decimal("1000.00"),
        )

        self.assertIsNotNone(
            refunded.refunded_at,
        )

    def test_full_refund(
        self,
    ):
        """
        Validate full refund lifecycle.
        """

        invoice = self.create_paid_invoice()

        payment = self.create_payment(
            invoice,
        )

        refunded = RefundPaymentWorkflow().handle(
            payment=payment,
            refund_amount=(invoice.total_amount),
        )

        refunded.refresh_from_db()

        self.assertEqual(
            refunded.status,
            Payment.Status.REFUNDED,
        )

        self.assertEqual(
            refunded.refunded_amount,
            invoice.total_amount,
        )
