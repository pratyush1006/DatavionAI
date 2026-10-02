"""
Tenant selector tests.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.platform.tenancy.models import (
    Tenant,
    TenantMembership,
)
from apps.platform.tenancy.selectors import (
    get_tenant_membership,
    list_tenant_memberships,
)

User = get_user_model()


class TenantSelectorTestCase(
    TestCase,
):
    """
    Test tenancy read operations.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            email="selector@datavion.ai",
            password="password123",
        )

        self.tenant = Tenant.objects.create(
            name="Apollo Clinic",
            slug="apollo-clinic",
        )

        self.membership = TenantMembership.objects.create(
            tenant=self.tenant,
            user=self.user,
            status=(TenantMembership.Status.ACTIVE),
        )

    def test_list_tenant_memberships(self):

        memberships = list_tenant_memberships(
            self.tenant.id,
        )

        self.assertEqual(
            memberships.count(),
            1,
        )

    def test_get_tenant_membership(self):

        membership = get_tenant_membership(
            tenant_id=self.tenant.id,
            user_id=self.user.id,
        )

        self.assertEqual(
            membership,
            self.membership,
        )
