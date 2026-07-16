"""
Password management services.
"""

from __future__ import annotations

from django.db import transaction

from apps.common.exceptions import ValidationException
from apps.platform.accounts.constants import OTPPurpose
from apps.platform.accounts.models import User
from apps.platform.accounts.selectors.account import (
    get_user_by_email,
)
from apps.platform.accounts.services.otp import OTPService
from apps.platform.notifications.services import (
    NotificationService,
)


class PasswordService:
    """
    Business services for password management.
    """

    @staticmethod
    @transaction.atomic
    def forgot_password(
        *,
        email: str,
    ) -> None:
        """
        Generate a password reset OTP and send it to the user.
        """

        user = get_user_by_email(
            email=email,
        )

        if user is None:
            raise ValidationException(
                message="User not found.",
            )

        otp = OTPService.create(
            user=user,
            purpose=OTPPurpose.PASSWORD_RESET,
            recipient=user.email,
        )

        transaction.on_commit(
            lambda: NotificationService.send_password_reset_otp(
                user=user,
                email=user.email,
                name=user.get_full_name() or user.email,
                otp=otp.code,
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
        Reset a user's password using a verified OTP.
        """

        user = get_user_by_email(
            email=email,
        )

        if user is None:
            raise ValidationException(
                message="User not found.",
            )

        if not OTPService.verify_for_user(
            user=user,
            purpose=OTPPurpose.PASSWORD_RESET,
            code=otp,
        ):
            raise ValidationException(
                message="Invalid or expired OTP.",
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
            lambda: NotificationService.send_password_changed(
                user=user,
                email=user.email,
                name=user.get_full_name() or user.email,
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
        Change a user's password.
        """

        if not user.check_password(
            current_password,
        ):
            raise ValidationException(
                message="Current password is incorrect.",
            )

        if current_password == new_password:
            raise ValidationException(
                message=("New password must be different from the current password."),
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
            lambda: NotificationService.send_password_changed(
                user=user,
                email=user.email,
                name=user.get_full_name() or user.email,
            ),
        )


__all__ = [
    "PasswordService",
]
