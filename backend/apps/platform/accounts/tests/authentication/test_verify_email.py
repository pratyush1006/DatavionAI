"""
Tests for email verification.
"""

from __future__ import annotations

from rest_framework import status

from apps.platform.accounts.constants import OTPPurpose
from apps.platform.accounts.services.otp import OTPService
from apps.platform.accounts.tests.base import BaseAccountsAPITestCase


class VerifyEmailAPIViewTestCase(
    BaseAccountsAPITestCase,
):
    """
    Test suite for Verify Email API.
    """

    endpoint = "/api/auth/verify-email/"

    def setUp(
        self,
    ) -> None:
        """
        Create an unverified user.
        """

        self.user = self.create_user(
            is_verified=False,
        )

        self.otp = OTPService.create(
            user=self.user,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            recipient=self.user.email,
        )

    def test_verify_email_success(
        self,
    ) -> None:
        """
        Email verification succeeds.
        """

        response = self.client.post(
            self.endpoint,
            {
                "email": self.user.email,
                "otp": self.otp.code,
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
            "Email verified successfully.",
        )

        self.assertIsNone(
            response.data["data"],
        )

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.is_verified,
        )

    def test_invalid_otp(
        self,
    ) -> None:
        """
        Invalid OTP.
        """

        response = self.client.post(
            self.endpoint,
            {
                "email": self.user.email,
                "otp": "000000",
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
        Email required.
        """

        response = self.client.post(
            self.endpoint,
            {
                "otp": self.otp.code,
            },
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
        OTP required.
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
                "otp": self.otp.code,
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

    def test_already_verified_user(
        self,
    ) -> None:
        """
        Already verified users cannot verify again.
        """

        self.user.is_verified = True

        self.user.save(
            update_fields=[
                "is_verified",
            ],
        )

        response = self.client.post(
            self.endpoint,
            {
                "email": self.user.email,
                "otp": self.otp.code,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
