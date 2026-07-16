"""
Verification services.
"""

from __future__ import annotations

from django.db import transaction

from apps.common.exceptions import ValidationException
from apps.platform.accounts.constants import (
    OTPChannel,
    OTPPurpose,
)
from apps.platform.accounts.models import User
from apps.platform.accounts.selectors.account import (
    get_user_by_email,
)
from apps.platform.accounts.services.otp import OTPService
from apps.platform.notifications.services import (
    NotificationService,
)


class VerificationService:
    """
    Business services for account verification.
    """

    @staticmethod
    @transaction.atomic
    def verify_email(
        *,
        email: str,
        otp: str,
    ) -> User:
        """
        Verify a user's email address using an OTP.
        """

        user = get_user_by_email(
            email=email,
        )

        if user is None:
            raise ValidationException(
                message="User not found.",
            )

        if user.is_verified:
            raise ValidationException(
                message="Email is already verified.",
            )

        active_otp = OTPService.get_active_otp(
            user=user,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
        )

        if active_otp is None:
            raise ValidationException(
                message="Verification code not found.",
            )

        if not OTPService.verify(
            otp=active_otp,
            code=otp,
        ):
            raise ValidationException(
                message="Invalid verification code.",
            )

        user.is_verified = True

        user.save(
            update_fields=[
                "is_verified",
                "updated_at",
            ],
        )

        #
        # Send the welcome email only after the
        # verification transaction commits.
        #
        transaction.on_commit(
            lambda: NotificationService.send_welcome_email(
                user=user,
                email=user.email,
                name=user.get_full_name() or user.email,
            ),
        )

        return user

    @staticmethod
    @transaction.atomic
    def resend_email_verification(
        *,
        email: str,
    ) -> None:
        """
        Generate and resend an email verification OTP.
        """

        user = get_user_by_email(
            email=email,
        )

        if user is None:
            raise ValidationException(
                message="User not found.",
            )

        if user.is_verified:
            raise ValidationException(
                message="Email is already verified.",
            )

        otp = OTPService.create(
            user=user,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            recipient=user.email,
            channel=OTPChannel.EMAIL,
        )

        transaction.on_commit(
            lambda: NotificationService.send_verification_otp(
                user=user,
                email=user.email,
                name=user.get_full_name() or user.email,
                otp=otp.code,
            ),
        )

    @staticmethod
    @transaction.atomic
    def verify_phone(
        *,
        user: User,
        otp: str,
    ) -> User:
        """
        Placeholder for future phone verification.
        """

        raise NotImplementedError(
            "Phone verification has not been implemented yet.",
        )


__all__ = [
    "VerificationService",
]
