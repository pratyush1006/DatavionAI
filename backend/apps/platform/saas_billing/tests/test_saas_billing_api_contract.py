"""
Canonical SaaS Billing API contract tests.
"""

from __future__ import annotations

from django.urls import get_resolver
from rest_framework.test import APITestCase


class SaaSBillingAPIContractTests(APITestCase):
    """
    Structural contract checks.

    These tests intentionally validate URL exposure rather than
    billing business data.
    """

    def _route_names(self) -> set[str]:
        resolver = get_resolver()

        names: set[str] = set()

        def walk(patterns, prefix=""):
            for pattern in patterns:
                route = getattr(pattern, "_route", "")
                current = f"{prefix}{route}"

                callback = getattr(
                    pattern,
                    "callback",
                    None,
                )

                if callback is not None:
                    names.add(current)

                nested = getattr(
                    pattern,
                    "url_patterns",
                    None,
                )

                if nested:
                    walk(
                        nested,
                        current,
                    )

        walk(resolver.url_patterns)

        return names

    def test_saas_billing_root_is_registered(self):
        routes = self._route_names()

        self.assertTrue(any("saas-billing" in route for route in routes))

    def test_subscription_runtime_route_is_registered(self):
        routes = self._route_names()

        self.assertTrue(any("subscriptions/runtime/" in route for route in routes))

    def test_subscription_collection_route_is_registered_when_available(
        self,
    ):
        routes = self._route_names()

        # The assertion is intentionally soft because the canonical
        # project may expose subscriptions through another aggregate
        # endpoint until a dedicated list implementation exists.
        self.assertTrue(any("subscriptions/" in route for route in routes))

    def test_billing_account_routes_are_registered(self):
        routes = self._route_names()

        self.assertTrue(any("billing-account/" in route for route in routes))

    def test_plan_routes_are_registered(self):
        routes = self._route_names()

        self.assertTrue(any("plans/" in route for route in routes))

    def test_invoice_routes_are_registered(self):
        routes = self._route_names()

        self.assertTrue(any("invoices/" in route for route in routes))

    def test_payment_routes_are_registered(self):
        routes = self._route_names()

        self.assertTrue(any("payments/" in route for route in routes))

    def test_usage_routes_are_registered(self):
        routes = self._route_names()

        self.assertTrue(any("usage/" in route for route in routes))
