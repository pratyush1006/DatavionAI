"""
Tests for the RoleHierarchy API.
"""

from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)

from apps.platform.rbac.tests.factories import (
    RoleFactory,
    RoleHierarchyFactory,
)
from apps.platform.rbac.tests.factories.user_role import (
    UserFactory,
)


class RoleHierarchyAPITestCase(
    APITestCase,
):
    """
    Tests for the RoleHierarchy API.
    """

    def setUp(
        self,
    ) -> None:
        """
        Set up the test case.
        """

        self.user = UserFactory()

        self.client.force_authenticate(
            self.user,
        )

        self.list_url = reverse(
            "rbac-api:role-hierarchy-api:list-create",
        )

    def test_should_list_role_hierarchies(
        self,
    ) -> None:
        """
        Should list role hierarchies.
        """

        RoleHierarchyFactory()
        RoleHierarchyFactory()

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_should_retrieve_role_hierarchy(
        self,
    ) -> None:
        """
        Should retrieve a role hierarchy.
        """

        hierarchy = RoleHierarchyFactory()

        url = reverse(
            "rbac-api:role-hierarchy-api:detail",
            kwargs={
                "pk": hierarchy.pk,
            },
        )

        response = self.client.get(
            url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_should_create_role_hierarchy(
        self,
    ) -> None:
        """
        Should create a role hierarchy.
        """

        payload = {
            "parent_role": RoleFactory().pk,
            "child_role": RoleFactory().pk,
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

    def test_should_update_role_hierarchy(
        self,
    ) -> None:
        """
        Should update a role hierarchy.
        """

        hierarchy = RoleHierarchyFactory()

        url = reverse(
            "rbac-api:role-hierarchy-api:detail",
            kwargs={
                "pk": hierarchy.pk,
            },
        )

        response = self.client.patch(
            url,
            {
                "is_active": False,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_should_delete_role_hierarchy(
        self,
    ) -> None:
        """
        Should delete a role hierarchy.
        """

        hierarchy = RoleHierarchyFactory()

        url = reverse(
            "rbac-api:role-hierarchy-api:detail",
            kwargs={
                "pk": hierarchy.pk,
            },
        )

        response = self.client.delete(
            url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
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

    def test_should_return_not_found(
        self,
    ) -> None:
        """
        Unknown hierarchy should return 404.
        """

        url = reverse(
            "rbac-api:role-hierarchy-api:detail",
            kwargs={
                "pk": 999999,
            },
        )

        response = self.client.get(
            url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_authentication_required(
        self,
    ) -> None:
        """
        Authentication should be required.
        """
        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


__all__ = [
    "RoleHierarchyAPITestCase",
]
