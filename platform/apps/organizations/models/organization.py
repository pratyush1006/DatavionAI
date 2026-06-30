"""
Organization models.
"""

from __future__ import annotations

from django.db import models

from apps.common.models import BaseManager
from apps.common.validators import (
    phone_validator,
    validate_organization_code,
)
from apps.core.models import TimeStampedModel
from apps.organizations.constants import (
    DEFAULT_ORGANIZATION_TYPE,
    OrganizationType,
)


class Organization(TimeStampedModel):
    """
    Represents a healthcare organization within the platform.
    """

    objects = BaseManager()

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Unique organization name.",
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_organization_code],
        help_text="Unique organization code.",
    )

    organization_type = models.CharField(
        max_length=100,
        choices=OrganizationType.choices,
        default=DEFAULT_ORGANIZATION_TYPE,
        db_index=True,
        help_text="Organization category.",
    )

    email = models.EmailField(
        blank=True,
        help_text="Primary contact email.",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_validator],
        help_text="Primary contact phone number.",
    )

    address = models.TextField(
        blank=True,
        help_text="Organization address.",
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        help_text="City where the organization is located.",
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        help_text="State where the organization is located.",
    )

    country = models.CharField(
        max_length=100,
        default="India",
        help_text="Country where the organization is located.",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Designates whether this organization is active.",
    )

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ("name",)

    def __str__(self) -> str:
        """
        Return the human-readable representation of the organization.
        """
        return f"{self.name} ({self.code})"
