"""
Tests for changing the authenticated user's password.
"""

from __future__ import annotations

from rest_framework import status

from apps.platform.accounts.tests.base import BaseAccountsAPITestCase


class ChangePasswordAPIViewTestCase(
    BaseAccountsAPITestCase,
):
    """
    Test suite for the Change Password API.
    """

    endpoint = "/api/auth/change-password/"

    def setUp(
        self,
    ) -> None:
        """
        Create an authenticated user.
        """

        self.user = self.create_user(
            password="Password@123",
        )

        self.authenticate(
            user=self.user,
        )

    def payload(
        self,
        **kwargs,
    ) -> dict:
        """
        Build a password change payload.
        """

        data = {
            "current_password": "Password@123",
            "new_password": "NewPassword@123",
            "confirm_password": "NewPassword@123",
        }

        data.update(kwargs)

        return data

    def test_change_password_success(
        self,
    ) -> None:
        """
        Password is changed successfully.
        """

        response = self.client.post(
            self.endpoint,
            self.payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

    def test_requires_authentication(
        self,
    ) -> None:
        """
        Authentication is required.
        """

        self.client.credentials()

        response = self.client.post(
            self.endpoint,
            self.payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_wrong_current_password(
        self,
    ) -> None:
        """
        Current password must be correct.
        """

        response = self.client.post(
            self.endpoint,
            self.payload(
                current_password="WrongPassword",
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_password_confirmation_mismatch(
        self,
    ) -> None:
        """
        Password confirmation must match.
        """

        response = self.client.post(
            self.endpoint,
            self.payload(
                confirm_password="DifferentPassword@123",
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_old_password_no_longer_works(
        self,
    ) -> None:
        """
        Old password becomes invalid.
        """

        self.client.post(
            self.endpoint,
            self.payload(),
            format="json",
        )

        response = self.client.post(
            "/api/auth/login/",
            {
                "email": self.user.email,
                "password": "Password@123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_new_password_works(
        self,
    ) -> None:
        """
        New password authenticates successfully.
        """

        self.client.post(
            self.endpoint,
            self.payload(),
            format="json",
        )

        response = self.client.post(
            "/api/auth/login/",
            {
                "email": self.user.email,
                "password": "NewPassword@123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_standard_response_envelope(
        self,
    ) -> None:
        """
        Verify the standardized response schema.
        """

        response = self.client.post(
            self.endpoint,
            self.payload(),
            format="json",
        )

        self.assertSetEqual(
            set(response.data.keys()),
            {
                "success",
                "message",
                "data",
            },
        )
