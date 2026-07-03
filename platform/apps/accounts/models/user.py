"""
Custom user model for the Accounts application.
"""

from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.accounts.models.managers import UserManager
from apps.core.models import TimeStampedModel


class User(
    AbstractUser,
    TimeStampedModel,
):
    """
    Custom user model for Datavion AI.
    """

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    email = models.EmailField(
        unique=True,
        help_text="Unique email address used for authentication.",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    employee_id = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
    )

    is_verified = models.BooleanField(
        default=False,
        help_text="Indicates whether the user's email has been verified.",
    )

    is_active_employee = models.BooleanField(
        default=True,
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("email",)

    def save(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Keep username synchronized with email.
        """

        self.username = self.email

        super().save(
            *args,
            **kwargs,
        )

    @property
    def full_name(self) -> str:
        """
        Return the user's full name.
        """

        return self.get_full_name()

    def __str__(
        self,
    ) -> str:
        """
        Return the user email.
        """

        return self.email


__all__ = [
    "User",
]
