"""
Authentication serializers.
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.platform.accounts.models import User
from apps.platform.accounts.selectors import get_user_by_email
from apps.platform.accounts.services import AuthenticationService


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    password = serializers.CharField(
        write_only=True,
        style={
            "input_type": "password",
        },
        validators=[
            validate_password,
        ],
    )

    class Meta:
        model = User

        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
        )

        extra_kwargs = {
            "email": {
                "required": True,
            },
            "first_name": {
                "required": True,
            },
            "last_name": {
                "required": True,
            },
        }

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize and validate the email address.
        """

        email = value.strip().lower()

        if (
            get_user_by_email(
                email=email,
            )
            is not None
        ):
            raise serializers.ValidationError(
                "A user with this email already exists.",
            )

        return email

    def create(
        self,
        validated_data: dict[str, Any],
    ) -> User:
        """
        Register a new user.
        """

        return AuthenticationService.register(
            **validated_data,
        )


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        style={
            "input_type": "password",
        },
    )

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize the email address.
        """

        return value.strip().lower()

    def save(
        self,
        **kwargs: Any,
    ) -> dict[str, str]:
        """
        Authenticate the user and issue JWT tokens.
        """

        return AuthenticationService.login(
            email=self.validated_data["email"],
            password=self.validated_data["password"],
            ip_address=self.context.get(
                "ip_address",
                "",
            ),
            device=self.context.get(
                "device",
                "Unknown Device",
            ),
            location=self.context.get(
                "location",
                "Unknown Location",
            ),
        )


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout.
    """

    refresh = serializers.CharField()

    def save(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Blacklist the supplied refresh token.
        """

        AuthenticationService.logout(
            refresh_token=self.validated_data["refresh"],
        )


class RefreshSerializer(serializers.Serializer):
    """
    Serializer for refreshing JWT access tokens.
    """

    refresh = serializers.CharField()

    def validate(
        self,
        attrs: dict[str, Any],
    ) -> dict[str, str]:
        """
        Generate a new access token.
        """

        return AuthenticationService.refresh(
            refresh_token=attrs["refresh"],
        )


__all__ = [
    "LoginSerializer",
    "LogoutSerializer",
    "RefreshSerializer",
    "RegisterSerializer",
]
