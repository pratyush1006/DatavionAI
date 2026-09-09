"""
Tests for login OTP resend and verification behavior.
"""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import patch

from django.utils import timezone
from rest_framework import status

from apps.platform.accounts.constants import (
    OTP_MAX_RESEND_PER_HOUR,
    OTP_RESEND_INTERVAL_SECONDS,
    OTPChannel,
    OTPPurpose,
)
from apps.platform.accounts.models import OTP
from apps.platform.accounts.services.otp import OTPService
from apps.platform.accounts.tests.base import BaseAccountsAPITestCase


class LoginOTPAPIViewTestCase(
    BaseAccountsAPITestCase,
):
    """
    Test suite for login OTP APIs.
    """

    login_endpoint = "/api/auth/login/"

    resend_endpoint = "/api/auth/login/resend-otp/"

    verify_endpoint = "/api/auth/login/verify-otp/"

    def setUp(
        self,
    ) -> None:
        """
        Create a verified test user and initial login OTP.
        """

        self.user = self.create_user(
            is_verified=True,
            is_active=True,
        )

    def create_login_otp(
        self,
    ) -> tuple[OTP, str]:
        """
        Create an active login OTP and return its plaintext code.
        """

        result = OTPService.create(
            user=self.user,
            purpose=OTPPurpose.LOGIN,
            recipient=self.user.email,
            channel=OTPChannel.EMAIL,
        )

        return result.otp, result.code

    def make_otp_old_enough_for_resend(
        self,
        otp: OTP,
    ) -> OTP:
        """
        Move an OTP outside the resend cooldown.
        """

        otp.created_at = timezone.now() - timedelta(
            seconds=OTP_RESEND_INTERVAL_SECONDS + 1,
        )

        otp.save(
            update_fields=[
                "created_at",
            ],
        )

        return otp

    @patch(
        "apps.platform.accounts.services.authentication.AuthenticationService._send_login_otp",
    )
    def test_resend_login_otp_success(
        self,
        send_login_otp,
    ) -> None:
        """
        Active login OTP can be resent after cooldown.
        """

        otp, _ = self.create_login_otp()

        self.make_otp_old_enough_for_resend(
            otp,
        )

        response = self.client.post(
            self.resend_endpoint,
            {
                "otp_id": str(otp.id),
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
            "Login verification code resent successfully.",
        )

        self.assertSetEqual(
            set(response.data["data"].keys()),
            {
                "otp_id",
                "requires_otp",
                "expires_at",
                "resend_available_at",
            },
        )

        self.assertTrue(
            response.data["data"]["requires_otp"],
        )

        self.assertNotEqual(
            response.data["data"]["otp_id"],
            str(otp.id),
        )

        send_login_otp.assert_called_once()

    @patch(
        "apps.platform.accounts.services.authentication.AuthenticationService._send_login_otp",
    )
    def test_resend_invalidates_previous_otp(
        self,
        send_login_otp,
    ) -> None:
        """
        Resending must invalidate the previous login OTP.
        """

        otp, old_code = self.create_login_otp()

        self.make_otp_old_enough_for_resend(
            otp,
        )

        response = self.client.post(
            self.resend_endpoint,
            {
                "otp_id": str(otp.id),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        new_otp_id = response.data["data"]["otp_id"]

        self.assertNotEqual(
            new_otp_id,
            str(otp.id),
        )

        otp.refresh_from_db()

        self.assertTrue(
            otp.is_used,
        )

        verify_response = self.client.post(
            self.verify_endpoint,
            {
                "otp_id": str(otp.id),
                "otp": old_code,
            },
            format="json",
        )

        self.assertEqual(
            verify_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_resend_before_cooldown_is_rejected(
        self,
    ) -> None:
        """
        Login OTP resend must respect the server-side cooldown.
        """

        otp, _ = self.create_login_otp()

        response = self.client.post(
            self.resend_endpoint,
            {
                "otp_id": str(otp.id),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertIn(
            "Please wait",
            response.data["error"]["message"],
        )

    def test_resend_unknown_otp_id(
        self,
    ) -> None:
        """
        Unknown OTP IDs must not be accepted.
        """

        response = self.client.post(
            self.resend_endpoint,
            {
                "otp_id": "00000000-0000-0000-0000-000000000000",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertEqual(
            response.data["error"]["message"],
            "Invalid or expired login verification request.",
        )

    def test_resend_requires_otp_id(
        self,
    ) -> None:
        """
        OTP ID is required.
        """

        response = self.client.post(
            self.resend_endpoint,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_resend_rejects_invalid_otp_id_format(
        self,
    ) -> None:
        """
        OTP ID must be a valid UUID.
        """

        response = self.client.post(
            self.resend_endpoint,
            {
                "otp_id": "not-a-uuid",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_resend_rejects_non_login_otp(
        self,
    ) -> None:
        """
        Email-verification OTPs cannot be reused for login OTP resend.
        """

        result = OTPService.create(
            user=self.user,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            recipient=self.user.email,
            channel=OTPChannel.EMAIL,
        )

        otp = result.otp

        self.make_otp_old_enough_for_resend(
            otp,
        )

        response = self.client.post(
            self.resend_endpoint,
            {
                "otp_id": str(otp.id),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertEqual(
            response.data["error"]["message"],
            "Invalid or expired login verification request.",
        )

    def test_resend_inactive_user(
        self,
    ) -> None:
        """
        Inactive users cannot resend login OTPs.
        """

        otp, _ = self.create_login_otp()

        self.make_otp_old_enough_for_resend(
            otp,
        )

        self.user.is_active = False
        self.user.save(
            update_fields=[
                "is_active",
            ],
        )

        response = self.client.post(
            self.resend_endpoint,
            {
                "otp_id": str(otp.id),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertEqual(
            response.data["error"]["message"],
            "User account is inactive.",
        )

    def test_resend_hourly_limit(
        self,
    ) -> None:
        """
        Login OTP resend is limited per hour.
        """

        otp = None

        for _ in range(
            OTP_MAX_RESEND_PER_HOUR + 1,
        ):
            otp, _ = self.create_login_otp()

            self.make_otp_old_enough_for_resend(
                otp,
            )

        self.assertIsNotNone(
            otp,
        )

        response = self.client.post(
            self.resend_endpoint,
            {
                "otp_id": str(otp.id),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertEqual(
            response.data["error"]["message"],
            (
                "You have reached the maximum number of "
                "verification code resends. Please try again later."
            ),
        )

    def test_resend_response_does_not_expose_otp_code(
        self,
    ) -> None:
        """
        OTP plaintext must never appear in the API response.
        """

        otp, _ = self.create_login_otp()

        self.make_otp_old_enough_for_resend(
            otp,
        )

        response = self.client.post(
            self.resend_endpoint,
            {
                "otp_id": str(otp.id),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertNotIn(
            "code",
            str(response.data).lower(),
        )

    def test_verify_expired_login_otp(
        self,
    ) -> None:
        """
        Expired login OTPs cannot be verified.
        """

        otp, code = self.create_login_otp()

        otp.expires_at = timezone.now() - timedelta(
            seconds=1,
        )

        otp.save(
            update_fields=[
                "expires_at",
            ],
        )

        response = self.client.post(
            self.verify_endpoint,
            {
                "otp_id": str(otp.id),
                "otp": code,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertEqual(
            response.data["error"]["message"],
            "Invalid login OTP.",
        )

    def test_verify_unknown_login_otp(
        self,
    ) -> None:
        """
        Unknown login OTP IDs cannot be verified.
        """

        response = self.client.post(
            self.verify_endpoint,
            {
                "otp_id": "00000000-0000-0000-0000-000000000000",
                "otp": "123456",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertEqual(
            response.data["error"]["message"],
            "Invalid login verification request.",
        )

    def test_verify_missing_otp(
        self,
    ) -> None:
        """
        OTP code is required for verification.
        """

        response = self.client.post(
            self.verify_endpoint,
            {
                "otp_id": "00000000-0000-0000-0000-000000000000",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_verify_missing_otp_id(
        self,
    ) -> None:
        """
        OTP ID is required for verification.
        """

        response = self.client.post(
            self.verify_endpoint,
            {
                "otp": "123456",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
