"""
User session tracking model.

Tracks active authentication sessions
for security, device management,
and tenant-grade identity control.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import (
    TimeStampedModel,
    UUIDModel,
)


class UserSessionStatus(models.TextChoices):
    """
    User session lifecycle states.
    """

    ACTIVE = (
        "ACTIVE",
        "Active",
    )

    REVOKED = (
        "REVOKED",
        "Revoked",
    )

    EXPIRED = (
        "EXPIRED",
        "Expired",
    )


class UserSession(
    UUIDModel,
    TimeStampedModel,
):
    """
    Authenticated user session.

    Supports:

    - Active device tracking
    - Session revocation
    - Logout from all devices
    - Security analytics
    - Suspicious session detection
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions",
    )

    refresh_token_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text=("JWT refresh token identifier (jti)."),
    )

    status = models.CharField(
        max_length=20,
        choices=UserSessionStatus.choices,
        default=UserSessionStatus.ACTIVE,
        db_index=True,
    )

    device = models.CharField(
        max_length=255,
        blank=True,
        help_text=("Client device information."),
    )

    browser = models.CharField(
        max_length=100,
        blank=True,
    )

    operating_system = models.CharField(
        max_length=100,
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    last_activity_at = models.DateTimeField(
        auto_now=True,
    )

    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "user",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "refresh_token_id",
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
    def is_active_session(
        self,
    ) -> bool:
        """
        Return whether session is active.
        """

        return self.status == UserSessionStatus.ACTIVE

    def revoke(
        self,
    ) -> None:
        """
        Revoke this session.
        """

        from django.utils import timezone

        self.status = UserSessionStatus.REVOKED

        self.revoked_at = timezone.now()

        self.save(
            update_fields=[
                "status",
                "revoked_at",
                "updated_at",
            ],
        )

    def __str__(
        self,
    ) -> str:
        return f"{self.user.email} - {self.status}"


__all__ = (
    "UserSession",
    "UserSessionStatus",
)
