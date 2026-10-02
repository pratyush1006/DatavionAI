"""
Verification services.

Handles:

- Email verification
- OTP verification workflow
- Verification notifications

Notification delivery is delegated to the DatavionOS
common notification framework.
"""

from __future__ import annotations

from django.db import transaction

from apps.common.exceptions import (
    ValidationException,
)
from apps.common.notifications.constants import (
    CHANNEL_EMAIL,
)
from apps.common.notifications.models import (
    Notification,
    NotificationRecipient,
)
from apps.common.notifications.services import (
    notification_service,
)
from apps.platform.accounts.constants import (
    OTPChannel,
    OTPPurpose,
)
from apps.platform.accounts.models import (
    User,
)
from apps.platform.accounts.selectors.account import (
    get_user_by_email,
)
from apps.platform.accounts.services.otp import (
    OTPService,
)


class VerificationService:
    """
    Business services for account verification.
    """

    @staticmethod
    def _send_email_verification_notification(
        *,
        user: User,
        code: str,
    ) -> None:
        """
        Send email verification OTP notification.
        """

        notification_service.send(
            Notification(
                name="EMAIL_VERIFICATION_OTP",
                channel=CHANNEL_EMAIL,
                recipient=NotificationRecipient(
                    recipient_id=str(user.id),
                    address=user.email,
                    name=(user.get_full_name() or user.email),
                ),
                template="verification_otp",
                payload={
                    "otp": code,
                    "email": user.email,
                },
            ),
        )

    @staticmethod
    @transaction.atomic
    def verify_email(
        *,
        email: str,
        otp: str,
    ) -> User:
        """
        Verify email address using OTP.
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

        transaction.on_commit(
            lambda: notification_service.send(
                Notification(
                    name="WELCOME_EMAIL",
                    channel=CHANNEL_EMAIL,
                    recipient=NotificationRecipient(
                        recipient_id=str(user.id),
                        address=user.email,
                        name=(user.get_full_name() or user.email),
                    ),
                    template="welcome",
                    payload={
                        "name": (user.get_full_name() or user.email),
                    },
                ),
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
        Generate and resend email verification OTP.
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

        result = OTPService.create(
            user=user,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            recipient=user.email,
            channel=OTPChannel.EMAIL,
        )

        transaction.on_commit(
            lambda: VerificationService._send_email_verification_notification(
                user=user,
                code=result.code,
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
