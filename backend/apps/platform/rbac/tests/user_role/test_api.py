"""
Tests for the UserRole API.
"""

from __future__ import annotations

from apps.platform.rbac.tests.factories import (
    RoleFactory,
    UserRoleFactory,
)
from apps.platform.rbac.tests.factories.user_role import UserFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserRoleAPITestCase(
    APITestCase,
):
    """
    Tests for the UserRole API.
    """

    def setUp(
        self,
    ) -> None:
        """
        Test setup.
        """

        self.user = UserFactory(
            is_superuser=True,
            is_staff=True,
        )

        self.client.force_authenticate(
            self.user,
        )

        self.role = RoleFactory()

        self.assignment = UserRoleFactory()

        self.list_url = reverse(
            "rbac-api:user-role-api:list-create",
        )

    def test_should_list_user_roles(
        self,
    ) -> None:
        """
        GET should return user roles.
        """

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_should_retrieve_user_role(
        self,
    ) -> None:
        """
        GET detail should return a user role.
        """

        response = self.client.get(
            reverse(
                "rbac-api:user-role-api:detail",
                kwargs={
                    "id": self.assignment.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_should_create_user_role(
        self,
    ) -> None:
        """
        POST should create a user role.
        """

        payload = {
            "user": UserFactory().id,
            "role": RoleFactory().id,
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

    def test_should_update_user_role(
        self,
    ) -> None:
        """
        PATCH should update a user role.
        """

        response = self.client.patch(
            reverse(
                "rbac-api:user-role-api:detail",
                kwargs={
                    "id": self.assignment.id,
                },
            ),
            {
                "is_active": False,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_should_delete_user_role(
        self,
    ) -> None:
        """
        DELETE should delete a user role.
        """

        response = self.client.delete(
            reverse(
                "rbac-api:user-role-api:detail",
                kwargs={
                    "id": self.assignment.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_should_return_not_found(
        self,
    ) -> None:
        """
        Unknown user role should return 404.
        """

        response = self.client.get(
            reverse(
                "rbac-api:user-role-api:detail",
                kwargs={
                    "id": "00000000-0000-0000-0000-000000000000",
                },
            ),
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


__all__ = [
    "UserRoleAPITestCase",
]
