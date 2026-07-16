"""
Custom user model for the Accounts application.
"""

from __future__ import annotations

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.validators import phone_number_validator
from apps.core.models import TimeStampedModel
from apps.platform.accounts.models.managers import UserManager


class User(AbstractUser, TimeStampedModel):
    """
    Platform user.

    A User represents an authenticated identity in Datavion AI.

    NOTE:
    The direct organization relationship is temporary and will be replaced
    by OrganizationMembership during the Platform Identity refactor.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
        help_text=(
            "Temporary default organization. "
            "Will be replaced by OrganizationMembership."
        ),
    )

    email = models.EmailField(
        unique=True,
        db_index=True,
        help_text="Primary email used for authentication.",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_number_validator],
        help_text="Phone number in E.164 format.",
    )

    employee_id = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
    )

    is_verified = models.BooleanField(
        default=False,
        db_index=True,
    )

    is_internal_user = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether the user belongs to the internal workforce.",
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("email",)
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["organization"]),
            models.Index(fields=["is_verified"]),
            models.Index(fields=["is_internal_user"]),
        ]

    def save(self, *args, **kwargs) -> None:
        """
        Keep username synchronized with email.
        """

        self.username = self.email
        super().save(*args, **kwargs)

    @property
    def full_name(self) -> str:
        """Return the user's full name."""

        return self.get_full_name()

    def __str__(self) -> str:
        return self.email


__all__ = [
    "User",
]
