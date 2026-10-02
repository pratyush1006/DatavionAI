"""
Tests for OAuth authentication endpoints.
"""

from __future__ import annotations

from rest_framework import status

from apps.platform.accounts.tests.base import BaseAccountsAPITestCase


class OAuthAPIViewTestCase(
    BaseAccountsAPITestCase,
):
    """
    Test suite for OAuth APIs.
    """

    google_endpoint = "/api/auth/oauth/google/"

    microsoft_endpoint = "/api/auth/oauth/microsoft/"

    # ------------------------------------------------------------------
    # Google OAuth
    # ------------------------------------------------------------------

    def test_google_login_success(
        self,
    ) -> None:
        """
        Google OAuth login succeeds.

        NOTE:
        Implement after Google OAuth integration.
        """

        self.skipTest(
            "Google OAuth not implemented.",
        )

    def test_google_invalid_token(
        self,
    ) -> None:
        """
        Invalid Google token is rejected.
        """

        self.skipTest(
            "Google OAuth not implemented.",
        )

    def test_google_missing_token(
        self,
    ) -> None:
        """
        Google token is required.
        """

        response = self.client.post(
            self.google_endpoint,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    # ------------------------------------------------------------------
    # Microsoft OAuth
    # ------------------------------------------------------------------

    def test_microsoft_login_success(
        self,
    ) -> None:
        """
        Microsoft OAuth login succeeds.

        NOTE:
        Implement after Microsoft OAuth integration.
        """

        self.skipTest(
            "Microsoft OAuth not implemented.",
        )

    def test_microsoft_invalid_token(
        self,
    ) -> None:
        """
        Invalid Microsoft token is rejected.
        """

        self.skipTest(
            "Microsoft OAuth not implemented.",
        )

    def test_microsoft_missing_token(
        self,
    ) -> None:
        """
        Microsoft token is required.
        """

        response = self.client.post(
            self.microsoft_endpoint,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    # ------------------------------------------------------------------
    # User Creation
    # ------------------------------------------------------------------

    def test_oauth_creates_new_user(
        self,
    ) -> None:
        """
        First OAuth login creates a new user.

        NOTE:
        Implement after OAuth service.
        """

        self.skipTest(
            "OAuth user creation not implemented.",
        )

    def test_oauth_existing_user_login(
        self,
    ) -> None:
        """
        Existing user can login via OAuth.

        NOTE:
        Implement after OAuth service.
        """

        self.skipTest(
            "OAuth login not implemented.",
        )

    def test_oauth_returns_jwt_tokens(
        self,
    ) -> None:
        """
        OAuth login returns JWT tokens.

        NOTE:
        Implement after OAuth service.
        """

        self.skipTest(
            "OAuth login not implemented.",
        )
