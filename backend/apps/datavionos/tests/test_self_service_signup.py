from __future__ import annotations

from decimal import Decimal
from types import SimpleNamespace

from django.test import SimpleTestCase
from django.urls import resolve, reverse

from apps.datavionos.onboarding.signup import (
    SelfServiceSignupService,
)


class SelfServiceSignupContractTests(SimpleTestCase):
    def test_tenant_type_mapping(self):
        self.assertEqual(
            SelfServiceSignupService.tenant_type_for_organization_type("hospital"),
            "hospital",
        )
        self.assertEqual(
            SelfServiceSignupService.tenant_type_for_organization_type(
                "retail_pharmacy"
            ),
            "pharmacy",
        )
        self.assertEqual(
            SelfServiceSignupService.tenant_type_for_organization_type("clinic"),
            "clinic",
        )

    def test_payment_requirements(self):
        free = SimpleNamespace(
            price=Decimal("0"),
            trial_days=0,
        )
        paid_trial = SimpleNamespace(
            price=Decimal("999"),
            trial_days=14,
        )
        paid_no_trial = SimpleNamespace(
            price=Decimal("999"),
            trial_days=0,
        )

        self.assertEqual(
            SelfServiceSignupService.payment_requirements(free),
            (False, False),
        )
        self.assertEqual(
            SelfServiceSignupService.payment_requirements(paid_trial),
            (True, False),
        )
        self.assertEqual(
            SelfServiceSignupService.payment_requirements(paid_no_trial),
            (True, False),
        )

    def test_signup_route_is_exposed(self):
        url = reverse("organization-onboarding:signup")
        self.assertEqual(url, "/api/onboarding/signup/")
        match = resolve(url)
        self.assertEqual(
            match.url_name,
            "signup",
        )

    def test_public_signup_service_contract_exists(self):
        self.assertTrue(callable(SelfServiceSignupService.signup))
        self.assertTrue(callable(SelfServiceSignupService.preflight))
