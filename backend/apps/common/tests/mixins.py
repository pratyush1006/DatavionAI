"""
Common API test mixins.

Provides:

- User creation
- Authentication
- Tenant context
- Organization context
"""

from __future__ import annotations

from apps.accounts.models import User
from apps.common.tests.tenant import (
    create_test_tenant_context,
)


class TenantTestMixin:
    """
    Multi tenant test helper.
    """

    def setup_tenant_context(
        self,
    ):
        """
        Create tenant organization context.
        """

        self.organization = create_test_tenant_context()

        self.tenant = self.organization.tenant

    def setup_test_user(
        self,
    ):
        """
        Create authenticated user.
        """

        self.user = User.objects.create_user(
            email="test@datavion.com",
            password="Test@12345",
        )

    def authenticate_test_user(
        self,
    ):
        """
        Authenticate API client.
        """

        self.client.force_authenticate(
            user=self.user,
        )

    def set_tenant_header(
        self,
    ):
        """
        Inject organization header.
        """

        self.client.credentials(HTTP_X_ORGANIZATION_ID=str(self.organization.id))


__all__ = [
    "TenantTestMixin",
]
