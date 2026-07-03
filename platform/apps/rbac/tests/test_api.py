"""
Tests for RBAC API.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status

from apps.common.tests.base import BaseAPITestCase
from apps.rbac.tests.factories import RoleFactory


class RoleAPITestCase(BaseAPITestCase):
    """
    API tests for Role endpoints.
    """

    def test_list_roles(self) -> None:
        """
        Roles can be listed.
        """

        RoleFactory(name="Administrator")
        RoleFactory(name="Manager")

        response = self.client.get(
            reverse(
                "role-list-create",
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
            len(response.data["data"]),
            2,
        )

    def test_retrieve_role(self) -> None:
        """
        A role can be retrieved.
        """

        role = RoleFactory(
            name="Administrator",
        )

        response = self.client.get(
            reverse(
                "role-detail",
                kwargs={
                    "role_id": role.id,
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
            role.id,
        )

    def test_create_role(self) -> None:
        """
        A role can be created.
        """

        payload = {
            "name": "Manager",
            "code": "MANAGER",
            "description": "Management role",
            "is_active": True,
        }

        response = self.client.post(
            reverse(
                "role-list-create",
            ),
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            response.data["data"]["name"],
            "Manager",
        )

    def test_update_role(self) -> None:
        """
        A role can be updated.
        """

        role = RoleFactory()

        payload = {
            "name": "Updated Role",
            "code": "UPDATED",
            "description": "Updated description",
            "is_active": False,
        }

        response = self.client.patch(
            reverse(
                "role-detail",
                kwargs={
                    "role_id": role.id,
                },
            ),
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        role.refresh_from_db()

        self.assertEqual(
            role.name,
            "Updated Role",
        )

        self.assertFalse(
            role.is_active,
        )

    def test_delete_role(self) -> None:
        """
        A role can be deleted.
        """

        role = RoleFactory()

        response = self.client.delete(
            reverse(
                "role-detail",
                kwargs={
                    "role_id": role.id,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            role.__class__.objects.filter(
                pk=role.pk,
            ).exists(),
        )

    def test_role_not_found(self) -> None:
        """
        Unknown roles should return 404.
        """

        response = self.client.get(
            reverse(
                "role-detail",
                kwargs={
                    "role_id": 999999,
                },
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertFalse(
            response.data["success"],
        )

    def test_role_requires_authentication(self) -> None:
        """
        Authentication is required.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            reverse(
                "role-list-create",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertFalse(
            response.data["success"],
        )
