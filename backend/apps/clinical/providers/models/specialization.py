"""
Provider specialization model.

Represents medical specialties
associated with healthcare providers.

Supports:

- Multi-specialty providers
- Primary specialty
- Provider discovery
- Appointment matching
- AI clinical routing
"""

from __future__ import annotations

from django.db import models

from apps.core.models import (
    BaseManager,
    BaseModel,
)


class ProviderSpecialization(
    BaseModel,
):
    """
    Medical specialization assigned
    to a provider.
    """

    objects = BaseManager()

    provider = models.ForeignKey(
        "providers.Provider",
        on_delete=models.CASCADE,
        related_name="specializations",
        help_text=("Provider associated with specialization."),
    )

    name = models.CharField(
        max_length=100,
        help_text=("Specialization name."),
    )

    code = models.CharField(
        max_length=50,
        help_text=("Unique specialization code."),
    )

    description = models.TextField(
        blank=True,
        help_text=("Specialization description."),
    )

    is_primary = models.BooleanField(
        default=False,
        db_index=True,
        help_text=("Primary specialization for provider."),
    )

    class Meta:
        db_table = "provider_specializations"

        verbose_name = "Provider Specialization"

        verbose_name_plural = "Provider Specializations"

        ordering = ("name",)

        indexes = [
            models.Index(
                fields=[
                    "provider",
                ],
            ),
            models.Index(
                fields=[
                    "code",
                ],
            ),
            models.Index(
                fields=[
                    "is_primary",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "provider",
                    "code",
                ],
                name=("unique_provider_specialization"),
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.provider.display_name} - {self.name}"


__all__ = [
    "ProviderSpecialization",
]
