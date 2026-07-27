"""
Password management services.

Handles:

- Forgot password workflow
- Password reset using OTP
- Password change
- Security notifications

Notification delivery is delegated to the
DatavionOS common notification framework.
"""

from __future__ import annotations

from django.contrib.auth.hashers import check_password
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
from apps.platform.accounts.selectors import (
    get_user_by_email,
)
from apps.platform.accounts.services.otp import (
    OTPService,
)


class PasswordService:
    """
    Password lifecycle management.

    Responsibilities:

    - Generate password reset OTP
    - Verify OTP
    - Reset password
    - Change password
    - Trigger security notifications

    This service does not handle notification delivery
    implementation directly.
    """

    @staticmethod
    def _send_password_reset_notification(
        *,
        user: User,
        code: str,
    ) -> None:
        """
        Send password reset OTP notification.
        """

        notification_service.send(
            Notification(
                name="PASSWORD_RESET_OTP",
                channel=CHANNEL_EMAIL,
                recipient=NotificationRecipient(
                    recipient_id=str(user.id),
                    address=user.email,
                    name=(user.get_full_name() or user.email),
                ),
                template="password_reset_otp",
                payload={
                    "otp": code,
                    "email": user.email,
                },
            ),
        )

    @staticmethod
    def _send_password_changed_notification(
        *,
        user: User,
    ) -> None:
        """
        Send password changed security notification.
        """

        notification_service.send(
            Notification(
                name="PASSWORD_CHANGED",
                channel=CHANNEL_EMAIL,
                recipient=NotificationRecipient(
                    recipient_id=str(user.id),
                    address=user.email,
                    name=(user.get_full_name() or user.email),
                ),
                template="password_changed",
                payload={
                    "name": (user.get_full_name() or user.email),
                },
            ),
        )

    @staticmethod
    @transaction.atomic
    def forgot_password(
        *,
        email: str,
    ) -> None:
        """
        Generate password reset OTP.

        Security:
        This method intentionally does not expose
        whether an email exists.
        """

        user = get_user_by_email(
            email=email,
        )

        if user is None:
            return

        result = OTPService.create(
            user=user,
            purpose=OTPPurpose.PASSWORD_RESET,
            recipient=user.email,
            channel=OTPChannel.EMAIL,
        )

        transaction.on_commit(
            lambda: PasswordService._send_password_reset_notification(
                user=user,
                code=result.code,
            ),
        )

    @staticmethod
    @transaction.atomic
    def reset_password(
        *,
        email: str,
        otp: str,
        new_password: str,
    ) -> User:
        """
        Reset password using OTP.
        """

        user = get_user_by_email(
            email=email,
        )

        if user is None:
            raise ValidationException(
                message="Invalid password reset request.",
            )

        active_otp = OTPService.get_active_otp(
            user=user,
            purpose=OTPPurpose.PASSWORD_RESET,
        )

        if active_otp is None:
            raise ValidationException(
                message="Password reset code expired.",
            )

        if not OTPService.verify(
            otp=active_otp,
            code=otp,
        ):
            raise ValidationException(
                message="Invalid password reset code.",
            )

        user.set_password(
            new_password,
        )

        user.save(
            update_fields=[
                "password",
                "updated_at",
            ],
        )

        transaction.on_commit(
            lambda: PasswordService._send_password_changed_notification(
                user=user,
            ),
        )

        return user

    @staticmethod
    @transaction.atomic
    def change_password(
        *,
        user: User,
        current_password: str,
        new_password: str,
    ) -> None:
        """
        Change authenticated user's password.
        """

        if not check_password(
            current_password,
            user.password,
        ):
            raise ValidationException(
                message="Current password is incorrect.",
            )

        user.set_password(
            new_password,
        )

        user.save(
            update_fields=[
                "password",
                "updated_at",
            ],
        )

        transaction.on_commit(
            lambda: PasswordService._send_password_changed_notification(
                user=user,
            ),
        )


__all__ = [
    "PasswordService",
]
