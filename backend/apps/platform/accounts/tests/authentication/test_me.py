"""
Tests for the authenticated user endpoint.
"""

from __future__ import annotations

from rest_framework import status

from apps.platform.accounts.tests.base import BaseAccountsAPITestCase


class MeAPIViewTestCase(
    BaseAccountsAPITestCase,
):
    """
    Test suite for the authenticated user endpoint.
    """

    endpoint = "/api/auth/me/"

    def setUp(
        self,
    ) -> None:
        """
        Create an authenticated user.
        """

        self.user = self.create_user(
            first_name="John",
            last_name="Doe",
        )

        self.authenticate(
            user=self.user,
        )

    def test_me_success(
        self,
    ) -> None:
        """
        Authenticated user can retrieve
        their profile.
        """

        response = self.client.get(
            self.endpoint,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            response.data["data"]["email"],
            self.user.email,
        )

        self.assertEqual(
            response.data["data"]["first_name"],
            self.user.first_name,
        )

        self.assertEqual(
            response.data["data"]["last_name"],
            self.user.last_name,
        )

    def test_me_requires_authentication(
        self,
    ) -> None:
        """
        Authentication is required.
        """

        self.client.credentials()

        response = self.client.get(
            self.endpoint,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_me_returns_correct_user(
        self,
    ) -> None:
        """
        The authenticated user's
        information is returned.
        """

        response = self.client.get(
            self.endpoint,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["data"]["id"],
            str(self.user.id),
        )

    def test_me_does_not_return_password(
        self,
    ) -> None:
        """
        Password must never be exposed.
        """

        response = self.client.get(
            self.endpoint,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertNotIn(
            "password",
            str(response.data),
        )

    def test_me_does_not_return_permissions(
        self,
    ) -> None:
        """
        Permission fields should not
        be exposed.
        """

        response = self.client.get(
            self.endpoint,
        )

        self.assertNotIn(
            "groups",
            str(response.data),
        )

        self.assertNotIn(
            "user_permissions",
            str(response.data),
        )

        self.assertNotIn(
            "is_superuser",
            str(response.data),
        )

    def test_me_returns_expected_fields(
        self,
    ) -> None:
        """
        Verify the standardized response schema.
        """

        response = self.client.get(
            self.endpoint,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertSetEqual(
            set(response.data.keys()),
            {
                "success",
                "message",
                "data",
            },
        )

        self.assertSetEqual(
            set(response.data["data"].keys()),
            {
                "id",
                "email",
                "first_name",
                "last_name",
                "phone",
                "is_verified",
                "organization",
            },
        )
