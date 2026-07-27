"""
Tenant context tests.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.tenancy.context import (
    clear_current_tenant,
    get_current_tenant,
    set_current_tenant,
)
from apps.platform.tenancy.models import Tenant


class TenantContextTestCase(
    TestCase,
):
    """
    Test tenant ContextVar lifecycle.
    """

    def setUp(self):
        self.tenant = Tenant(
            name="Demo Clinic",
            slug="demo-clinic",
        )

    def tearDown(self):
        clear_current_tenant()

    def test_set_current_tenant(self):

        set_current_tenant(
            self.tenant,
        )

        current = get_current_tenant()

        self.assertEqual(
            current,
            self.tenant,
        )

    def test_clear_current_tenant(self):

        set_current_tenant(
            self.tenant,
        )

        clear_current_tenant()

        self.assertIsNone(
            get_current_tenant(),
        )
