from __future__ import annotations

from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from apps.platform.organizations.models import OrganizationModule
from apps.platform.organizations.services.organization_module import (
    ModuleEntitlementError,
    enable_module,
    update_module,
)


class SaaSModuleEntitlementWriteBoundaryTests(SimpleTestCase):
    """Verify SaaS entitlement is the upper bound for organization module ON."""

    def _instance(self):
        instance = MagicMock()
        instance.status = OrganizationModule.Status.DISABLED
        instance.module_code = "PHARMACY"
        instance.organization = MagicMock()
        return instance

    @patch(
        "apps.platform.saas_billing.services.entitlement_service.EntitlementService.has_module",
        return_value=False,
    )
    def test_enable_unpurchased_module_fails_closed(self, has_module):
        instance = self._instance()
        with self.assertRaises(ModuleEntitlementError):
            enable_module(instance=instance)
        has_module.assert_called_once_with(
            organization=instance.organization,
            module="PHARMACY",
        )
        instance.save.assert_not_called()

    @patch(
        "apps.platform.saas_billing.services.entitlement_service.EntitlementService.has_module",
        return_value=True,
    )
    def test_enable_purchased_module_is_allowed(self, has_module):
        instance = self._instance()
        result = enable_module(instance=instance)
        self.assertIs(result, instance)
        has_module.assert_called_once_with(
            organization=instance.organization,
            module="PHARMACY",
        )
        instance.save.assert_called_once()
        self.assertEqual(instance.status, OrganizationModule.Status.ENABLED)

    @patch(
        "apps.platform.saas_billing.services.entitlement_service.EntitlementService.has_module",
        return_value=False,
    )
    def test_update_cannot_bypass_enable_guard(self, has_module):
        instance = self._instance()
        with self.assertRaises(ModuleEntitlementError):
            update_module(
                instance=instance,
                validated_data={"status": OrganizationModule.Status.ENABLED},
            )
        has_module.assert_called_once_with(
            organization=instance.organization,
            module="PHARMACY",
        )
        instance.save.assert_not_called()

    @patch(
        "apps.platform.saas_billing.services.entitlement_service.EntitlementService.has_module",
        return_value=True,
    )
    def test_update_purchased_module_can_enable(self, has_module):
        instance = self._instance()
        result = update_module(
            instance=instance,
            validated_data={"status": OrganizationModule.Status.ENABLED},
        )
        self.assertIs(result, instance)
        has_module.assert_called_once_with(
            organization=instance.organization,
            module="PHARMACY",
        )
        instance.save.assert_called_once()
        self.assertEqual(instance.status, OrganizationModule.Status.ENABLED)
