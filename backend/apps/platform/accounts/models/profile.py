"""
Profile model for the Accounts application.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel
from apps.platform.accounts.constants import (
    DEFAULT_LANGUAGE,
    DEFAULT_TIMEZONE,
)


class Profile(
    TimeStampedModel,
):
    """
    Extended profile information for a platform user.

    Authentication information belongs to User.

    User preferences and personalization
    belong here.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text=("User associated with this profile."),
    )

    avatar = models.ImageField(
        upload_to="profiles/avatars/",
        blank=True,
        null=True,
        help_text=("Profile avatar image."),
    )

    timezone = models.CharField(
        max_length=100,
        default=DEFAULT_TIMEZONE,
        help_text=("Preferred user timezone."),
    )

    language = models.CharField(
        max_length=20,
        default=DEFAULT_LANGUAGE,
        help_text=("Preferred application language."),
    )

    theme = models.CharField(
        max_length=20,
        default="system",
        help_text=("Preferred UI theme."),
    )

    locale = models.CharField(
        max_length=20,
        default="en",
        help_text=("Preferred locale."),
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(
        self,
    ) -> str:
        return self.user.email


__all__ = ("Profile",)
