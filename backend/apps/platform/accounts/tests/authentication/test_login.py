"""
Tests for password authentication and login OTP workflow.
"""

from __future__ import annotations

from unittest.mock import patch

from rest_framework import status

from apps.platform.accounts.models import OTP
from apps.platform.accounts.tests.base import BaseAccountsAPITestCase


class LoginAPIViewTestCase(
    BaseAccountsAPITestCase,
):
    """
    Test suite for the Login API.

    Login is a two-step authentication flow:

    1. Validate email and password.
    2. Issue a login OTP challenge.

    JWT tokens are issued only after successful OTP verification.
    """

    endpoint = "/api/auth/login/"

    verify_endpoint = "/api/auth/login/verify-otp/"

    def setUp(
        self,
    ) -> None:
        """
        Create a verified test user.
        """

        self.user = self.create_user(
            is_verified=True,
            is_active=True,
        )

    def get_login_otp(
        self,
    ) -> OTP:
        """
        Return the active login OTP for the test user.
        """

        return (
            OTP.objects.filter(
                user=self.user,
                purpose="LOGIN",
                is_used=False,
            )
            .order_by("-created_at")
            .first()
        )

    @patch(
        "apps.platform.accounts.services.authentication.AuthenticationService._send_login_otp",
    )
    def test_login_success(
        self,
        send_login_otp,
    ) -> None:
        """
        Correct credentials issue a login OTP challenge.
        """

        with self.captureOnCommitCallbacks(execute=True):
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
            "Login OTP sent successfully.",
        )

        self.assertSetEqual(
            set(response.data["data"].keys()),
            {
                "otp_id",
                "requires_otp",
                "expires_at",
            },
        )

        self.assertTrue(
            response.data["data"]["requires_otp"],
        )

        self.assertIsNotNone(
            response.data["data"]["otp_id"],
        )

        self.assertIsNotNone(
            response.data["data"]["expires_at"],
        )

        otp = self.get_login_otp()

        self.assertIsNotNone(
            otp,
        )

        send_login_otp.assert_called_once()

    def test_login_invalid_password(
        self,
    ) -> None:
        """
        Incorrect password must be rejected.

        No login OTP must be created.
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

        self.assertFalse(
            response.data["success"],
        )

        self.assertEqual(
            response.data["error"]["message"],
            "Invalid email or password.",
        )

        self.assertFalse(
            OTP.objects.filter(
                user=self.user,
                purpose="LOGIN",
            ).exists(),
        )

    def test_login_unknown_email(
        self,
    ) -> None:
        """
        Unknown email must fail without creating an OTP.
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

        self.assertFalse(
            response.data["success"],
        )

        self.assertEqual(
            response.data["error"]["message"],
            "Invalid email or password.",
        )

    def test_login_unverified_user(
        self,
    ) -> None:
        """
        Unverified users cannot request a login OTP.
        """

        self.user.is_verified = False
        self.user.save(
            update_fields=[
                "is_verified",
            ],
        )

        response = self.client.post(
            self.endpoint,
            self.login_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertEqual(
            response.data["error"]["message"],
            "Please verify your email before logging in.",
        )

        self.assertFalse(
            OTP.objects.filter(
                user=self.user,
                purpose="LOGIN",
            ).exists(),
        )

    def test_login_inactive_user(
        self,
    ) -> None:
        """
        Inactive users cannot request a login OTP.
        """

        self.user.is_active = False
        self.user.save(
            update_fields=[
                "is_active",
            ],
        )

        response = self.client.post(
            self.endpoint,
            self.login_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertEqual(
            response.data["error"]["message"],
            "Invalid email or password.",
        )

        self.assertFalse(
            OTP.objects.filter(
                user=self.user,
                purpose="LOGIN",
            ).exists(),
        )

    def test_login_missing_password(
        self,
    ) -> None:
        """
        Password is required.
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

    def test_login_missing_email(
        self,
    ) -> None:
        """
        Email is required.
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
        Invalid email format is rejected by the serializer.
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

    @patch(
        "apps.platform.accounts.services.authentication.AuthenticationService._send_login_otp",
    )
    def test_login_otp_verification_success(
        self,
        send_login_otp,
    ) -> None:
        """
        Correct login OTP issues access and refresh tokens.
        """

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                self.endpoint,
                self.login_payload(),
                format="json",
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        otp = (
            OTP.objects.filter(
                user=self.user,
                purpose="LOGIN",
                is_used=False,
            )
            .order_by("-created_at")
            .first()
        )

        self.assertIsNotNone(
            otp,
        )

        code = send_login_otp.call_args.kwargs["code"]

        verify_response = self.client.post(
            self.verify_endpoint,
            {
                "otp_id": str(otp.id),
                "otp": code,
            },
            format="json",
        )

        self.assertEqual(
            verify_response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            verify_response.data["success"],
        )

        self.assertEqual(
            verify_response.data["message"],
            "Login successful.",
        )

        self.assertSetEqual(
            set(verify_response.data["data"].keys()),
            {
                "access",
                "refresh",
            },
        )

        otp.refresh_from_db()

        self.assertTrue(
            otp.is_used,
        )

    @patch(
        "apps.platform.accounts.services.authentication.AuthenticationService._send_login_otp",
    )
    def test_login_otp_invalid(
        self,
        send_login_otp,
    ) -> None:
        """
        Invalid login OTP must be rejected.
        """

        response = self.client.post(
            self.endpoint,
            self.login_payload(),
            format="json",
        )

        otp = (
            OTP.objects.filter(
                user=self.user,
                purpose="LOGIN",
                is_used=False,
            )
            .order_by("-created_at")
            .first()
        )

        self.assertIsNotNone(
            otp,
        )

        verify_response = self.client.post(
            self.verify_endpoint,
            {
                "otp_id": str(otp.id),
                "otp": "000000",
            },
            format="json",
        )

        self.assertEqual(
            verify_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertEqual(
            verify_response.data["error"]["message"],
            "Invalid login OTP.",
        )

    def test_login_response_does_not_expose_password(
        self,
    ) -> None:
        """
        Password must never appear in the login response.
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
            str(response.data).lower(),
        )

    def test_login_response_contains_only_expected_fields(
        self,
    ) -> None:
        """
        Login OTP response must contain only the expected fields.
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
                "meta",
            },
        )

        self.assertSetEqual(
            set(response.data["data"].keys()),
            {
                "otp_id",
                "requires_otp",
                "expires_at",
            },
        )

    def test_login_otp_verification_requires_otp_id(
        self,
    ) -> None:
        """
        OTP verification requires an OTP ID.
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

    def test_login_otp_verification_requires_otp(
        self,
    ) -> None:
        """
        OTP verification requires an OTP code.
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
