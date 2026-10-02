from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from apps.platform.organizations.models import OrganizationModule
from apps.platform.organizations.services.organization_module import (
    create_module,
    enable_module,
    update_module,
)


class SaaSModuleWriteAuthorityTests(SimpleTestCase):
    def test_enable_blocks_unentitled_module(self):
        organization = SimpleNamespace(pk="org-1")
        module = SimpleNamespace(
            organization=organization,
            module_code="PHARMACY",
            status=OrganizationModule.Status.DISABLED,
        )

        with patch(
            "apps.platform.organizations.services.organization_module.EntitlementService.has_module",
            return_value=False,
        ):
            with self.assertRaises(ValidationError) as exc:
                enable_module(instance=module)

        self.assertEqual(
            exc.exception.message_dict["code"][0],
            "module_not_entitled",
        )

    def test_enable_allows_purchased_module(self):
        organization = SimpleNamespace(pk="org-2")
        module = MagicMock(
            organization=organization,
            module_code="PHARMACY",
            status=OrganizationModule.Status.DISABLED,
        )

        with patch(
            "apps.platform.organizations.services.organization_module.EntitlementService.has_module",
            return_value=True,
        ):
            result = enable_module(instance=module)

        self.assertEqual(
            result.status,
            OrganizationModule.Status.ENABLED,
        )

    def test_update_cannot_turn_unentitled_module_on(self):
        organization = SimpleNamespace(pk="org-3")
        module = SimpleNamespace(
            organization=organization,
            module_code="LABORATORY",
            status=OrganizationModule.Status.DISABLED,
        )

        with patch(
            "apps.platform.organizations.services.organization_module.EntitlementService.has_module",
            return_value=False,
        ):
            with self.assertRaises(ValidationError):
                update_module(
                    instance=module,
                    validated_data={
                        "status": OrganizationModule.Status.ENABLED,
                    },
                )

    @patch(
        "apps.platform.organizations.services.organization_module.OrganizationModule.objects"
    )
    @patch(
        "apps.platform.organizations.services.organization_module.EntitlementService.has_module",
        return_value=False,
    )
    def test_create_defaults_to_enabled_and_blocks_unentitled(
        self,
        entitlement,
        objects,
    ):
        organization = SimpleNamespace(pk="org-4")

        with self.assertRaises(ValidationError):
            create_module(
                validated_data={
                    "organization": organization,
                    "module_code": "IMAGING",
                },
            )

        objects.create.assert_not_called()
        entitlement.assert_called_once_with(
            organization=organization,
            module="IMAGING",
        )
