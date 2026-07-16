"""
Tests for Storage API.
"""

from __future__ import annotations

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.storage.constants import (
    ASSET_CATEGORY_DOCUMENT,
    ASSET_STATUS_READY,
    ASSET_VISIBILITY_PRIVATE,
)
from apps.storage.models import (
    Asset,
    Folder,
)


class StorageAPITestCase(APITestCase):
    """
    Tests for Storage API endpoints.
    """

    def setUp(self):
        self.organization = Organization.objects.create(
            name="Test Organization",
        )

        self.user = User.objects.create_user(
            email="user@example.com",
            password="password",
            organization=self.organization,
        )

        self.client.force_authenticate(
            user=self.user,
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
            provider="LOCAL",
            storage_key="documents/report.pdf",
            path="documents/report.pdf",
            checksum="checksum",
            visibility=ASSET_VISIBILITY_PRIVATE,
            status=ASSET_STATUS_READY,
        )

    def test_list_assets(self):
        """
        Should return asset list.
        """

        response = self.client.get(
            reverse("storage-api:asset-list-create"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            len(response.data["data"]),
            1,
        )

    def test_retrieve_asset(self):
        """
        Should return asset details.
        """

        response = self.client.get(
            reverse(
                "storage-api:asset-detail",
                kwargs={
                    "pk": self.asset.pk,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            response.data["data"]["id"],
            str(self.asset.id),
        )

    def test_upload_asset(self):
        """
        Should upload an asset.
        """

        upload = SimpleUploadedFile(
            "document.pdf",
            b"Sample content",
            content_type="application/pdf",
        )

        response = self.client.post(
            reverse("storage-api:asset-list-create"),
            {
                "file": upload,
                "folder": self.folder.pk,
                "category": ASSET_CATEGORY_DOCUMENT,
                "visibility": ASSET_VISIBILITY_PRIVATE,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_update_asset(self):
        """
        Should update asset metadata.
        """

        response = self.client.patch(
            reverse(
                "storage-api:asset-detail",
                kwargs={
                    "pk": self.asset.pk,
                },
            ),
            {
                "name": "Updated Report",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.asset.refresh_from_db()

        self.assertEqual(
            self.asset.name,
            "Updated Report",
        )

    def test_delete_asset(self):
        """
        Should soft delete an asset.
        """

        response = self.client.delete(
            reverse(
                "storage-api:asset-detail",
                kwargs={
                    "pk": self.asset.pk,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.asset.refresh_from_db()

        self.assertFalse(
            self.asset.is_active,
        )

    def test_authentication_required(self):
        """
        Anonymous users should not access the API.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            reverse("storage-api:asset-list-create"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
