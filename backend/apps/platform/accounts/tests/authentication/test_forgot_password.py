"""
Tests for forgot password.
"""

from __future__ import annotations

from rest_framework import status

from apps.platform.accounts.tests.base import BaseAccountsAPITestCase


class ForgotPasswordAPIViewTestCase(
    BaseAccountsAPITestCase,
):
    """
    Test suite for Forgot Password API.
    """

    endpoint = "/api/auth/forgot-password/"

    def setUp(
        self,
    ) -> None:
        """
        Create a test user.
        """

        self.user = self.create_user()

    def test_forgot_password_success(
        self,
    ) -> None:
        """
        Password reset request succeeds.
        """

        response = self.client.post(
            self.endpoint,
            {
                "email": self.user.email,
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
            "Password reset instructions have been sent.",
        )

        self.assertIsNone(
            response.data["data"],
        )

    def test_unknown_email(
        self,
    ) -> None:
        """
        Unknown email should be rejected.
        """

        response = self.client.post(
            self.endpoint,
            {
                "email": "unknown@example.com",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_email(
        self,
    ) -> None:
        """
        Invalid email format.
        """

        response = self.client.post(
            self.endpoint,
            {
                "email": "invalid-email",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_missing_email(
        self,
    ) -> None:
        """
        Email is required.
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

    def test_standard_response_envelope(
        self,
    ) -> None:
        """
        Verify standardized response schema.
        """

        response = self.client.post(
            self.endpoint,
            {
                "email": self.user.email,
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
