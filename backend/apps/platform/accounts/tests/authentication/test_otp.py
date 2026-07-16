"""
Tests for OTP verification endpoints.
"""

from __future__ import annotations

from rest_framework import status

from apps.platform.accounts.tests.base import BaseAccountsAPITestCase


class OTPAPIViewTestCase(
    BaseAccountsAPITestCase,
):
    """
    Test suite for OTP APIs.
    """

    verify_endpoint = "/api/auth/verify-email/"

    resend_endpoint = "/api/auth/resend-verification/"

    def setUp(
        self,
    ) -> None:
        """
        Create a user.
        """

        self.user = self.create_user()

    def test_verify_otp_success(
        self,
    ) -> None:
        """
        Valid OTP verifies the user.

        NOTE:
        Covered by test_verify_email.py.
        """

        self.skipTest(
            "Covered by test_verify_email.py.",
        )

    def test_verify_invalid_otp(
        self,
    ) -> None:
        """
        Invalid OTP is rejected.

        NOTE:
        Covered by test_verify_email.py.
        """

        self.skipTest(
            "Covered by test_verify_email.py.",
        )

    def test_verify_expired_otp(
        self,
    ) -> None:
        """
        Expired OTP is rejected.

        NOTE:
        Will be implemented after OTP expiry support.
        """

        self.skipTest(
            "OTP expiry not implemented.",
        )

    def test_verify_missing_otp(
        self,
    ) -> None:
        """
        OTP field is required.
        """

        response = self.client.post(
            self.verify_endpoint,
            {
                "email": self.user.email,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_resend_otp_success(
        self,
    ) -> None:
        """
        OTP resend succeeds.

        NOTE:
        Covered by resend verification endpoint tests.
        """

        self.skipTest(
            "Covered by resend verification tests.",
        )

    def test_resend_unknown_email(
        self,
    ) -> None:
        """
        Unknown email is rejected.

        NOTE:
        Covered by resend verification endpoint tests.
        """

        self.skipTest(
            "Covered by resend verification tests.",
        )

    def test_resend_rate_limit(
        self,
    ) -> None:
        """
        OTP resend is rate limited.

        NOTE:
        Implement after rate limiting middleware.
        """

        self.skipTest(
            "Rate limiting not implemented.",
        )
