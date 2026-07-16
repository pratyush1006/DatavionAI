"""
OTP verification serializers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.accounts.models import User
from apps.platform.accounts.selectors import get_user_by_email
from apps.platform.accounts.services import VerificationService


class VerifyOTPSerializer(serializers.Serializer):
    """
    Serializer for verifying an email verification OTP.
    """

    email = serializers.EmailField()

    otp = serializers.CharField(
        max_length=10,
    )

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize the email.
        """

        return value.strip().lower()

    def save(
        self,
        **kwargs,
    ) -> User:
        """
        Verify the supplied OTP.
        """

        return VerificationService.verify_email(
            email=self.validated_data["email"],
            otp=self.validated_data["otp"],
        )


class ResendOTPSerializer(serializers.Serializer):
    """
    Serializer for resending an email verification OTP.
    """

    email = serializers.EmailField()

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize the email.
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
        **kwargs,
    ) -> None:
        """
        Resend an email verification OTP.
        """

        VerificationService.resend_email_verification(
            email=self.validated_data["email"],
        )


__all__ = [
    "ResendOTPSerializer",
    "VerifyOTPSerializer",
]
