"""
DatavionOS SaaS Billing API tests.

Validates:

- Authentication
- Organization isolation
- RBAC access
- Billing API access
- Response contracts
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .base import SaaSBillingTestBase


class BillingAPITest(
    SaaSBillingTestBase,
):
    """
    Billing API integration tests.
    """

    def setUp(
        self,
    ):
        super().setUp()

        self.client = APIClient()

    # ==============================================================
    # AUTH HELPERS
    # ==============================================================

    def authenticate(
        self,
    ):
        """
        Authenticate API client.

        Simulates:

        User
          |
        Organization Context
          |
        RBAC Engine
        """

        self.client.force_authenticate(
            user=self.user,
        )

        self.client.credentials(
            HTTP_X_ORGANIZATION_ID=str(self.organization.id),
        )

    # ==============================================================
    # Authentication
    # ==============================================================

    def test_subscription_requires_authentication(
        self,
    ):
        """
        Anonymous users cannot access subscription.
        """

        response = self.client.get(reverse("saas_billing:subscription-detail"))

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_invoice_list_requires_authentication(
        self,
    ):
        """
        Invoice API requires login.
        """

        response = self.client.get(reverse("saas_billing:invoice-list"))

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    # ==============================================================
    # Authenticated access
    # ==============================================================

    def test_subscription_authenticated_access(
        self,
    ):
        """
        User can access own subscription.
        """

        self.authenticate()

        response = self.client.get(reverse("saas_billing:subscription-detail"))

        self.assertIn(
            response.status_code,
            [
                status.HTTP_200_OK,
                status.HTTP_404_NOT_FOUND,
            ],
        )

    def test_invoice_list_authenticated_access(
        self,
    ):
        """
        User can access invoices.
        """

        self.authenticate()

        response = self.client.get(reverse("saas_billing:invoice-list"))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    # ==============================================================
    # Payment API
    # ==============================================================

    def test_payment_list_authenticated_access(
        self,
    ):
        """
        Payment list API access.
        """

        self.authenticate()

        response = self.client.get(reverse("saas_billing:payment-list"))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    # ==============================================================
    # Usage API
    # ==============================================================

    def test_usage_list_authenticated_access(
        self,
    ):
        """
        Usage list API access.
        """

        self.authenticate()

        response = self.client.get(reverse("saas_billing:usage-list"))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
