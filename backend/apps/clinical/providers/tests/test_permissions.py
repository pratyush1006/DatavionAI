"""
Tests for provider permissions.
"""

from __future__ import annotations

from apps.clinical.providers.permissions import (
    CanCreateProvider,
    CanDeleteProvider,
    CanUpdateProvider,
    CanViewProvider,
    ProviderPermission,
)
from apps.common.tests.base import BaseTestCase


class ProviderPermissionTestCase(BaseTestCase):
    """
    Tests for provider permissions.
    """

    def test_permission_constants(
        self,
    ) -> None:
        """
        Permission constants should exist.
        """

        self.assertEqual(
            ProviderPermission.VIEW,
            "clinical.providers.view_provider",
        )

        self.assertEqual(
            ProviderPermission.CREATE,
            "clinical.providers.create_provider",
        )

        self.assertEqual(
            ProviderPermission.UPDATE,
            "clinical.providers.update_provider",
        )

        self.assertEqual(
            ProviderPermission.DELETE,
            "clinical.providers.delete_provider",
        )

    def test_permission_classes(
        self,
    ) -> None:
        """
        Permission classes should expose permission_code.
        """

        self.assertEqual(
            CanViewProvider.permission_code,
            ProviderPermission.VIEW,
        )

        self.assertEqual(
            CanCreateProvider.permission_code,
            ProviderPermission.CREATE,
        )

        self.assertEqual(
            CanUpdateProvider.permission_code,
            ProviderPermission.UPDATE,
        )

        self.assertEqual(
            CanDeleteProvider.permission_code,
            ProviderPermission.DELETE,
        )


__all__ = [
    "ProviderPermissionTestCase",
]
