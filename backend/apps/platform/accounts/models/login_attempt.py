"""
Login attempt tracking model.

Tracks authentication attempts for security,
fraud detection, and audit purposes.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import (
    TimeStampedModel,
    UUIDModel,
)


class LoginAttemptStatus(models.TextChoices):
    """
    Login attempt lifecycle status.
    """

    SUCCESS = (
        "SUCCESS",
        "Success",
    )

    FAILED = (
        "FAILED",
        "Failed",
    )

    BLOCKED = (
        "BLOCKED",
        "Blocked",
    )


class LoginFailureReason(models.TextChoices):
    """
    Authentication failure reasons.
    """

    INVALID_PASSWORD = (
        "INVALID_PASSWORD",
        "Invalid Password",
    )

    USER_NOT_FOUND = (
        "USER_NOT_FOUND",
        "User Not Found",
    )

    USER_INACTIVE = (
        "USER_INACTIVE",
        "User Inactive",
    )

    EMAIL_NOT_VERIFIED = (
        "EMAIL_NOT_VERIFIED",
        "Email Not Verified",
    )

    ACCOUNT_LOCKED = (
        "ACCOUNT_LOCKED",
        "Account Locked",
    )


class LoginAttempt(
    UUIDModel,
    TimeStampedModel,
):
    """
    Authentication attempt audit record.

    Used for:

    - Security monitoring
    - Fraud detection
    - Compliance audit
    - Suspicious login analysis
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="login_attempts",
        null=True,
        blank=True,
    )

    email = models.EmailField(
        db_index=True,
        help_text="Email used during login attempt.",
    )

    status = models.CharField(
        max_length=20,
        choices=LoginAttemptStatus.choices,
        db_index=True,
    )

    failure_reason = models.CharField(
        max_length=50,
        choices=LoginFailureReason.choices,
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    device = models.CharField(
        max_length=255,
        blank=True,
    )

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    class Meta:
        verbose_name = "Login Attempt"
        verbose_name_plural = "Login Attempts"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "email",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "user",
                    "created_at",
                ],
            ),
            models.Index(
                fields=[
                    "ip_address",
                    "created_at",
                ],
            ),
        ]

    @property
    def is_successful(
        self,
    ) -> bool:
        """
        Return whether login succeeded.
        """

        return self.status == LoginAttemptStatus.SUCCESS

    def __str__(
        self,
    ) -> str:
        return f"{self.email} - {self.status}"


__all__ = (
    "LoginAttempt",
    "LoginAttemptStatus",
    "LoginFailureReason",
)
