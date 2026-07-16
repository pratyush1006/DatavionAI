"""
Tests for password management endpoints.
"""

from __future__ import annotations

from rest_framework import status

from apps.platform.accounts.tests.base import BaseAccountsAPITestCase


class PasswordAPIViewTestCase(
    BaseAccountsAPITestCase,
):
    """
    Test suite for password management APIs.
    """

    forgot_endpoint = "/api/auth/forgot-password/"

    reset_endpoint = "/api/auth/reset-password/"

    change_endpoint = "/api/auth/change-password/"

    def setUp(
        self,
    ) -> None:
        """
        Create an authenticated user.
        """

        self.user = self.create_user()

        self.authenticate(
            user=self.user,
        )

    # ------------------------------------------------------------------
    # Forgot Password
    # ------------------------------------------------------------------

    def test_forgot_password_success(
        self,
    ) -> None:
        """
        Password reset email is sent.

        NOTE:
        Implement after email service.
        """

        self.skipTest(
            "Forgot password not implemented.",
        )

    def test_forgot_password_unknown_email(
        self,
    ) -> None:
        """
        Unknown email is handled correctly.
        """

        self.skipTest(
            "Forgot password not implemented.",
        )

    def test_forgot_password_missing_email(
        self,
    ) -> None:
        """
        Email field is required.
        """

        response = self.client.post(
            self.forgot_endpoint,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    # ------------------------------------------------------------------
    # Reset Password
    # ------------------------------------------------------------------

    def test_reset_password_success(
        self,
    ) -> None:
        """
        Password reset succeeds.

        NOTE:
        Implement after reset token model.
        """

        self.skipTest(
            "Reset password not implemented.",
        )

    def test_reset_password_invalid_token(
        self,
    ) -> None:
        """
        Invalid reset token is rejected.
        """

        self.skipTest(
            "Reset password not implemented.",
        )

    def test_reset_password_expired_token(
        self,
    ) -> None:
        """
        Expired reset token is rejected.
        """

        self.skipTest(
            "Reset password not implemented.",
        )

    # ------------------------------------------------------------------
    # Change Password
    # ------------------------------------------------------------------

    def test_change_password_success(
        self,
    ) -> None:
        """
        Authenticated user changes password.

        NOTE:
        Implement after service.
        """

        self.skipTest(
            "Change password not implemented.",
        )

    def test_change_password_wrong_old_password(
        self,
    ) -> None:
        """
        Incorrect current password is rejected.
        """

        self.skipTest(
            "Change password not implemented.",
        )

    def test_change_password_weak_password(
        self,
    ) -> None:
        """
        Weak passwords are rejected.
        """

        self.skipTest(
            "Change password not implemented.",
        )

    def test_change_password_requires_authentication(
        self,
    ) -> None:
        """
        Authentication is required.
        """

        self.client.credentials()

        response = self.client.post(
            self.change_endpoint,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
