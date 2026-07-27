"""
Tenant permission tests.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from apps.platform.tenancy.permissions import (
    HasTenantAccess,
    IsPlatformAdmin,
)

User = get_user_model()


class TenantPermissionTestCase(
    TestCase,
):
    def setUp(self):

        self.factory = APIRequestFactory()

    def test_platform_admin_permission(self):

        user = User(
            username="admin",
            is_staff=True,
        )

        request = self.factory.get("/")

        request.user = user

        permission = IsPlatformAdmin()

        self.assertTrue(
            permission.has_permission(
                request,
                None,
            )
        )

    def test_anonymous_denied(self):

        request = self.factory.get("/")

        permission = HasTenantAccess()

        self.assertFalse(
            permission.has_permission(
                request,
                None,
            )
        )
