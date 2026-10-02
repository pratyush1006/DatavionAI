"""
Tests for the Role API.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.platform.rbac.tests.factories import (
    create_role,
)

User = get_user_model()


class RoleAPITestCase(
    APITestCase,
):
    """
    Tests for the Role API.
    """

    def setUp(
        self,
    ) -> None:
        """
        Set up test data.
        """

        super().setUp()

        self.user = User.objects.create_superuser(
            email="admin@datavion.ai",
            password="Password@123",
        )

        self.client.force_authenticate(
            self.user,
        )

        self.list_url = reverse(
            "rbac-api:roles:role-list",
        )

    def test_should_list_roles(
        self,
    ) -> None:
        """
        GET should return roles.
        """

        create_role(
            name="Doctor",
        )

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_should_create_role(
        self,
    ) -> None:
        """
        POST should create a role.
        """

        payload = {
            "name": "Doctor",
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

    def test_should_retrieve_role(
        self,
    ) -> None:
        """
        GET detail should retrieve a role.
        """

        role = create_role()

        url = reverse(
            "rbac-api:roles:role-detail",
            kwargs={
                "id": role.id,
            },
        )

        response = self.client.get(
            url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_should_update_role(
        self,
    ) -> None:
        """
        PATCH should update a role.
        """

        role = create_role()

        url = reverse(
            "rbac-api:roles:role-detail",
            kwargs={
                "id": role.id,
            },
        )

        response = self.client.patch(
            url,
            {
                "name": "Senior Doctor",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_should_delete_role(
        self,
    ) -> None:
        """
        DELETE should remove a role.
        """

        role = create_role()

        url = reverse(
            "rbac-api:roles:role-detail",
            kwargs={
                "id": role.id,
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
        Unknown role should return 404.
        """

        import uuid

        url = reverse(
            "rbac-api:roles:role-detail",
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
            {
                "name": "",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


__all__ = [
    "RoleAPITestCase",
]
