"""
Password management serializers.
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.platform.accounts.models import User
from apps.platform.accounts.selectors import get_user_by_email
from apps.platform.accounts.services import PasswordService


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for initiating the password reset workflow.
    """

    email = serializers.EmailField()

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize and validate the email.
        """

        email = value.strip().lower()

        if (
            get_user_by_email(
                email=email,
            )
            is None
        ):
            raise serializers.ValidationError(
                "User not found.",
            )

        return email

    def save(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Initiate password reset.
        """

        PasswordService.forgot_password(
            email=self.validated_data["email"],
        )


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for completing the password reset workflow.
    """

    email = serializers.EmailField()

    otp = serializers.CharField(
        max_length=6,
    )

    password = serializers.CharField(
        write_only=True,
        style={
            "input_type": "password",
        },
        validators=[
            validate_password,
        ],
    )

    confirm_password = serializers.CharField(
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
        Normalize the email.
        """

        return value.strip().lower()

    def validate(
        self,
        attrs: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Validate password confirmation.
        """

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": ("Passwords do not match."),
                },
            )

        return attrs

    def save(
        self,
        **kwargs: Any,
    ) -> User:
        """
        Reset a user's password.
        """

        return PasswordService.reset_password(
            email=self.validated_data["email"],
            otp=self.validated_data["otp"],
            new_password=self.validated_data["password"],
        )


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing the authenticated user's password.
    """

    current_password = serializers.CharField(
        write_only=True,
        style={
            "input_type": "password",
        },
    )

    new_password = serializers.CharField(
        write_only=True,
        style={
            "input_type": "password",
        },
        validators=[
            validate_password,
        ],
    )

    confirm_password = serializers.CharField(
        write_only=True,
        style={
            "input_type": "password",
        },
    )

    def validate(
        self,
        attrs: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Validate password change request.
        """

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": ("Passwords do not match."),
                },
            )

        if attrs["current_password"] == attrs["new_password"]:
            raise serializers.ValidationError(
                {
                    "new_password": (
                        "New password must be different from the current password."
                    ),
                },
            )

        return attrs

    def save(
        self,
        *,
        user: User,
        **kwargs: Any,
    ) -> None:
        """
        Change the authenticated user's password.
        """

        PasswordService.change_password(
            user=user,
            current_password=self.validated_data["current_password"],
            new_password=self.validated_data["new_password"],
        )


__all__ = [
    "ChangePasswordSerializer",
    "ForgotPasswordSerializer",
    "ResetPasswordSerializer",
]
