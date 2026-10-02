"""
Canonical SaaS Billing subscription runtime API tests.
"""

from __future__ import annotations

from django.test import SimpleTestCase
from django.urls import resolve, reverse

from apps.platform.saas_billing.api.views.subscription_runtime import (
    CurrentSubscriptionAPIView,
    SubscriptionRuntimeAPIView,
)


class SubscriptionRuntimeAPIArchitectureTests(
    SimpleTestCase,
):
    """Validate canonical subscription runtime API architecture."""

    def test_runtime_view_exists(self) -> None:
        self.assertTrue(
            issubclass(
                SubscriptionRuntimeAPIView,
                object,
            )
        )

    def test_current_subscription_compatibility_export(self) -> None:
        self.assertTrue(
            issubclass(
                CurrentSubscriptionAPIView,
                object,
            )
        )

    def test_runtime_route_exists(self) -> None:
        url = reverse("saas_billing:subscription-runtime")

        self.assertEqual(
            url,
            "/api/saas-billing/subscription/runtime/",
        )

        match = resolve(url)

        self.assertIs(
            match.func.view_class,
            SubscriptionRuntimeAPIView,
        )
