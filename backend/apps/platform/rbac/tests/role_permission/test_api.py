"""
Tests for the RolePermission API.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.platform.rbac.constants import (
    RolePermissionSource,
    RolePermissionType,
)
from apps.platform.rbac.tests.factories import (
    PermissionFactory,
    RoleFactory,
    RolePermissionFactory,
)

User = get_user_model()


class RolePermissionAPITestCase(
    APITestCase,
):
    """
    Tests for the RolePermission API.
    """

    def setUp(
        self,
    ) -> None:
        """
        Set up test data.
        """

        super().setUp()

        self.user = User.objects.create_user(
            email="admin@datavion.ai",
            password="password123",
        )

        self.client.force_authenticate(
            user=self.user,
        )

        self.list_url = reverse(
            "rbac-api:role-permissions:list-create",
        )

    def test_should_list_role_permissions(
        self,
    ) -> None:
        """
        GET should return role permissions.
        """

        RolePermissionFactory()

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_should_create_role_permission(
        self,
    ) -> None:
        """
        POST should create a role permission.
        """

        role = RoleFactory()

        permission = PermissionFactory()

        payload = {
            "role": role.id,
            "permission": permission.id,
            "assignment_type": RolePermissionType.DIRECT,
            "assignment_source": RolePermissionSource.SYSTEM,
            "is_active": True,
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

    def test_should_retrieve_role_permission(
        self,
    ) -> None:
        """
        GET detail should retrieve a role permission.
        """

        role_permission = RolePermissionFactory()

        url = reverse(
            "rbac-api:role-permissions:retrieve-update-destroy",
            kwargs={
                "id": role_permission.id,
            },
        )

        response = self.client.get(
            url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_should_update_role_permission(
        self,
    ) -> None:
        """
        PATCH should update a role permission.
        """

        role_permission = RolePermissionFactory()

        url = reverse(
            "rbac-api:role-permissions:retrieve-update-destroy",
            kwargs={
                "id": role_permission.id,
            },
        )

        payload = {
            "is_active": False,
        }

        response = self.client.patch(
            url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_should_delete_role_permission(
        self,
    ) -> None:
        """
        DELETE should remove a role permission.
        """

        role_permission = RolePermissionFactory()

        url = reverse(
            "rbac-api:role-permissions:retrieve-update-destroy",
            kwargs={
                "id": role_permission.id,
            },
        )

        response = self.client.delete(
            url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_should_return_not_found(
        self,
    ) -> None:
        """
        Unknown role permission should return 404.
        """

        import uuid

        url = reverse(
            "rbac-api:role-permissions:retrieve-update-destroy",
            kwargs={
                "id": uuid.uuid4(),
            },
        )

        response = self.client.get(
            url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_should_reject_invalid_payload(
        self,
    ) -> None:
        """
        Invalid payload should return 400.
        """

        response = self.client.post(
            self.list_url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
