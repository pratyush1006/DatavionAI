"""
Tests for storage services.
"""

from __future__ import annotations

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.accounts.models import User
from apps.organizations.models import Organization
from apps.storage.constants import (
    ASSET_CATEGORY_DOCUMENT,
    ASSET_STATUS_DELETED,
    ASSET_STATUS_READY,
    ASSET_VISIBILITY_PRIVATE,
)
from apps.storage.models import (
    Asset,
    Folder,
)
from apps.storage.services.asset import (
    change_asset_status,
    change_asset_visibility,
    move_asset,
    update_asset,
)
from apps.storage.services.delete import delete_asset
from apps.storage.services.upload import upload_asset


class AssetServiceTestCase(TestCase):
    """
    Tests for asset services.
    """

    def setUp(self):
        self.organization = Organization.objects.create(
            name="Test Organization",
        )

        self.user = User.objects.create_user(
            email="user@example.com",
            password="password",
        )

        self.folder = Folder.objects.create(
            organization=self.organization,
            name="Documents",
        )

    def create_uploaded_file(self):
        """
        Create a sample uploaded file.
        """

        return SimpleUploadedFile(
            "report.pdf",
            b"Sample PDF content",
            content_type="application/pdf",
        )

    def test_upload_asset(self):
        """
        Uploading an asset should create metadata.
        """

        uploaded_file = self.create_uploaded_file()

        asset = upload_asset(
            organization=self.organization,
            uploaded_by=self.user,
            file=uploaded_file,
            original_name=uploaded_file.name,
            mime_type=uploaded_file.content_type,
            category=ASSET_CATEGORY_DOCUMENT,
            folder=self.folder,
            visibility=ASSET_VISIBILITY_PRIVATE,
        )

        self.assertIsInstance(
            asset,
            Asset,
        )

        self.assertEqual(
            asset.original_name,
            "report.pdf",
        )

        self.assertEqual(
            asset.status,
            ASSET_STATUS_READY,
        )

    def test_update_asset(self):
        """
        Asset metadata should be updated.
        """

        asset = Asset.objects.create(
            organization=self.organization,
            uploaded_by=self.user,
            name="Old",
            original_name="old.pdf",
            extension="pdf",
            mime_type="application/pdf",
            category=ASSET_CATEGORY_DOCUMENT,
            size=100,
            provider="LOCAL",
            storage_key="old.pdf",
            path="old.pdf",
            checksum="abc",
            visibility=ASSET_VISIBILITY_PRIVATE,
            status=ASSET_STATUS_READY,
        )

        update_asset(
            asset=asset,
            name="New",
        )

        asset.refresh_from_db()

        self.assertEqual(
            asset.name,
            "New",
        )

    def test_move_asset(self):
        """
        Asset should move between folders.
        """

        folder2 = Folder.objects.create(
            organization=self.organization,
            name="Reports",
        )

        asset = Asset.objects.create(
            organization=self.organization,
            uploaded_by=self.user,
            name="Report",
            original_name="report.pdf",
            extension="pdf",
            mime_type="application/pdf",
            category=ASSET_CATEGORY_DOCUMENT,
            size=100,
            provider="LOCAL",
            storage_key="report.pdf",
            path="report.pdf",
            checksum="abc",
            visibility=ASSET_VISIBILITY_PRIVATE,
            status=ASSET_STATUS_READY,
            folder=self.folder,
        )

        move_asset(
            asset=asset,
            folder=folder2,
        )

        asset.refresh_from_db()

        self.assertEqual(
            asset.folder,
            folder2,
        )

    def test_change_visibility(self):
        """
        Asset visibility should be updated.
        """

        asset = Asset.objects.create(
            organization=self.organization,
            uploaded_by=self.user,
            name="Report",
            original_name="report.pdf",
            extension="pdf",
            mime_type="application/pdf",
            category=ASSET_CATEGORY_DOCUMENT,
            size=100,
            provider="LOCAL",
            storage_key="report.pdf",
            path="report.pdf",
            checksum="abc",
            visibility=ASSET_VISIBILITY_PRIVATE,
            status=ASSET_STATUS_READY,
        )

        change_asset_visibility(
            asset=asset,
            visibility="PUBLIC",
        )

        asset.refresh_from_db()

        self.assertEqual(
            asset.visibility,
            "PUBLIC",
        )

    def test_change_status(self):
        """
        Asset status should be updated.
        """

        asset = Asset.objects.create(
            organization=self.organization,
            uploaded_by=self.user,
            name="Report",
            original_name="report.pdf",
            extension="pdf",
            mime_type="application/pdf",
            category=ASSET_CATEGORY_DOCUMENT,
            size=100,
            provider="LOCAL",
            storage_key="report.pdf",
            path="report.pdf",
            checksum="abc",
            visibility=ASSET_VISIBILITY_PRIVATE,
            status=ASSET_STATUS_READY,
        )

        change_asset_status(
            asset=asset,
            status=ASSET_STATUS_DELETED,
        )

        asset.refresh_from_db()

        self.assertEqual(
            asset.status,
            ASSET_STATUS_DELETED,
        )

    def test_delete_asset(self):
        """
        Asset should be soft deleted.
        """

        asset = Asset.objects.create(
            organization=self.organization,
            uploaded_by=self.user,
            name="Report",
            original_name="report.pdf",
            extension="pdf",
            mime_type="application/pdf",
            category=ASSET_CATEGORY_DOCUMENT,
            size=100,
            provider="LOCAL",
            storage_key="report.pdf",
            path="report.pdf",
            checksum="abc",
            visibility=ASSET_VISIBILITY_PRIVATE,
            status=ASSET_STATUS_READY,
        )

        delete_asset(
            asset=asset,
        )

        asset.refresh_from_db()

        self.assertFalse(
            asset.is_active,
        )

        self.assertEqual(
            asset.status,
            ASSET_STATUS_DELETED,
        )
