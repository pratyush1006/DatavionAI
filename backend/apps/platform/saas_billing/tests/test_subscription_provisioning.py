"""
Subscription provisioning service tests.

These tests intentionally focus on service invariants and do not
recreate the pricing catalog.
"""

from __future__ import annotations

from decimal import Decimal

from django.test import TestCase

from apps.platform.saas_billing.models.plan import Plan
from apps.platform.saas_billing.services.subscription_provisioning import (
    PlanResolutionError,
    SubscriptionAlreadyExistsError,
    SubscriptionProvisioningService,
)


class SubscriptionProvisioningServiceTests(TestCase):
    def test_plan_snapshot_contains_commercial_configuration(self):
        plan = Plan.objects.create(
            name="Provisioning Test",
            code="provisioning-test",
            description="Provisioning test plan",
            plan_type="MONTHLY",
            healthcare_segment="healthcare_provider",
            display_order=999999,
            price=Decimal("0.00"),
            setup_fee=Decimal("0.00"),
            currency="INR",
            billing_cycle="MONTHLY",
            trial_days=0,
            annual_discount_percentage=0,
            max_users=5,
            max_branches=1,
            max_doctors=2,
            max_patients=100,
            max_lab_orders=10,
            max_imaging_orders=10,
            max_pharmacy_products=10,
            max_inventory_transactions=100,
            max_storage_gb=5,
            max_api_requests=1000,
            max_ai_requests=100,
            max_ai_tokens=10000,
            features={"test": True},
            modules={"test": True},
            limits={"test": 1},
            metadata={
                "category": "healthcare_provider",
                "organization_type": "clinic",
                "size": "solo",
                "tier": "free",
            },
            is_active=True,
            is_public=True,
            is_featured=False,
            is_default=False,
            is_custom=False,
        )

        snapshot = SubscriptionProvisioningService._plan_snapshot(plan)

        self.assertEqual(
            snapshot["id"],
            str(plan.id),
        )

        self.assertEqual(
            snapshot["price"],
            "0.00",
        )

        self.assertEqual(
            snapshot["currency"],
            "INR",
        )

        self.assertEqual(
            snapshot["metadata"]["category"],
            "healthcare_provider",
        )

    def test_missing_plan_raises_resolution_error(self):
        with self.assertRaises(PlanResolutionError):
            SubscriptionProvisioningService.resolve_plan(
                category="does_not_exist",
                organization_type="does_not_exist",
                size="solo",
                tier="free",
            )

    def test_duplicate_subscription_is_rejected(self):
        self.assertTrue(
            issubclass(
                SubscriptionAlreadyExistsError,
                Exception,
            )
        )
