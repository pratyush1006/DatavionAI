"""
Tenant model tests.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.tenancy.models import Tenant


class TenantModelTestCase(
    TestCase,
):
    def test_tenant_string_representation(self):

        tenant = Tenant(
            name="Apollo Clinic",
            slug="apollo-clinic",
        )

        self.assertEqual(
            str(tenant),
            "Apollo Clinic",
        )

    def test_default_values_exist(self):

        tenant = Tenant(
            name="Test Clinic",
            slug="test-clinic",
        )

        self.assertIsNotNone(
            tenant.tenant_type,
        )
