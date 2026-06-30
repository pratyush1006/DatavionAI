"""
Profile model for the Accounts app.
"""

from __future__ import annotations

from django.db import models

from apps.accounts.constants import (
    DEFAULT_LANGUAGE,
    DEFAULT_TIMEZONE,
)
from apps.core.models import TimeStampedModel


class Profile(TimeStampedModel):
    """
    Stores additional profile information for a user.
    """

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="profile",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    avatar_url = models.URLField(
        blank=True,
        help_text="URL of the user's profile image.",
    )

    timezone = models.CharField(
        max_length=100,
        default=DEFAULT_TIMEZONE,
        help_text="User's preferred timezone.",
    )

    language = models.CharField(
        max_length=20,
        default=DEFAULT_LANGUAGE,
        help_text="User's preferred language.",
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self) -> str:
        """
        Return the string representation of the profile.
        """
        return self.user.email
