"""
Base test classes for the Accounts application.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class BaseAccountsAPITestCase(APITestCase):
    """
    Base class for Accounts API tests.
    """

    def create_user(
        self,
        *,
        email: str = "john@example.com",
        password: str = "Password@123",
        **extra_fields,
    ) -> User:
        """
        Create and return a test user.
        """

        return User.objects.create_user(
            email=email,
            password=password,
            **extra_fields,
        )

    def get_refresh_token(
        self,
        *,
        user: User,
    ) -> str:
        """
        Generate a refresh token.
        """

        refresh = RefreshToken.for_user(
            user,
        )

        return str(
            refresh,
        )

    def get_access_token(
        self,
        *,
        user: User,
    ) -> str:
        """
        Generate an access token.
        """

        refresh = RefreshToken.for_user(
            user,
        )

        return str(
            refresh.access_token,
        )

    def authenticate(
        self,
        *,
        user: User,
    ) -> None:
        """
        Authenticate the API client.
        """

        access = self.get_access_token(
            user=user,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )

    def register_payload(
        self,
        **kwargs,
    ) -> dict:
        """
        Build a registration payload.
        """

        payload = {
            "email": "john@example.com",
            "password": "Password@123",
            "first_name": "John",
            "last_name": "Doe",
        }

        payload.update(
            kwargs,
        )

        return payload

    def login_payload(
        self,
        **kwargs,
    ) -> dict:
        """
        Build a login payload.
        """

        payload = {
            "email": "john@example.com",
            "password": "Password@123",
        }

        payload.update(
            kwargs,
        )

        return payload
