"""
Password authentication serializers.

Handles:

- Forgot password request
- Password reset verification
- Password change

Business logic is delegated to PasswordService.
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth.password_validation import (
    validate_password,
)
from rest_framework import serializers

from apps.platform.accounts.services import (
    PasswordService,
)


class ForgotPasswordSerializer(
    serializers.Serializer,
):
    """
    Serializer for initiating password reset.
    """

    email = serializers.EmailField(
        required=True,
    )

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize email.

        User existence validation is intentionally
        handled inside the service layer to prevent
        account enumeration.
        """

        return value.strip().lower()

    def save(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Generate password reset OTP.
        """

        PasswordService.forgot_password(
            email=self.validated_data["email"],
        )


class ResetPasswordSerializer(
    serializers.Serializer,
):
    """
    Serializer for resetting password using OTP.
    """

    email = serializers.EmailField(
        required=True,
    )

    otp = serializers.CharField(
        required=True,
        write_only=True,
        min_length=6,
        max_length=6,
        trim_whitespace=True,
    )

    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[
            validate_password,
        ],
        style={
            "input_type": "password",
        },
    )

    confirm_password = serializers.CharField(
        required=True,
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
        Normalize email.
        """

        return value.strip().lower()

    def validate_otp(
        self,
        value: str,
    ) -> str:
        """
        Validate OTP format.
        """

        otp = value.strip()

        if not otp.isdigit():
            raise serializers.ValidationError(
                "OTP must contain only digits.",
            )

        return otp

    def validate(
        self,
        attrs: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Validate password confirmation.
        """

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": ("Passwords do not match.")}
            )

        return attrs

    def save(
        self,
        **kwargs: Any,
    ):
        """
        Reset user password.
        """

        return PasswordService.reset_password(
            email=self.validated_data["email"],
            otp=self.validated_data["otp"],
            new_password=self.validated_data["new_password"],
        )


class ChangePasswordSerializer(
    serializers.Serializer,
):
    """
    Serializer for authenticated password change.
    """

    current_password = serializers.CharField(
        required=True,
        write_only=True,
        style={
            "input_type": "password",
        },
    )

    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[
            validate_password,
        ],
        style={
            "input_type": "password",
        },
    )

    confirm_password = serializers.CharField(
        required=True,
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
        Validate new password confirmation.
        """

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": ("Passwords do not match.")}
            )

        return attrs

    def save(
        self,
        *,
        user,
        **kwargs: Any,
    ) -> None:
        """
        Change authenticated user's password.
        """

        PasswordService.change_password(
            user=user,
            current_password=(self.validated_data["current_password"]),
            new_password=(self.validated_data["new_password"]),
        )


__all__ = (
    "ChangePasswordSerializer",
    "ForgotPasswordSerializer",
    "ResetPasswordSerializer",
)
