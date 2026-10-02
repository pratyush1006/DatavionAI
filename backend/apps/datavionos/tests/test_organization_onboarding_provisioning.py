from __future__ import annotations

import os
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.test import SimpleTestCase

from apps.datavionos.onboarding.contracts import (
    OrganizationOnboardingRequest,
    OrganizationOnboardingResult,
)
from apps.datavionos.onboarding.provisioning import (
    OrganizationOnboardingProvisioner,
    OrganizationPlanMismatchError,
)


class OrganizationOnboardingProvisioningTests(SimpleTestCase):
    def test_request_requires_organization_type(self):
        request = OrganizationOnboardingRequest(
            tenant=object(),
            organization_data={"name": "Test"},
        )
        with self.assertRaises(ValueError):
            OrganizationOnboardingProvisioner._organization_type(
                request.organization_data,
            )

    def test_plan_resolution_uses_matching_healthcare_segment(self):
        plan = SimpleNamespace(
            pk="p1",
            code="clinic-starter",
            healthcare_segment="CLINIC",
        )
        manager = MagicMock()
        manager.filter.return_value.order_by.return_value.first.return_value = plan

        with patch(
            "apps.datavionos.onboarding.provisioning.Plan.objects",
            manager,
        ):
            result = OrganizationOnboardingProvisioner._resolve_plan(
                OrganizationOnboardingRequest(
                    tenant=object(),
                    organization_data={
                        "organization_type": "CLINIC",
                    },
                ),
                "CLINIC",
            )

        self.assertIs(result, plan)

    def test_explicit_plan_mismatch_is_rejected(self):
        plan = SimpleNamespace(
            pk="p1",
            code="pharmacy-pro",
            healthcare_segment="PHARMACY",
        )
        manager = MagicMock()
        manager.filter.return_value.first.return_value = plan

        with (
            patch(
                "apps.datavionos.onboarding.provisioning.Plan.objects",
                manager,
            ),
            self.assertRaises(OrganizationPlanMismatchError),
        ):
            OrganizationOnboardingProvisioner._resolve_plan(
                OrganizationOnboardingRequest(
                    tenant=object(),
                    organization_data={
                        "organization_type": "CLINIC",
                    },
                    plan_code="pharmacy-pro",
                ),
                "CLINIC",
            )

    def test_mapping_is_boolean_only(self):
        self.assertEqual(
            OrganizationOnboardingProvisioner._normalize_mapping(
                {
                    "patients": True,
                    "off": False,
                    "malformed": "true",
                }
            ),
            {
                "patients": True,
                "off": False,
            },
        )

    def test_workspace_contract(self):
        self.assertEqual(
            OrganizationOnboardingProvisioner.DEFAULT_WORKSPACE,
            "organization",
        )

    def test_result_serializes_runtime_outputs(self):
        organization = SimpleNamespace(
            pk="o1",
            name="Clinic",
            display_name="Clinic",
            code="clinic",
            slug="clinic",
            organization_type="clinic",
        )
        plan = SimpleNamespace(
            pk="p1",
            code="clinic-starter",
            name="Clinic Starter",
            healthcare_segment="CLINIC",
        )
        subscription = SimpleNamespace(
            pk="s1",
            status="TRIAL",
            plan=plan,
        )

        payload = OrganizationOnboardingResult(
            organization=organization,
            subscription=subscription,
            modules=("appointments", "patients"),
            features=("patients.dashboard",),
            workspace="organization",
            created_organization=True,
            created_subscription=True,
            organization_admin_assigned=True,
        ).as_dict()

        self.assertEqual(
            payload["modules"],
            ["appointments", "patients"],
        )
        self.assertEqual(
            payload["workspace"],
            "organization",
        )
        self.assertTrue(
            payload["organization_admin_assigned"],
        )

    def test_owner_is_part_of_request_contract(self):
        owner = object()
        request = OrganizationOnboardingRequest(
            tenant=object(),
            organization_data={
                "name": "Clinic",
                "organization_type": "CLINIC",
            },
            owner_user=owner,
        )
        self.assertIs(request.owner_user, owner)
