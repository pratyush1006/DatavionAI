"""
DatavionOS complete SaaS billing lifecycle E2E test.

Validates:

Organization
    |
Subscription
    |
Usage Collection
    |
Usage Charge
    |
Invoice Generation
    |
Invoice Issue
    |
Payment Creation
    |
Payment Reconciliation
    |
Billing Completion
"""

from __future__ import annotations

from decimal import Decimal

from django.utils import timezone

from apps.platform.saas_billing.models import (
    Invoice,
    Payment,
    Usage,
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
from apps.platform.saas_billing.workflows.usage.charge import (
    ChargeUsageWorkflow,
)
from apps.platform.saas_billing.workflows.usage.collect import (
    CollectUsageWorkflow,
)

from .base import (
    SaaSBillingTestBase,
)


class BillingLifecycleE2ETest(
    SaaSBillingTestBase,
):
    """
    Complete DatavionOS billing lifecycle test.
    """

    def test_complete_billing_lifecycle(
        self,
    ):
        """
        Validate complete SaaS billing flow.
        """

        # ==========================================================
        # SUBSCRIPTION
        # ==========================================================

        subscription = self.subscription

        self.assertEqual(
            subscription.status,
            subscription.Status.ACTIVE,
        )

        # ==========================================================
        # COLLECT USAGE
        # ==========================================================

        usage = CollectUsageWorkflow().handle(
            organization=self.organization,
            metric_type=(Usage.MetricType.AI_REQUESTS),
            value=Decimal("250"),
            module="ai",
            source="AI_ENGINE",
            reference_id="AI-BILLING-E2E-001",
            billable=True,
        )

        self.assertTrue(
            usage.is_billable,
        )

        # ==========================================================
        # CHARGE USAGE
        # ==========================================================

        usage.billing_rate = Decimal("0.020000")

        usage.save(
            update_fields=[
                "billing_rate",
            ],
        )

        charged_usage = ChargeUsageWorkflow().handle(
            usage=usage,
        )

        charged_usage.refresh_from_db()

        self.assertEqual(
            charged_usage.calculated_cost,
            Decimal("5.00"),
        )

        # ==========================================================
        # GENERATE INVOICE
        # ==========================================================

        invoice = GenerateInvoiceWorkflow().handle(
            subscription=subscription,
            usage_amount=(charged_usage.calculated_cost),
        )

        self.assertGreater(
            invoice.total_amount,
            Decimal("0"),
        )

        # ==========================================================
        # ISSUE INVOICE
        # ==========================================================

        invoice = IssueInvoiceWorkflow().handle(
            invoice=invoice,
        )

        self.assertEqual(
            invoice.status,
            Invoice.Status.ISSUED,
        )

        # ==========================================================
        # CREATE PAYMENT
        # ==========================================================

        payment = Payment.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            invoice=invoice,
            provider=(Payment.Provider.MANUAL),
            payment_method=(Payment.PaymentMethod.BANK_TRANSFER),
            amount=(invoice.total_amount),
            currency="INR",
            status=(Payment.Status.SUCCESS),
            transaction_id=("DATAVION-LIFECYCLE-E2E"),
            paid_at=timezone.now(),
        )

        self.assertEqual(
            payment.status,
            Payment.Status.SUCCESS,
        )

        # ==========================================================
        # RECONCILE PAYMENT
        # ==========================================================

        payment = ReconcilePaymentWorkflow().handle(
            payment=payment,
            gateway_response={
                "status": "SUCCESS",
                "gateway": "MANUAL",
                "transaction_id": "DATAVION-LIFECYCLE-E2E",
            },
        )

        payment.refresh_from_db()

        self.assertEqual(
            payment.status,
            Payment.Status.SUCCESS,
        )

        self.assertEqual(
            payment.reconciliation_data.get("gateway_status"),
            "SUCCESS",
        )

        # ==========================================================
        # FINAL ASSERTIONS
        # ==========================================================

        self.assertEqual(
            payment.invoice,
            invoice,
        )

        self.assertEqual(
            invoice.organization,
            self.organization,
        )
