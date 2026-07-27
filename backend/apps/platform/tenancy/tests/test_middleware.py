"""
Tenant middleware tests.
"""

from __future__ import annotations

from django.test import RequestFactory, TestCase

from apps.platform.tenancy.middleware import (
    TenantMiddleware,
)


class TenantMiddlewareTestCase(
    TestCase,
):
    def test_middleware_exists(self):

        factory = RequestFactory()

        request = factory.get(
            "/",
        )

        middleware = TenantMiddleware(
            lambda request: request,
        )

        response = middleware(
            request,
        )

        self.assertIsNotNone(
            response,
        )
