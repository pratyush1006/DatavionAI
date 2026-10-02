from __future__ import annotations

from types import SimpleNamespace

from django.test import SimpleTestCase

from apps.datavionos.onboarding.plan_catalog import (
    organization_type_matches_category,
    plan_is_eligible_for_onboarding,
)


class OnboardingProfilePlanEligibilityTests(SimpleTestCase):
    def test_type_must_belong_to_category(self):
        self.assertTrue(
            organization_type_matches_category("healthcare_provider", "clinic")
        )
        self.assertFalse(organization_type_matches_category("pharmacy", "clinic"))

    def test_size_restriction_is_enforced_from_plan_metadata(self):
        plan = SimpleNamespace(
            healthcare_segment="CLINIC",
            metadata={"organization_sizes": ["small", "medium"]},
        )
        self.assertTrue(
            plan_is_eligible_for_onboarding(
                plan,
                category="healthcare_provider",
                organization_type="clinic",
                size="medium",
            )
        )
        self.assertFalse(
            plan_is_eligible_for_onboarding(
                plan,
                category="healthcare_provider",
                organization_type="clinic",
                size="enterprise",
            )
        )

    def test_type_restriction_is_enforced(self):
        plan = SimpleNamespace(
            healthcare_segment="CLINIC",
            metadata={"organization_types": ["clinic"]},
        )
        self.assertTrue(
            plan_is_eligible_for_onboarding(
                plan,
                category="healthcare_provider",
                organization_type="clinic",
                size="small",
            )
        )
        self.assertFalse(
            plan_is_eligible_for_onboarding(
                plan,
                category="healthcare_provider",
                organization_type="cardiology_clinic",
                size="small",
            )
        )

    def test_missing_eligibility_metadata_remains_backward_compatible(self):
        plan = SimpleNamespace(healthcare_segment="CLINIC", metadata={})
        self.assertTrue(
            plan_is_eligible_for_onboarding(
                plan,
                category="healthcare_provider",
                organization_type="clinic",
                size="small",
            )
        )

    def test_deployed_category_segmented_catalog_matches_type_and_size(self):
        plan = SimpleNamespace(
            healthcare_segment="healthcare_provider",
            code="datavion-healthcare_provider-dental_clinic-solo-starter",
            metadata={},
        )

        self.assertTrue(
            plan_is_eligible_for_onboarding(
                plan,
                category="healthcare_provider",
                organization_type="dental_clinic",
                size="solo",
            )
        )
        self.assertFalse(
            plan_is_eligible_for_onboarding(
                plan,
                category="healthcare_provider",
                organization_type="dental_clinic",
                size="small",
            )
        )
