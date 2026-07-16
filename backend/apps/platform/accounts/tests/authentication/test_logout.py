"""
Tests for user logout.
"""

from __future__ import annotations

from rest_framework import status

from apps.platform.accounts.tests.base import BaseAccountsAPITestCase


class LogoutAPIViewTestCase(
    BaseAccountsAPITestCase,
):
    """
    Test suite for the Logout API.
    """

    endpoint = "/api/auth/logout/"

    def setUp(
        self,
    ) -> None:
        """
        Create an authenticated user.
        """

        self.user = self.create_user()

        self.refresh = self.get_refresh_token(
            user=self.user,
        )

        self.authenticate(
            user=self.user,
        )

    def test_logout_success(
        self,
    ) -> None:
        """
        Authenticated user can logout.
        """

        response = self.client.post(
            self.endpoint,
            {
                "refresh": self.refresh,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            response.data["message"],
            "Logout successful.",
        )

        self.assertIsNone(
            response.data["data"],
        )

    def test_logout_requires_authentication(
        self,
    ) -> None:
        """
        Authentication is required.
        """

        self.client.credentials()

        response = self.client.post(
            self.endpoint,
            {
                "refresh": self.refresh,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_logout_missing_refresh_token(
        self,
    ) -> None:
        """
        Refresh token is required.
        """

        response = self.client.post(
            self.endpoint,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_logout_invalid_refresh_token(
        self,
    ) -> None:
        """
        Invalid refresh token is rejected.
        """

        response = self.client.post(
            self.endpoint,
            {
                "refresh": "invalid-token",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertFalse(
            response.data["success"],
        )

        self.assertEqual(
            response.data["error"]["code"],
            "authentication_required",
        )

        self.assertEqual(
            response.data["error"]["message"],
            "Invalid refresh token.",
        )

    def test_logout_response_contains_standard_envelope(
        self,
    ) -> None:
        """
        Verify the standardized response schema.
        """

        response = self.client.post(
            self.endpoint,
            {
                "refresh": self.refresh,
            },
            format="json",
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

    def test_logout_blacklists_refresh_token(
        self,
    ) -> None:
        """
        Logout invalidates the refresh token.
        """

        response = self.client.post(
            self.endpoint,
            {
                "refresh": self.refresh,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        #
        # TODO:
        # Verify OutstandingToken and BlacklistedToken
        # entries after implementing blacklist assertions.
        #
