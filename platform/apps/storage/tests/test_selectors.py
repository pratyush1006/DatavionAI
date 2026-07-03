"""
Tests for storage selectors.
"""

from __future__ import annotations

from django.test import TestCase

from apps.accounts.models import User
from apps.organizations.models import Organization
from apps.storage.constants import (
    ASSET_CATEGORY_DOCUMENT,
    ASSET_CATEGORY_IMAGE,
    ASSET_STATUS_DELETED,
    ASSET_STATUS_READY,
    ASSET_VISIBILITY_PRIVATE,
    STORAGE_PROVIDER_LOCAL,
)
from apps.storage.models import (
    Asset,
    Folder,
)
from apps.storage.selectors.asset import (
    get_asset,
    get_assets,
    get_assets_by_category,
    get_assets_by_provider,
    get_assets_by_status,
    get_folder_assets,
    get_organization_assets,
    search_assets,
)


class AssetSelectorTestCase(TestCase):
    """
    Tests for asset selectors.
    """

    def setUp(self):
        self.organization = Organization.objects.create(
            name="Organization A",
            code="ORG_A",
        )

        self.other_organization = Organization.objects.create(
            name="Organization B",
            code="ORG_B",
        )

        self.user = User.objects.create_user(
            email="user@example.com",
            password="password",
            organization=self.organization,
        )

        self.folder = Folder.objects.create(
            organization=self.organization,
            name="Documents",
        )

        self.asset = Asset.objects.create(
            organization=self.organization,
            uploaded_by=self.user,
            folder=self.folder,
            name="Report",
            original_name="report.pdf",
            extension="pdf",
            mime_type="application/pdf",
            category=ASSET_CATEGORY_DOCUMENT,
            size=100,
            provider=STORAGE_PROVIDER_LOCAL,
            storage_key="documents/report.pdf",
            path="documents/report.pdf",
            checksum="checksum-1",
            visibility=ASSET_VISIBILITY_PRIVATE,
            status=ASSET_STATUS_READY,
        )

        self.image_asset = Asset.objects.create(
            organization=self.organization,
            uploaded_by=self.user,
            name="Logo",
            original_name="logo.png",
            extension="png",
            mime_type="image/png",
            category=ASSET_CATEGORY_IMAGE,
            size=200,
            provider=STORAGE_PROVIDER_LOCAL,
            storage_key="images/logo.png",
            path="images/logo.png",
            checksum="checksum-2",
            visibility=ASSET_VISIBILITY_PRIVATE,
            status=ASSET_STATUS_DELETED,
        )

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="password",
            organization=self.other_organization,
        )

        self.other_asset = Asset.objects.create(
            organization=self.other_organization,
            uploaded_by=self.other_user,
            name="Other",
            original_name="other.pdf",
            extension="pdf",
            mime_type="application/pdf",
            category=ASSET_CATEGORY_DOCUMENT,
            size=150,
            provider=STORAGE_PROVIDER_LOCAL,
            storage_key="other/report.pdf",
            path="other/report.pdf",
            checksum="checksum-3",
            visibility=ASSET_VISIBILITY_PRIVATE,
            status=ASSET_STATUS_READY,
        )

    def test_get_asset(self):
        """
        Should return the requested asset.
        """

        asset = get_asset(
            asset_id=self.asset.id,
            organization=self.organization,
        )

        self.assertEqual(
            asset,
            self.asset,
        )

    def test_get_assets(self):
        """
        Should return active assets.
        """

        queryset = get_assets()

        self.assertIn(
            self.asset,
            queryset,
        )

    def test_get_organization_assets(self):
        """
        Should return only organization assets.
        """

        queryset = get_organization_assets(
            organization=self.organization,
        )

        self.assertIn(
            self.asset,
            queryset,
        )

        self.assertNotIn(
            self.other_asset,
            queryset,
        )

    def test_get_folder_assets(self):
        """
        Should return assets within a folder.
        """

        queryset = get_folder_assets(
            folder=self.folder,
        )

        self.assertIn(
            self.asset,
            queryset,
        )

    def test_get_assets_by_category(self):
        """
        Should filter assets by category.
        """

        queryset = get_assets_by_category(
            organization=self.organization,
            category=ASSET_CATEGORY_DOCUMENT,
        )

        self.assertIn(
            self.asset,
            queryset,
        )

        self.assertNotIn(
            self.image_asset,
            queryset,
        )

    def test_get_assets_by_status(self):
        """
        Should filter assets by status.
        """

        queryset = get_assets_by_status(
            organization=self.organization,
            status=ASSET_STATUS_READY,
        )

        self.assertIn(
            self.asset,
            queryset,
        )

        self.assertNotIn(
            self.image_asset,
            queryset,
        )

    def test_get_assets_by_provider(self):
        """
        Should filter assets by provider.
        """

        queryset = get_assets_by_provider(
            organization=self.organization,
            provider=STORAGE_PROVIDER_LOCAL,
        )

        self.assertIn(
            self.asset,
            queryset,
        )

    def test_search_assets(self):
        """
        Should search assets by filename.
        """

        queryset = search_assets(
            organization=self.organization,
            query="report",
        )

        self.assertIn(
            self.asset,
            queryset,
        )

        self.assertNotIn(
            self.other_asset,
            queryset,
        )
