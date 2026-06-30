"""
Custom user model for the Accounts app.
"""

from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    """
    Custom user model for Datavion AI.
    """

    email = models.EmailField(
        unique=True,
    )

    is_verified = models.BooleanField(
        default=False,
        help_text="Indicates whether the user's email address has been verified.",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        """
        Return the string representation of the user.
        """
        return self.email
