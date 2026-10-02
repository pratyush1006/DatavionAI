from importlib import import_module

from django.test import SimpleTestCase


class OrganizationRegistrationRuntimeContractTests(SimpleTestCase):
    def test_organizations_control_plane_is_importable(self):
        modules = (
            "apps.platform.organizations.models.organization",
            "apps.platform.organizations.workflows.organization_creation",
            "apps.platform.organizations.workflows.organization_onboarding",
            "apps.platform.organizations.services.saas_provisioning",
        )
        for module_name in modules:
            with self.subTest(module=module_name):
                import_module(module_name)

    def test_saas_billing_control_plane_is_importable(self):
        modules = (
            "apps.platform.saas_billing.models.plan",
            "apps.platform.saas_billing.models.subscription",
            "apps.platform.saas_billing.services.entitlement_service",
            "apps.platform.saas_billing.selectors.entitlement_selector",
            "apps.platform.saas_billing.workflows.registration",
        )
        for module_name in modules:
            with self.subTest(module=module_name):
                import_module(module_name)

    def test_tenancy_control_plane_is_importable(self):
        modules = (
            "apps.platform.tenancy.models.tenant",
            "apps.platform.tenancy.models.membership",
            "apps.platform.tenancy.context",
            "apps.platform.tenancy.services.tenant",
            "apps.platform.tenancy.services.membership",
        )
        for module_name in modules:
            with self.subTest(module=module_name):
                import_module(module_name)
