"""
OTP service for the Accounts application.

Responsible only for OTP lifecycle management.

Responsibilities:

- Generate OTPs
- Securely store OTP hashes
- Verify OTPs
- Expire OTPs
- Prevent OTP reuse

Notification delivery is handled by the notification framework.
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

from .results import (
    OTPCreateResult,
)


class OTPService:
    """
    OTP lifecycle service.

    This service has no dependency on email,
    SMS, push, or notification providers.
    """

    @staticmethod
    def generate_code() -> str:
        """
        Generate a secure six digit OTP.
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
    ) -> OTPCreateResult:
        """
        Create a new OTP.

        Database stores only the hash.
        Plain OTP is returned only for delivery.
        """

        OTP.objects.filter(
            user=user,
            purpose=purpose,
            is_used=False,
        ).update(
            is_used=True,
            used_at=timezone.now(),
            updated_at=timezone.now(),
        )

        code = cls.generate_code()

        otp = OTP(
            user=user,
            recipient=recipient,
            channel=channel,
            purpose=purpose,
            expires_at=(
                timezone.now()
                + timedelta(
                    minutes=OTP_EXPIRY_MINUTES,
                )
            ),
            created_ip=ip_address,
            user_agent=user_agent,
        )

        otp.set_code(
            code,
        )

        otp.save()

        return OTPCreateResult(
            otp=otp,
            code=code,
        )

    @staticmethod
    def get_active_otp(
        *,
        user: User,
        purpose: OTPPurpose,
    ) -> OTP | None:
        """
        Return latest active OTP.
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
        Verify OTP.
        """

        return otp.verify(
            code,
        )

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
        Verify OTP for a user.
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
        Expire OTP.
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
    ) -> OTPCreateResult:
        """
        Create replacement OTP.
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
