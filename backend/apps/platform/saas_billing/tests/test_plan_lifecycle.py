"""
Plan lifecycle workflow tests.

DatavionOS SaaS Billing.
"""

from django.test import TestCase

from apps.platform.saas_billing.models import (
    Plan,
)
from apps.platform.saas_billing.workflows import (
    WorkflowRegistry,
)


class PlanLifecycleTestCase(
    TestCase,
):
    """
    Plan lifecycle workflow coverage.
    """

    def test_create_plan(
        self,
    ):
        plan = WorkflowRegistry.execute(
            "plan.create",
            data={
                "name": "Professional Clinic",
                "code": "professional-clinic",
                "price": 999,
                "currency": "INR",
                "billing_cycle": "monthly",
            },
        )

        self.assertIsInstance(
            plan,
            Plan,
        )

        self.assertEqual(
            plan.code,
            "professional-clinic",
        )

    def test_update_plan(
        self,
    ):
        plan = Plan.objects.create(
            name="Starter",
            code="starter",
        )

        updated = WorkflowRegistry.execute(
            "plan.update",
            plan=plan,
            data={
                "name": "Starter Clinic",
            },
        )

        self.assertEqual(
            updated.name,
            "Starter Clinic",
        )

    def test_activate_plan(
        self,
    ):
        plan = Plan.objects.create(
            name="Starter",
            code="starter",
            is_active=False,
        )

        result = WorkflowRegistry.execute(
            "plan.activate",
            plan=plan,
        )

        self.assertTrue(
            result.is_active,
        )

    def test_deactivate_plan(
        self,
    ):
        plan = Plan.objects.create(
            name="Starter",
            code="starter",
            is_active=True,
        )

        result = WorkflowRegistry.execute(
            "plan.deactivate",
            plan=plan,
        )

        self.assertFalse(
            result.is_active,
        )

    def test_archive_plan(
        self,
    ):
        plan = Plan.objects.create(
            name="Starter",
            code="starter",
            is_active=True,
        )

        result = WorkflowRegistry.execute(
            "plan.archive",
            plan=plan,
        )

        self.assertFalse(
            result.is_active,
        )
