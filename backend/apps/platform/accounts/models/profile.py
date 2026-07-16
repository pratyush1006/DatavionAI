"""
Profile model for the Accounts application.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import TimeStampedModel
from apps.platform.accounts.constants import (
    DEFAULT_LANGUAGE,
    DEFAULT_TIMEZONE,
)


class Profile(TimeStampedModel):
    """
    Extended profile information for a platform user.

    Authentication information belongs to User.
    User preferences belong here.
    """

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="profile",
    )

    avatar = models.ImageField(
        upload_to="profiles/avatars/",
        blank=True,
        null=True,
    )

    timezone = models.CharField(
        max_length=100,
        default=DEFAULT_TIMEZONE,
    )

    language = models.CharField(
        max_length=20,
        default=DEFAULT_LANGUAGE,
    )

    theme = models.CharField(
        max_length=20,
        default="system",
    )

    locale = models.CharField(
        max_length=20,
        default="en",
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self) -> str:
        return self.user.email


__all__ = [
    "Profile",
]
