"""
Provider credential model.

Stores professional qualifications,
certifications and training records
for healthcare providers.

Supports:

- Credential verification workflow
- Compliance tracking
- Document linkage
- Expiry management
"""

from __future__ import annotations

from django.db import models

from apps.clinical.providers.constants import (
    CredentialStatus,
    CredentialType,
)
from apps.core.models import (
    BaseManager,
    BaseModel,
)


class ProviderCredential(
    BaseModel,
):
    """
    Professional credential of a provider.
    """

    objects = BaseManager()

    provider = models.ForeignKey(
        "providers.Provider",
        on_delete=models.CASCADE,
        related_name="credentials",
        help_text=("Provider associated with credential."),
    )

    credential_type = models.CharField(
        max_length=30,
        choices=CredentialType.choices,
        help_text=("Type of professional credential."),
    )

    name = models.CharField(
        max_length=150,
        help_text=("Credential name."),
    )

    issuing_authority = models.CharField(
        max_length=150,
        blank=True,
        help_text=("Organization issuing credential."),
    )

    credential_number = models.CharField(
        max_length=100,
        blank=True,
        help_text=("Credential reference number."),
    )

    issued_date = models.DateField(
        null=True,
        blank=True,
        help_text=("Credential issue date."),
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
        help_text=("Credential expiry date."),
    )

    status = models.CharField(
        max_length=30,
        choices=CredentialStatus.choices,
        default=CredentialStatus.PENDING,
        db_index=True,
        help_text=("Credential verification status."),
    )

    document_id = models.UUIDField(
        null=True,
        blank=True,
        help_text=("Linked document identifier."),
    )

    remarks = models.TextField(
        blank=True,
        help_text=("Verification notes."),
    )

    class Meta:
        db_table = "provider_credentials"

        verbose_name = "Provider Credential"

        verbose_name_plural = "Provider Credentials"

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
                    "credential_type",
                ],
            ),
            models.Index(
                fields=[
                    "expiry_date",
                ],
            ),
        ]

    @property
    def is_verified(
        self,
    ) -> bool:
        """
        Check credential verification state.
        """

        return self.status == CredentialStatus.VERIFIED

    def __str__(
        self,
    ) -> str:
        return f"{self.name} - {self.provider.display_name}"


__all__ = [
    "ProviderCredential",
]
