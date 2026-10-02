from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from apps.platform.organizations.services.saas_provisioning import (
    OrganizationProvisioningError,
    provision_organization_saas,
    resolve_healthcare_segment,
    resolve_signup_plan,
)


class OrganizationSaaSProvisioningTests(SimpleTestCase):
    def test_supported_organization_types_map_to_plan_segments(self):
        self.assertEqual(resolve_healthcare_segment("clinic"), "CLINIC")
        self.assertEqual(resolve_healthcare_segment("medical store"), "PHARMACY")
        self.assertEqual(
            resolve_healthcare_segment("diagnostic-laboratory"), "LABORATORY"
        )
        self.assertEqual(resolve_healthcare_segment("Dental Clinic"), "DENTAL")

    def test_unknown_organization_type_fails_closed(self):
        with self.assertRaises(OrganizationProvisioningError):
            resolve_healthcare_segment("UNKNOWN_HEALTHCARE_TYPE")

    @patch("apps.platform.organizations.services.saas_provisioning.Plan.objects")
    def test_explicit_plan_must_match_organization_segment(self, objects):
        queryset = MagicMock()
        objects.filter.return_value = queryset
        queryset.filter.return_value.first.return_value = None

        with self.assertRaises(OrganizationProvisioningError):
            resolve_signup_plan(
                organization_type="CLINIC",
                plan_code="pharmacy-pro",
            )

        objects.filter.assert_called_once_with(
            is_active=True,
            healthcare_segment="CLINIC",
        )
        queryset.filter.assert_called_once_with(code="pharmacy-pro")

    @patch(
        "apps.platform.organizations.services.saas_provisioning.Subscription.objects"
    )
    @patch(
        "apps.platform.organizations.services.saas_provisioning.SubscriptionService.create_trial_subscription"
    )
    @patch("apps.platform.organizations.services.saas_provisioning.resolve_signup_plan")
    def test_provisioning_creates_trial_from_matching_plan(
        self,
        resolve_plan,
        create_trial,
        subscriptions,
    ):
        plan = SimpleNamespace(code="clinic-starter", healthcare_segment="CLINIC")
        subscription = SimpleNamespace(
            plan=plan,
            status="TRIAL",
            feature_snapshot={
                "modules": {"patients": True, "pharmacy": False},
                "features": {"patients.dashboard": True},
            },
        )
        organization = SimpleNamespace(
            pk="org-1",
            organization_type="CLINIC",
        )

        subscriptions.select_related.return_value.filter.return_value.first.return_value = None
        resolve_plan.return_value = plan
        create_trial.return_value = subscription

        result = provision_organization_saas(organization=organization)

        resolve_plan.assert_called_once_with(
            organization_type="CLINIC",
            plan_code=None,
        )
        create_trial.assert_called_once_with(
            organization=organization,
            plan=plan,
        )
        self.assertEqual(result.plan_code, "clinic-starter")
        self.assertEqual(result.healthcare_segment, "CLINIC")
        self.assertEqual(result.modules, {"patients": True})
        self.assertEqual(result.features, {"patients.dashboard": True})

    @patch("apps.platform.organizations.services.saas_provisioning.resolve_signup_plan")
    def test_existing_subscription_is_idempotent(self, resolve_plan):
        plan = SimpleNamespace(code="clinic-starter", healthcare_segment="CLINIC")
        subscription = SimpleNamespace(
            plan=plan,
            status="TRIAL",
            feature_snapshot={"modules": {"patients": True}, "features": {}},
        )
        organization = SimpleNamespace(pk="org-2", organization_type="CLINIC")

        manager = MagicMock()
        manager.select_related.return_value.filter.return_value.first.return_value = (
            subscription
        )

        with (
            patch(
                "apps.platform.organizations.services.saas_provisioning.Subscription.objects",
                manager,
            ),
            patch(
                "apps.platform.organizations.services.saas_provisioning.SubscriptionService.create_trial_subscription"
            ) as create_trial,
        ):
            resolve_plan.return_value = plan
            result = provision_organization_saas(organization=organization)

        create_trial.assert_not_called()
        self.assertEqual(result.plan_code, "clinic-starter")
        self.assertEqual(result.modules, {"patients": True})

    @patch("apps.platform.organizations.services.saas_provisioning.resolve_signup_plan")
    def test_existing_subscription_with_wrong_segment_fails_closed(self, resolve_plan):
        requested_plan = SimpleNamespace(
            code="clinic-starter", healthcare_segment="CLINIC"
        )
        existing_plan = SimpleNamespace(
            code="pharmacy-pro", healthcare_segment="PHARMACY"
        )
        subscription = SimpleNamespace(
            plan=existing_plan, status="TRIAL", feature_snapshot={}
        )
        organization = SimpleNamespace(pk="org-3", organization_type="CLINIC")

        manager = MagicMock()
        manager.select_related.return_value.filter.return_value.first.return_value = (
            subscription
        )

        with patch(
            "apps.platform.organizations.services.saas_provisioning.Subscription.objects",
            manager,
        ):
            resolve_plan.return_value = requested_plan
            with self.assertRaises(OrganizationProvisioningError):
                provision_organization_saas(organization=organization)
