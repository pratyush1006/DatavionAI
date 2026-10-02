"""
Provider policy tests.

Validates provider authorization rules.

Coverage:

- Create permission
- Update permission
- Delete permission
- Verify permission
- Activate permission
- Deactivate permission
- Assign permission
"""

from __future__ import annotations

from uuid import uuid4

from django.test import TestCase

from apps.clinical.providers.policies import (
    ProviderPolicy,
)
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.rbac.models import (
    OrganizationRole,
    Permission,
    Role,
    RolePermission,
)
from apps.platform.tenancy.models import Tenant


class ProviderPolicyTestCase(
    TestCase,
):
    """
    Provider RBAC policy tests.
    """

    def setUp(self):

        self.tenant = Tenant.objects.create(
            name="Datavion Test Tenant",
            slug=(f"tenant-{uuid4().hex[:8]}"),
            tenant_type="ORGANIZATION",
            status="ACTIVE",
        )

        self.organization = Organization.objects.create(
            tenant=self.tenant,
            name="Datavion Healthcare",
            display_name="Datavion Healthcare",
            code=(f"DVT-{uuid4().hex[:6].upper()}"),
            slug=(f"clinic-{uuid4().hex[:8]}"),
            organization_type="CLINIC",
            status="ACTIVE",
            email="clinic@datavion.test",
        )

        self.user = User.objects.create_user(
            email="provider.admin@datavion.test",
            password="TestPassword@123",
        )

        self.denied_user = User.objects.create_user(
            email="provider.denied@datavion.test",
            password="TestPassword@123",
        )

        self.role = Role.objects.create(
            name="Provider Manager",
            code="provider_manager",
        )

        self.permissions = {}

        permission_codes = [
            "providers.create",
            "providers.update",
            "providers.delete",
            "providers.verify",
            "providers.activate",
            "providers.deactivate",
            "providers.assign",
        ]

        for code in permission_codes:
            module, action = code.split(".")

            permission = Permission.objects.create(
                code=code,
                module=module,
                action=action,
                scope="organization",
                name=code.replace(
                    ".",
                    " ",
                ).title(),
            )

            self.permissions[code] = permission

            RolePermission.objects.create(
                role=self.role,
                permission=permission,
            )

        OrganizationRole.objects.create(
            organization=self.organization,
            user=self.user,
            role=self.role,
            is_primary=True,
        )

        self.policy = ProviderPolicy()

    def test_create_permission_allowed(self):

        self.assertTrue(
            self.policy.can_create(
                actor=self.user,
                organization=self.organization,
            ),
        )

    def test_create_permission_denied(self):

        self.assertFalse(
            self.policy.can_create(
                actor=self.denied_user,
                organization=self.organization,
            ),
        )

    def test_all_provider_permissions_allowed(self):

        checks = [
            self.policy.can_update,
            self.policy.can_delete,
            self.policy.can_verify,
            self.policy.can_activate,
            self.policy.can_deactivate,
            self.policy.can_assign,
        ]

        for check in checks:
            self.assertTrue(
                check(
                    actor=self.user,
                    organization=self.organization,
                ),
            )

    def test_all_provider_permissions_denied(self):

        checks = [
            self.policy.can_update,
            self.policy.can_delete,
            self.policy.can_verify,
            self.policy.can_activate,
            self.policy.can_deactivate,
            self.policy.can_assign,
        ]

        for check in checks:
            self.assertFalse(
                check(
                    actor=self.denied_user,
                    organization=self.organization,
                ),
            )
