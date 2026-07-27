"""
Tenant membership tests.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.platform.tenancy.models import (
    Tenant,
    TenantMembership,
)
from apps.platform.tenancy.services import (
    TenantMembershipService,
)

User = get_user_model()


class TenantMembershipTestCase(
    TestCase,
):
    """
    Test tenant membership lifecycle.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            email="tenant-user@datavion.ai",
            password="password123",
        )

        self.tenant = Tenant.objects.create(
            name="Apollo Clinic",
            slug="apollo-clinic",
        )

    def test_create_membership(self):

        membership = TenantMembershipService.create_membership(
            tenant=self.tenant,
            user=self.user,
        )

        self.assertEqual(
            membership.tenant,
            self.tenant,
        )

        self.assertEqual(
            membership.user,
            self.user,
        )

        self.assertEqual(
            membership.status,
            TenantMembership.Status.ACTIVE,
        )

    def test_suspend_membership(self):

        membership = TenantMembershipService.create_membership(
            tenant=self.tenant,
            user=self.user,
        )

        TenantMembershipService.suspend_membership(
            membership,
        )

        membership.refresh_from_db()

        self.assertEqual(
            membership.status,
            TenantMembership.Status.SUSPENDED,
        )

    def test_remove_membership(self):

        membership = TenantMembershipService.create_membership(
            tenant=self.tenant,
            user=self.user,
        )

        TenantMembershipService.remove_membership(
            membership,
        )

        membership.refresh_from_db()

        self.assertEqual(
            membership.status,
            TenantMembership.Status.REMOVED,
        )
