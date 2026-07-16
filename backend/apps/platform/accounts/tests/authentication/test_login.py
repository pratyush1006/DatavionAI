"""
Tests for user login.
"""

from __future__ import annotations

from rest_framework import status

from apps.platform.accounts.tests.base import BaseAccountsAPITestCase


class LoginAPIViewTestCase(
    BaseAccountsAPITestCase,
):
    """
    Test suite for the Login API.
    """

    endpoint = "/api/auth/login/"

    def setUp(
        self,
    ) -> None:
        """
        Create a test user.
        """

        self.user = self.create_user()

    def test_login_success(
        self,
    ) -> None:
        """
        User can login successfully.
        """

        response = self.client.post(
            self.endpoint,
            self.login_payload(),
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
            "Login successful.",
        )

        self.assertIn(
            "access",
            response.data["data"],
        )

        self.assertIn(
            "refresh",
            response.data["data"],
        )

    def test_login_invalid_password(
        self,
    ) -> None:
        """
        Login fails with an incorrect password.
        """

        response = self.client.post(
            self.endpoint,
            self.login_payload(
                password="WrongPassword@123",
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_login_unknown_email(
        self,
    ) -> None:
        """
        Login fails for an unknown email.
        """

        response = self.client.post(
            self.endpoint,
            self.login_payload(
                email="unknown@example.com",
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_login_missing_password(
        self,
    ) -> None:
        """
        Login fails when password is missing.
        """

        response = self.client.post(
            self.endpoint,
            {
                "email": "john@example.com",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_missing_email(
        self,
    ) -> None:
        """
        Login fails when email is missing.
        """

        response = self.client.post(
            self.endpoint,
            {
                "password": "Password@123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_invalid_email_format(
        self,
    ) -> None:
        """
        Login fails with an invalid email address.
        """

        response = self.client.post(
            self.endpoint,
            self.login_payload(
                email="invalid-email",
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_response_does_not_expose_password(
        self,
    ) -> None:
        """
        Password must never be exposed.
        """

        response = self.client.post(
            self.endpoint,
            self.login_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertNotIn(
            "password",
            str(response.data),
        )

    def test_login_returns_only_expected_fields(
        self,
    ) -> None:
        """
        Login response should contain only the standard response envelope.
        """

        response = self.client.post(
            self.endpoint,
            self.login_payload(),
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
