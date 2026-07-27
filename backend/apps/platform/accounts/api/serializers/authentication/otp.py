"""
OTP authentication serializers.

Handles:

- OTP verification
- OTP resend validation

Business logic is delegated to services.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rest_framework import serializers

from apps.platform.accounts.services import (
    VerificationService,
)

if TYPE_CHECKING:
    from apps.platform.accounts.models import User


class VerifyOTPSerializer(
    serializers.Serializer,
):
    """
    Serializer for OTP verification.
    """

    email = serializers.EmailField(
        required=True,
    )

    otp = serializers.CharField(
        write_only=True,
        min_length=6,
        max_length=6,
        trim_whitespace=True,
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

    def save(
        self,
        **kwargs: Any,
    ) -> User:
        """
        Verify email OTP.
        """

        return VerificationService.verify_email(
            email=self.validated_data["email"],
            otp=self.validated_data["otp"],
        )


class ResendOTPSerializer(
    serializers.Serializer,
):
    """
    Serializer for resending verification OTP.
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
        performed in service layer to avoid
        account enumeration.
        """

        return value.strip().lower()

    def save(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Resend verification OTP.
        """

        VerificationService.resend_email_verification(
            email=self.validated_data["email"],
        )


__all__ = (
    "ResendOTPSerializer",
    "VerifyOTPSerializer",
)
