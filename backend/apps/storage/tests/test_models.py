"""
Tests for storage models.
"""

from __future__ import annotations

from django.test import TestCase

from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.storage.constants import (
    ASSET_CATEGORY_DOCUMENT,
    ASSET_STATUS_READY,
    ASSET_VISIBILITY_PRIVATE,
    STORAGE_PROVIDER_LOCAL,
)
from apps.storage.models import (
    Asset,
    Folder,
)


class FolderModelTestCase(TestCase):
    """
    Tests for the Folder model.
    """

    def setUp(self):
        self.organization = Organization.objects.create(
            name="Test Organization",
        )

    def test_folder_str_returns_full_path(self):
        """
        __str__ should return the folder full path.
        """

        parent = Folder.objects.create(
            organization=self.organization,
            name="Documents",
        )

        child = Folder.objects.create(
            organization=self.organization,
            parent=parent,
            name="Reports",
        )

        self.assertEqual(
            str(child),
            "Documents/Reports",
        )

    def test_root_folder_full_path(self):
        """
        Root folder should return its own name.
        """

        folder = Folder.objects.create(
            organization=self.organization,
            name="Images",
        )

        self.assertEqual(
            folder.full_path,
            "Images",
        )


class AssetModelTestCase(TestCase):
    """
    Tests for the Asset model.
    """

    def setUp(self):
        self.organization = Organization.objects.create(
            name="Test Organization",
        )

        self.user = User.objects.create_user(
            email="user@example.com",
            password="password",
        )

    def test_asset_string_representation(self):
        """
        __str__ should return the original filename.
        """

        asset = Asset.objects.create(
            organization=self.organization,
            uploaded_by=self.user,
            name="report",
            original_name="report.pdf",
            extension="pdf",
            mime_type="application/pdf",
            category=ASSET_CATEGORY_DOCUMENT,
            size=1024,
            provider=STORAGE_PROVIDER_LOCAL,
            storage_key="reports/report.pdf",
            path="reports/report.pdf",
            checksum="abc123",
            visibility=ASSET_VISIBILITY_PRIVATE,
            status=ASSET_STATUS_READY,
        )

        self.assertEqual(
            str(asset),
            "report.pdf",
        )

    def test_asset_defaults(self):
        """
        Asset should use the expected default values.
        """

        asset = Asset.objects.create(
            organization=self.organization,
            uploaded_by=self.user,
            name="report",
            original_name="report.pdf",
            extension="pdf",
            mime_type="application/pdf",
            size=100,
            storage_key="reports/report.pdf",
            path="reports/report.pdf",
            checksum="checksum",
        )

        self.assertEqual(
            asset.category,
            ASSET_CATEGORY_DOCUMENT,
        )

        self.assertEqual(
            asset.visibility,
            ASSET_VISIBILITY_PRIVATE,
        )

        self.assertEqual(
            asset.status,
            ASSET_STATUS_READY,
        )

        self.assertEqual(
            asset.provider,
            STORAGE_PROVIDER_LOCAL,
        )
