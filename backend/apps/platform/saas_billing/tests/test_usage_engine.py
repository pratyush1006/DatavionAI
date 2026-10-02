"""
DatavionOS usage engine tests.

Validates:

- Usage collection
- Usage charging
- Billable calculation
- Metadata enrichment
- Usage cost calculation
"""

from __future__ import annotations

from decimal import Decimal

from django.utils import timezone

from apps.platform.saas_billing.models import (
    Usage,
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


class UsageEngineTest(
    SaaSBillingTestBase,
):
    """
    Usage metering workflow tests.
    """

    def test_collect_usage(
        self,
    ):
        """
        Validate usage collection.
        """

        usage = CollectUsageWorkflow().handle(
            organization=self.organization,
            metric_type=(Usage.MetricType.PATIENTS),
            value=Decimal("100"),
            module="patient_management",
            source="PATIENT_REGISTRATION",
            reference_id="PATIENT-E2E-001",
            billable=True,
        )

        self.assertIsNotNone(usage.id)

        self.assertEqual(
            usage.metric_type,
            Usage.MetricType.PATIENTS,
        )

        self.assertEqual(
            usage.value,
            Decimal("100"),
        )

        self.assertTrue(usage.is_billable)

        self.assertEqual(
            usage.source,
            "PATIENT_REGISTRATION",
        )

    def test_charge_usage(
        self,
    ):
        """
        Validate usage billing calculation.
        """

        usage = CollectUsageWorkflow().handle(
            organization=self.organization,
            metric_type=(Usage.MetricType.AI_REQUESTS),
            value=Decimal("250"),
            module="ai",
            source="AI_ENGINE",
            reference_id="AI-REQUEST-BATCH",
            billable=True,
        )

        usage.billing_rate = Decimal("0.020000")

        usage.save(
            update_fields=[
                "billing_rate",
            ]
        )

        charged = ChargeUsageWorkflow().handle(
            usage=usage,
        )

        charged.refresh_from_db()

        self.assertEqual(
            charged.calculated_cost,
            Decimal("5.00"),
        )

        self.assertTrue(charged.metadata.get("charge_calculated"))

        self.assertEqual(
            charged.metadata.get("billing_rate"),
            "0.020000",
        )

    def test_usage_charge_idempotency(
        self,
    ):
        """
        Validate duplicate charging protection.
        """

        usage = CollectUsageWorkflow().handle(
            organization=self.organization,
            metric_type=(Usage.MetricType.AI_REQUESTS),
            value=Decimal("100"),
            billable=True,
        )

        usage.billing_rate = Decimal("0.050000")

        usage.save(
            update_fields=[
                "billing_rate",
            ]
        )

        first = ChargeUsageWorkflow().handle(
            usage=usage,
        )

        first_cost = first.calculated_cost

        second = ChargeUsageWorkflow().handle(
            usage=first,
        )

        self.assertEqual(
            second.calculated_cost,
            first_cost,
        )

    def test_non_billable_usage_skipped(
        self,
    ):
        """
        Validate non billable usage.
        """

        usage = Usage.objects.create(
            tenant=self.tenant,
            organization=self.organization,
            metric_type=(Usage.MetricType.PATIENTS),
            value=Decimal("50"),
            unit="count",
            is_billable=False,
            period_start=timezone.now(),
            period_end=timezone.now(),
        )

        result = ChargeUsageWorkflow().handle(
            usage=usage,
        )

        self.assertEqual(
            result.calculated_cost,
            Decimal("0"),
        )
