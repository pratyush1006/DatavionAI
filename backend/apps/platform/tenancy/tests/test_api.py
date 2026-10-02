"""
Tenant API tests.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework.test import APITestCase


class TenantAPITestCase(
    APITestCase,
):
    def test_tenant_list_endpoint_exists(self):

        url = reverse(
            "tenancy:tenant-list",
        )

        response = self.client.get(
            url,
        )

        self.assertIn(
            response.status_code,
            (
                401,
                403,
            ),
        )
