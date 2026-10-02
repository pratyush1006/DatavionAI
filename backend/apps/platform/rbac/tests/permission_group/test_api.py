"""
Tests for PermissionGroup API.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.platform.rbac.tests.factories import (
    PermissionGroupFactory,
)

User = get_user_model()


class PermissionGroupAPITestCase(
    APITestCase,
):
    """
    Tests for PermissionGroup API.
    """

    def setUp(
        self,
    ) -> None:
        """
        Test setup.
        """

        self.user = User.objects.create_superuser(
            email="admin@datavion.ai",
            password="Password@123",
        )

        self.client.force_authenticate(
            self.user,
        )

        self.list_url = reverse(
            "rbac-api:permission-groups:permission-group-list",
        )

    def test_list_permission_groups(
        self,
    ) -> None:
        """
        Should list permission groups.
        """

        PermissionGroupFactory.create_batch(
            3,
        )

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_create_permission_group(
        self,
    ) -> None:
        """
        Should create a permission group.
        """

        payload = {
            "name": "Clinical Operations",
            "module": "patients",
            "description": "Clinical permissions.",
            "is_system": True,
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_retrieve_permission_group(
        self,
    ) -> None:
        """
        Should retrieve a permission group.
        """

        permission_group = PermissionGroupFactory()

        response = self.client.get(
            reverse(
                "rbac-api:permission-groups:permission-group-detail",
                kwargs={
                    "uuid": permission_group.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_permission_group(
        self,
    ) -> None:
        """
        Should update a permission group.
        """

        permission_group = PermissionGroupFactory()

        response = self.client.patch(
            reverse(
                "rbac-api:permission-groups:permission-group-detail",
                kwargs={
                    "uuid": permission_group.id,
                },
            ),
            {
                "description": "Updated description.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_permission_group(
        self,
    ) -> None:
        """
        Should delete a permission group.
        """

        permission_group = PermissionGroupFactory()

        response = self.client.delete(
            reverse(
                "rbac-api:permission-groups:permission-group-detail",
                kwargs={
                    "uuid": permission_group.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )


__all__ = [
    "PermissionGroupAPITestCase",
]
