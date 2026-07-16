"""
Tests for Permission API.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.platform.rbac.constants import (
    PermissionAction,
    PermissionModule,
    PermissionScope,
)
from apps.platform.rbac.tests.factories.permission import (
    create_permission,
)

User = get_user_model()


class PermissionAPITestCase(
    APITestCase,
):
    """
    Tests for Permission API.
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
            "rbac-api:permissions:permission-list",
        )

    def test_list_permissions(
        self,
    ) -> None:
        """
        List permissions.
        """

        create_permission()

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_create_permission(
        self,
    ) -> None:
        """
        Create permission.
        """

        response = self.client.post(
            self.list_url,
            {
                "module": PermissionModule.PATIENTS,
                "action": PermissionAction.VIEW,
                "scope": PermissionScope.ORGANIZATION,
            },
            format="json",
        )
        print(response.status_code)
        print(response.data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_detail_permission(
        self,
    ) -> None:
        """
        Retrieve permission.
        """

        permission = create_permission()

        url = reverse(
            "rbac-api:permissions:permission-detail",
            kwargs={
                "permission_id": permission.id,
            },
        )

        response = self.client.get(
            url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_permission(
        self,
    ) -> None:
        """
        Update permission.
        """

        permission = create_permission()

        url = reverse(
            "rbac-api:permissions:permission-detail",
            kwargs={
                "permission_id": permission.id,
            },
        )

        response = self.client.patch(
            url,
            {
                "action": PermissionAction.UPDATE,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_permission(
        self,
    ) -> None:
        """
        Delete permission.
        """

        permission = create_permission()

        url = reverse(
            "rbac-api:permissions:permission-detail",
            kwargs={
                "permission_id": permission.id,
            },
        )

        response = self.client.delete(
            url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )


__all__ = [
    "PermissionAPITestCase",
]
