"""
Provider model.

Represents healthcare providers
within a tenant organization.

Provider is the clinical profile
linked to an Employee identity.

Lifecycle is managed through
Provider workflows.

Supports:

- Multi-tenant healthcare SaaS
- Employee integration
- Clinical scheduling
- Credential verification
- Provider discovery
"""

from __future__ import annotations

from decimal import Decimal

from django.db import models

from apps.clinical.providers.constants import (
    DEFAULT_PROVIDER_STATUS,
    ProviderStatus,
    ProviderType,
)
from apps.core.models import (
    BaseManager,
    BaseModel,
)
from apps.organization.employees.models import Employee
from apps.platform.organizations.models import Organization


class Provider(
    BaseModel,
):
    """
    Healthcare provider profile.

    Provider belongs to an organization
    and extends an employee identity.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="providers",
        help_text=("Organization that owns the provider."),
    )

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="provider",
        help_text=("Employee profile associated with provider."),
    )

    provider_number = models.CharField(
        max_length=30,
        help_text=("Unique provider identifier."),
    )

    provider_type = models.CharField(
        max_length=30,
        choices=ProviderType.choices,
        help_text=("Healthcare provider classification."),
    )

    years_of_experience = models.PositiveSmallIntegerField(
        default=0,
        help_text=("Professional experience in years."),
    )

    consultation_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Consultation fee in INR; zero disables paid appointment booking.",
    )

    is_accepting_patients = models.BooleanField(
        default=True,
        db_index=True,
        help_text=("Whether provider accepts new patients."),
    )

    bio = models.TextField(
        blank=True,
        help_text=("Professional biography."),
    )

    status = models.CharField(
        max_length=30,
        choices=ProviderStatus.choices,
        default=DEFAULT_PROVIDER_STATUS,
        db_index=True,
        help_text=("Provider workflow lifecycle status."),
    )

    class Meta:
        db_table = "providers"

        verbose_name = "Provider"

        verbose_name_plural = "Providers"

        ordering = ("provider_number",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "provider_type",
                ],
            ),
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "organization",
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
                name=("unique_provider_number_per_organization"),
            ),
        ]

    @property
    def full_name(
        self,
    ) -> str:
        """
        Return provider employee name.
        """

        return self.employee.full_name

    @property
    def display_name(
        self,
    ) -> str:
        """
        Display provider name.
        """

        return self.employee.full_name

    @property
    def is_active_provider(
        self,
    ) -> bool:
        """
        Check provider availability.
        """

        return self.status == ProviderStatus.ACTIVE

    def __str__(
        self,
    ) -> str:
        return f"{self.display_name} ({self.provider_number})"


__all__ = [
    "Provider",
]
