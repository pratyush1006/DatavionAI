"""
OTP model for the Accounts application.
"""

from __future__ import annotations

from django.conf import settings
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


class OTP(
    UUIDModel,
    TimeStampedModel,
):
    """
    One-Time Password (OTP).

    Used for:

    - Login verification
    - Email verification
    - Password reset
    - MFA
    - Sensitive account actions
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otps",
    )

    recipient = models.CharField(
        max_length=255,
        help_text="Destination where the OTP was delivered.",
    )

    channel = models.CharField(
        max_length=20,
        choices=OTPChannel.choices,
        default=OTPChannel.EMAIL,
        db_index=True,
        help_text="Delivery channel.",
    )

    code = models.CharField(
        max_length=10,
    )

    purpose = models.CharField(
        max_length=30,
        choices=OTPPurpose.choices,
        db_index=True,
    )

    expires_at = models.DateTimeField()

    attempts = models.PositiveSmallIntegerField(
        default=0,
    )

    max_attempts = models.PositiveSmallIntegerField(
        default=OTP_MAX_ATTEMPTS,
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
                ],
            ),
            models.Index(
                fields=[
                    "recipient",
                ],
            ),
            models.Index(
                fields=[
                    "channel",
                ],
            ),
            models.Index(
                fields=[
                    "expires_at",
                ],
            ),
            models.Index(
                fields=[
                    "is_used",
                ],
            ),
        ]

    def is_expired(self) -> bool:
        """
        Return whether the OTP has expired.
        """

        return timezone.now() >= self.expires_at

    def can_attempt(self) -> bool:
        """
        Return whether another verification attempt is allowed.
        """

        return (
            not self.is_used
            and not self.is_expired()
            and self.attempts < self.max_attempts
        )

    def increment_attempts(self) -> None:
        """
        Increment the failed verification attempt counter.
        """

        self.attempts += 1

        self.save(
            update_fields=[
                "attempts",
                "updated_at",
            ],
        )

    def mark_used(self) -> None:
        """
        Mark the OTP as successfully used.
        """

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
        Verify the supplied OTP.
        """

        if not self.can_attempt():
            return False

        if self.code != code:
            self.increment_attempts()
            self.failure_reason = "INVALID_CODE"
            self.save(update_fields=["failure_reason"])
            return False

        self.mark_used()
        return True

    def __str__(self) -> str:
        return f"{self.user.email} [{self.channel}] ({self.purpose})"


__all__ = [
    "OTP",
]
