"""Tests for Billing RBAC delegation."""

from __future__ import annotations

from unittest.mock import patch

from django.test import SimpleTestCase

from apps.billing.foundation.exceptions import BillingPermissionError
from apps.billing.foundation.permissions import BillingPermission
from apps.billing.foundation.rbac import require_billing_permission


class BillingPermissionTests(SimpleTestCase):
    """Verify canonical RBAC delegation."""

    @patch("apps.billing.foundation.rbac.user_has_permission", return_value=True)
    def test_delegates_to_platform_rbac(self, mock_permission) -> None:
        """Delegate exact permission checks."""
        user = object()
        organization = object()
        require_billing_permission(
            user=user,
            permission=BillingPermission.INVOICE_VIEW,
            organization=organization,
        )
        mock_permission.assert_called_once_with(
            user=user,
            permission=BillingPermission.INVOICE_VIEW,
            organization=organization,
        )

    @patch("apps.billing.foundation.rbac.user_has_permission", return_value=False)
    def test_denial_raises(self, mock_permission) -> None:
        """Raise a Billing permission error on denial."""
        with self.assertRaises(BillingPermissionError):
            require_billing_permission(
                user=object(),
                permission=BillingPermission.INVOICE_VIEW,
                organization=object(),
            )


__all__ = ["BillingPermissionTests"]
