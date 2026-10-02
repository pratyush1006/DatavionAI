from __future__ import annotations

from types import SimpleNamespace

from django.test import SimpleTestCase

from apps.datavionos.onboarding.plan_catalog import (
    OrganizationOnboardingValidationError,
    organization_type_matches_category,
    plan_is_eligible_for_onboarding,
    plan_segments_for_organization_type,
    validate_organization_profile,
)


class OrganizationRegistrationContractTests(SimpleTestCase):
    def test_type_plan_segment_lookup_is_case_normalized(self):
        self.assertEqual(
            plan_segments_for_organization_type("clinic"),
            ("CLINIC",),
        )
        self.assertEqual(
            plan_segments_for_organization_type("CLINIC"),
            ("CLINIC",),
        )

    def test_category_matches_type(self):
        self.assertTrue(
            organization_type_matches_category(
                "clinic",
                "healthcare_provider",
            )
        )
        self.assertFalse(
            organization_type_matches_category(
                "clinic",
                "pharmacy",
            )
        )

    def test_profile_validation_requires_category_type_and_size(self):
        result = validate_organization_profile(
            {
                "category": "healthcare_provider",
                "organization_type": "clinic",
                "size": "medium",
            }
        )

        self.assertEqual(
            result,
            (
                "healthcare_provider",
                "clinic",
                "medium",
            ),
        )

        with self.assertRaises(
            OrganizationOnboardingValidationError,
        ):
            validate_organization_profile(
                {
                    "category": "pharmacy",
                    "organization_type": "clinic",
                    "size": "medium",
                }
            )

    def test_plan_eligibility_respects_metadata(self):
        plan = SimpleNamespace(
            healthcare_segment="CLINIC",
            metadata={
                "organization_categories": [
                    "healthcare_provider",
                ],
                "organization_types": [
                    "clinic",
                ],
                "organization_sizes": [
                    "small",
                    "medium",
                ],
            },
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

        self.assertFalse(
            plan_is_eligible_for_onboarding(
                plan,
                category="healthcare_provider",
                organization_type="cardiology_clinic",
                size="medium",
            )
        )

    def test_plan_without_optional_metadata_is_backward_compatible(self):
        plan = SimpleNamespace(
            healthcare_segment="CLINIC",
            metadata={},
        )

        self.assertTrue(
            plan_is_eligible_for_onboarding(
                plan,
                category="healthcare_provider",
                organization_type="clinic",
                size="small",
            )
        )
