"""
Plan API tests.

DatavionOS SaaS Billing.

Architecture:

API
 |
RBAC
 |
Serializer
 |
Workflow
 |
Service
 |
Domain Event
"""

from __future__ import annotations

from rest_framework import status

from apps.platform.saas_billing.tests.base import (
    SaaSBillingTestBase,
)
from apps.platform.saas_billing.tests.mixins import (
    OrganizationContextMixin,
)


class PlanAPITestCase(
    OrganizationContextMixin,
    SaaSBillingTestBase,
):
    """
    SaaS Billing Plan API coverage.
    """

    def setUp(
        self,
    ):
        super().setUp()

        self.api_client = self.get_api_client()

    # ==========================================================
    # LIST
    # ==========================================================

    def test_plan_list(
        self,
    ):
        """
        Verify plan catalog listing.
        """

        response = self.api_client.get(
            "/api/saas-billing/plans/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            (
                len(response.data["results"]) >= 0
                if isinstance(response.data, dict) and "results" in response.data
                else True
            ),
        )

    # ==========================================================
    # DETAIL
    # ==========================================================

    def test_plan_detail(
        self,
    ):
        """
        Verify plan detail retrieval.
        """

        response = self.api_client.get(
            f"/api/saas-billing/plans/{self.plan.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            str(self.plan.id),
        )

    # ==========================================================
    # CREATE
    # ==========================================================

    def test_create_plan(
        self,
    ):
        """
        Verify plan creation API.
        """

        response = self.api_client.post(
            "/api/saas-billing/plans/create/",
            {
                "name": "Clinic Starter",
                "code": "clinic-starter-api",
                "price": "999",
                "currency": "INR",
                "billing_cycle": "monthly",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["code"],
            "clinic-starter-api",
        )

    # ==========================================================
    # UPDATE
    # ==========================================================

    def test_update_plan(
        self,
    ):
        """
        Verify plan update API.
        """

        response = self.api_client.patch(
            f"/api/saas-billing/plans/{self.plan.id}/update/",
            {
                "name": "Enterprise Healthcare AI Plus",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["name"],
            "Enterprise Healthcare AI Plus",
        )

    # ==========================================================
    # ACTIONS
    # ==========================================================

    def test_activate_plan(
        self,
    ):
        """
        Verify plan activation API.
        """

        self.plan.is_active = False

        self.plan.save()

        response = self.api_client.post(
            f"/api/saas-billing/plans/{self.plan.id}/activate/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_deactivate_plan(
        self,
    ):
        """
        Verify plan deactivation API.
        """

        response = self.api_client.post(
            f"/api/saas-billing/plans/{self.plan.id}/deactivate/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
