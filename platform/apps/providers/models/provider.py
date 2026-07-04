"""
Provider model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.employees.models import Employee
from apps.organizations.models import Organization
from apps.providers.constants import (
    DEFAULT_PROVIDER_STATUS,
    ProviderStatus,
    ProviderType,
)


class Provider(BaseModel):
    """
    Represents a healthcare provider within an organization.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="providers",
        help_text="Organization that owns the provider.",
    )

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="provider",
        help_text="Employee profile associated with this provider.",
    )

    provider_number = models.CharField(
        max_length=30,
        help_text="Unique provider identifier.",
    )

    license_number = models.CharField(
        max_length=100,
        help_text="Professional license number.",
    )

    provider_type = models.CharField(
        max_length=30,
        choices=ProviderType.choices,
        help_text="Healthcare provider type.",
    )

    years_of_experience = models.PositiveSmallIntegerField(
        default=0,
        help_text="Years of professional experience.",
    )

    is_accepting_patients = models.BooleanField(
        default=True,
        help_text="Whether the provider is accepting new patients.",
    )

    bio = models.TextField(
        blank=True,
        help_text="Professional biography.",
    )

    status = models.CharField(
        max_length=20,
        choices=ProviderStatus.choices,
        default=DEFAULT_PROVIDER_STATUS,
        db_index=True,
        help_text="Provider lifecycle status.",
    )

    class Meta:
        db_table = "providers"

        verbose_name = "Provider"

        verbose_name_plural = "Providers"

        ordering = ("provider_number",)

        indexes = [
            models.Index(
                fields=[
                    "provider_number",
                ],
            ),
            models.Index(
                fields=[
                    "provider_type",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "is_accepting_patients",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "provider_number",
                ],
                name="unique_provider_number_per_organization",
            ),
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "license_number",
                ],
                name="unique_provider_license_per_organization",
            ),
        ]

    @property
    def full_name(
        self,
    ) -> str:
        """
        Return the provider's full name.
        """

        return self.employee.full_name

    def __str__(
        self,
    ) -> str:
        """
        Return the provider display name.
        """

        return f"{self.employee.full_name} ({self.provider_number})"


__all__ = [
    "Provider",
]
