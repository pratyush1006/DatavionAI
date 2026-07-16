"""
Organization model.
"""

from __future__ import annotations

from apps.common.validators import (
    phone_number_validator,
)
from apps.core.models import (
    BaseManager,
    BaseModel,
)
from apps.platform.organizations.constants import (
    DEFAULT_ORGANIZATION_TYPE,
    OrganizationType,
)
from apps.platform.organizations.validators.organization import (
    validate_organization_code,
)
from django.db import models


class Organization(BaseModel):
    """
    Represents an organization within the Datavion AI platform.
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
        validators=[phone_number_validator],
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

    class Meta:
        db_table = "organizations"
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ("name",)
        indexes = [
            models.Index(fields=["organization_type"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        """
        Return the organization name.
        """
        return f"{self.name} ({self.code})"


__all__ = [
    "Organization",
]
