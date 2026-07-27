"""
OTP model for the Accounts application.
"""

from __future__ import annotations

from django.conf import settings
from django.contrib.auth.hashers import (
    check_password,
    make_password,
)
from django.db import models
from django.utils import timezone

from apps.core.models import (
    TimeStampedModel,
    UUIDModel,
)
from apps.platform.accounts.constants import (
    OTP_MAX_ATTEMPTS,
    OTPChannel,
    OTPPurpose,
)


class OTPDeliveryStatus(models.TextChoices):
    """
    OTP delivery lifecycle.
    """

    PENDING = (
        "pending",
        "Pending",
    )

    SENT = (
        "sent",
        "Sent",
    )

    FAILED = (
        "failed",
        "Failed",
    )

    DELIVERED = (
        "delivered",
        "Delivered",
    )


class OTP(
    UUIDModel,
    TimeStampedModel,
):
    """
    Secure One-Time Password model.

    Supports:

    - Email verification
    - Login MFA
    - Password reset
    - Sensitive actions
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otps",
    )

    recipient = models.CharField(
        max_length=255,
    )

    channel = models.CharField(
        max_length=20,
        choices=OTPChannel.choices,
        default=OTPChannel.EMAIL,
        db_index=True,
    )

    code_hash = models.CharField(
        max_length=255,
    )

    purpose = models.CharField(
        max_length=30,
        choices=OTPPurpose.choices,
        db_index=True,
    )

    delivery_status = models.CharField(
        max_length=20,
        choices=OTPDeliveryStatus.choices,
        default=OTPDeliveryStatus.PENDING,
        db_index=True,
    )

    expires_at = models.DateTimeField()

    attempts = models.PositiveSmallIntegerField(
        default=0,
    )

    max_attempts = models.PositiveSmallIntegerField(
        default=OTP_MAX_ATTEMPTS,
    )

    resend_count = models.PositiveSmallIntegerField(
        default=0,
    )

    locked_until = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_used = models.BooleanField(
        default=False,
        db_index=True,
    )

    used_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    failure_reason = models.CharField(
        max_length=100,
        blank=True,
    )

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "user",
                    "purpose",
                    "is_used",
                ],
            ),
            models.Index(
                fields=[
                    "expires_at",
                ],
            ),
        ]

    def set_code(
        self,
        code: str,
    ) -> None:
        """
        Securely hash OTP.
        """

        self.code_hash = make_password(
            code,
        )

    def verify_code(
        self,
        code: str,
    ) -> bool:
        """
        Verify supplied OTP.
        """

        return check_password(
            code,
            self.code_hash,
        )

    def is_expired(
        self,
    ) -> bool:
        return timezone.now() >= self.expires_at

    def is_locked(
        self,
    ) -> bool:
        return self.locked_until is not None and timezone.now() < self.locked_until

    def can_attempt(
        self,
    ) -> bool:
        return (
            not self.is_used
            and not self.is_expired()
            and not self.is_locked()
            and self.attempts < self.max_attempts
        )

    def increment_failed_attempt(
        self,
    ) -> None:
        """
        Increase failed attempts.
        """

        self.attempts += 1

        self.failure_reason = "INVALID_CODE"

        self.save(
            update_fields=[
                "attempts",
                "failure_reason",
                "updated_at",
            ],
        )

    def mark_used(
        self,
    ) -> None:

        self.is_used = True
        self.used_at = timezone.now()

        self.save(
            update_fields=[
                "is_used",
                "used_at",
                "updated_at",
            ],
        )

    def verify(
        self,
        code: str,
    ) -> bool:
        """
        Verify OTP.
        """

        if not self.can_attempt():
            return False

        if not self.verify_code(code):
            self.increment_failed_attempt()

            return False

        self.mark_used()

        return True

    def __str__(
        self,
    ) -> str:

        return f"{self.user.email} [{self.channel}] {self.purpose}"


__all__ = (
    "OTP",
    "OTPDeliveryStatus",
)
