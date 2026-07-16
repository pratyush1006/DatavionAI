"""
Tests for JWT token refresh.
"""

from __future__ import annotations

from rest_framework import status

from apps.platform.accounts.tests.base import BaseAccountsAPITestCase


class RefreshAPIViewTestCase(
    BaseAccountsAPITestCase,
):
    """
    Test suite for the Refresh API.
    """

    endpoint = "/api/auth/refresh/"

    def setUp(
        self,
    ) -> None:
        """
        Create a test user.
        """

        self.user = self.create_user()

        self.refresh = self.get_refresh_token(
            user=self.user,
        )

    def test_refresh_success(
        self,
    ) -> None:
        """
        A valid refresh token returns
        a new access token.
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
            "Token refreshed successfully.",
        )

        self.assertIn(
            "access",
            response.data["data"],
        )

        self.assertIn(
            "refresh",
            response.data["data"],
        )

    def test_refresh_returns_new_refresh_token(
        self,
    ) -> None:
        """
        Refresh token rotation returns
        a new refresh token.
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

        self.assertIn(
            "refresh",
            response.data["data"],
        )

        self.assertNotEqual(
            response.data["data"]["refresh"],
            self.refresh,
        )

    def test_refresh_missing_token(
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

    def test_refresh_invalid_token(
        self,
    ) -> None:
        """
        Invalid refresh tokens are rejected.
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

    def test_refresh_response_contains_standard_envelope(
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

        self.assertSetEqual(
            set(response.data["data"].keys()),
            {
                "access",
                "refresh",
            },
        )

    def test_refresh_expired_token(
        self,
    ) -> None:
        """
        Expired refresh tokens should
        be rejected.

        NOTE:
        Implement after adding an
        expired token fixture.
        """

        self.skipTest(
            "Expired token test will be implemented later.",
        )

    def test_refresh_token_cannot_be_reused(
        self,
    ) -> None:
        """
        A refresh token may only be used once.
        """

        #
        # First refresh succeeds.
        #
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
        # Reusing the same refresh token
        # must fail.
        #
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
