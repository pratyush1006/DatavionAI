"""
OTP service for the Accounts application.
"""

from __future__ import annotations

from datetime import timedelta
from secrets import randbelow

from django.db import transaction
from django.utils import timezone

from apps.platform.accounts.constants import (
    OTP_EXPIRY_MINUTES,
    OTPChannel,
    OTPPurpose,
)
from apps.platform.accounts.models import (
    OTP,
    User,
)


class OTPService:
    """
    Service responsible for OTP lifecycle management.

    Responsibilities:

    - Generate OTPs
    - Verify OTPs
    - Retrieve active OTPs
    - Resend OTPs
    - Expire OTPs
    """

    @staticmethod
    def generate_code() -> str:
        """
        Generate a secure six-digit OTP.
        """

        return f"{randbelow(1_000_000):06d}"

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        user: User,
        purpose: OTPPurpose,
        recipient: str,
        channel: OTPChannel = OTPChannel.EMAIL,
        ip_address: str | None = None,
        user_agent: str = "",
    ) -> OTP:
        """
        Create a new OTP.

        Any previous active OTP for the same
        user and purpose is automatically expired.
        """

        OTP.objects.filter(
            user=user,
            purpose=purpose,
            is_used=False,
        ).update(
            is_used=True,
            used_at=timezone.now(),
        )

        return OTP.objects.create(
            user=user,
            recipient=recipient,
            channel=channel,
            purpose=purpose,
            code=cls.generate_code(),
            expires_at=timezone.now()
            + timedelta(
                minutes=OTP_EXPIRY_MINUTES,
            ),
            created_ip=ip_address,
            user_agent=user_agent,
        )

    @staticmethod
    def get_active_otp(
        *,
        user: User,
        purpose: OTPPurpose,
    ) -> OTP | None:
        """
        Return the latest active OTP.
        """

        return (
            OTP.objects.filter(
                user=user,
                purpose=purpose,
                is_used=False,
            )
            .order_by(
                "-created_at",
            )
            .first()
        )

    @staticmethod
    @transaction.atomic
    def verify(
        *,
        otp: OTP,
        code: str,
    ) -> bool:
        """
        Verify an OTP instance.
        """

        if not otp.can_attempt():
            return False

        if otp.code != code:
            otp.increment_attempts()

            otp.save(
                update_fields=[
                    "attempts",
                    "updated_at",
                ],
            )

            return False

        otp.mark_used()

        return True

    @classmethod
    @transaction.atomic
    def verify_for_user(
        cls,
        *,
        user: User,
        purpose: OTPPurpose,
        code: str,
    ) -> bool:
        """
        Verify an OTP using user, purpose and code.

        This is the preferred API for business services.
        """

        otp = cls.get_active_otp(
            user=user,
            purpose=purpose,
        )

        if otp is None:
            return False

        return cls.verify(
            otp=otp,
            code=code,
        )

    @staticmethod
    @transaction.atomic
    def expire(
        *,
        otp: OTP,
    ) -> None:
        """
        Expire an OTP immediately.
        """

        if otp.is_used:
            return

        otp.is_used = True
        otp.used_at = timezone.now()

        otp.save(
            update_fields=[
                "is_used",
                "used_at",
                "updated_at",
            ],
        )

    @classmethod
    @transaction.atomic
    def resend(
        cls,
        *,
        otp: OTP,
    ) -> OTP:
        """
        Generate a replacement OTP.
        """

        cls.expire(
            otp=otp,
        )

        return cls.create(
            user=otp.user,
            purpose=otp.purpose,
            recipient=otp.recipient,
            channel=otp.channel,
            ip_address=otp.created_ip,
            user_agent=otp.user_agent,
        )


__all__ = [
    "OTPService",
]
