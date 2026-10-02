"""
Tests for password reset.
"""

from __future__ import annotations

from rest_framework import status

from apps.platform.accounts.constants import OTPPurpose
from apps.platform.accounts.services.otp import OTPService
from apps.platform.accounts.tests.base import BaseAccountsAPITestCase


class ResetPasswordAPIViewTestCase(
    BaseAccountsAPITestCase,
):
    """
    Test suite for Reset Password API.
    """

    endpoint = "/api/auth/reset-password/"

    def setUp(
        self,
    ) -> None:
        """
        Create a test user and password reset OTP.
        """

        self.user = self.create_user(
            password="Password@123",
            is_verified=True,
        )

        self.otp = OTPService.create(
            user=self.user,
            purpose=OTPPurpose.PASSWORD_RESET,
            recipient=self.user.email,
        )

    def payload(
        self,
        **kwargs,
    ) -> dict:
        """
        Build a reset password payload.
        """

        data = {
            "email": self.user.email,
            "otp": self.otp.code,
            "password": "NewPassword@123",
            "confirm_password": "NewPassword@123",
        }

        data.update(
            kwargs,
        )

        return data

    def test_reset_password_success(
        self,
    ) -> None:
        """
        Password is reset successfully.
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

        self.assertEqual(
            response.data["message"],
            "Password reset successfully.",
        )

        self.assertIsNone(
            response.data["data"],
        )

    def test_invalid_otp(
        self,
    ) -> None:
        """
        Invalid OTP is rejected.
        """

        response = self.client.post(
            self.endpoint,
            self.payload(
                otp="000000",
            ),
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

        payload = self.payload()

        payload.pop(
            "email",
        )

        response = self.client.post(
            self.endpoint,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_missing_otp(
        self,
    ) -> None:
        """
        OTP is required.
        """

        payload = self.payload()

        payload.pop(
            "otp",
        )

        response = self.client.post(
            self.endpoint,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_missing_password(
        self,
    ) -> None:
        """
        Password is required.
        """

        payload = self.payload()

        payload.pop(
            "password",
        )

        response = self.client.post(
            self.endpoint,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_password_confirmation_required(
        self,
    ) -> None:
        """
        Confirmation password is required.
        """

        payload = self.payload()

        payload.pop(
            "confirm_password",
        )

        response = self.client.post(
            self.endpoint,
            payload,
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
                confirm_password="Different@123",
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

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertSetEqual(
            set(
                response.data.keys(),
            ),
            {
                "success",
                "message",
                "data",
            },
        )
