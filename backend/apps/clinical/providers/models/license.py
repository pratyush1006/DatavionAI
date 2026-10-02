"""
Provider license model.

Stores professional medical licenses
and regulatory registrations.

Supports:

- Healthcare compliance
- License verification workflow
- Expiry monitoring
- Multi-license providers
"""

from __future__ import annotations

from django.db import models

from apps.clinical.providers.constants import (
    LicenseStatus,
)
from apps.core.models import (
    BaseManager,
    BaseModel,
)


class ProviderLicense(
    BaseModel,
):
    """
    Regulatory license associated
    with a healthcare provider.
    """

    objects = BaseManager()

    provider = models.ForeignKey(
        "providers.Provider",
        on_delete=models.CASCADE,
        related_name="licenses",
        help_text=("Provider associated with license."),
    )

    license_number = models.CharField(
        max_length=100,
        help_text=("Professional license number."),
    )

    license_type = models.CharField(
        max_length=100,
        help_text=("Type of medical license."),
    )

    issuing_authority = models.CharField(
        max_length=150,
        help_text=("Regulatory authority issuing license."),
    )

    issuing_region = models.CharField(
        max_length=100,
        blank=True,
        help_text=("State, province or country."),
    )

    issue_date = models.DateField(
        help_text=("License issue date."),
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
        help_text=("License expiry date."),
    )

    status = models.CharField(
        max_length=30,
        choices=LicenseStatus.choices,
        default=LicenseStatus.PENDING,
        db_index=True,
        help_text=("License lifecycle status."),
    )

    verification_notes = models.TextField(
        blank=True,
        help_text=("License verification remarks."),
    )

    document_id = models.UUIDField(
        null=True,
        blank=True,
        help_text=("Linked license document identifier."),
    )

    class Meta:
        db_table = "provider_licenses"

        verbose_name = "Provider License"

        verbose_name_plural = "Provider Licenses"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "provider",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "license_number",
                ],
            ),
            models.Index(
                fields=[
                    "expiry_date",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "provider",
                    "license_number",
                ],
                name=("unique_provider_license"),
            ),
        ]

    @property
    def is_verified(
        self,
    ) -> bool:
        """
        Check whether license is verified.
        """

        return self.status == LicenseStatus.VERIFIED

    def __str__(
        self,
    ) -> str:
        return f"{self.license_number} - {self.provider.display_name}"


__all__ = [
    "ProviderLicense",
]
