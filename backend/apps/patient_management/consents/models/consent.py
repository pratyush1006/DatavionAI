"""
Consent model.
"""

from __future__ import annotations

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from apps.core.models import BaseModel
from apps.patient_management.consents.constants import (
    ConsentMethod,
    ConsentSource,
    ConsentStatus,
    ConsentType,
)
from apps.patient_management.consents.managers import (
    ConsentManager,
)
from apps.patient_management.consents.validators import (
    validate_consent_title,
)
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization

__all__ = [
    "Consent",
]


class Consent(BaseModel):
    """
    Versioned patient consent.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="consents",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="consents",
    )

    consent_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
    )

    title = models.CharField(
        max_length=255,
        validators=[
            validate_consent_title,
        ],
    )

    description = models.TextField(
        blank=True,
    )

    consent_type = models.CharField(
        max_length=50,
        choices=ConsentType.choices,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=ConsentStatus.choices,
        default=ConsentStatus.DRAFT,
        db_index=True,
    )

    method = models.CharField(
        max_length=30,
        choices=ConsentMethod.choices,
    )

    source = models.CharField(
        max_length=30,
        choices=ConsentSource.choices,
    )

    version = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
        ],
    )

    effective_date = models.DateField(
        null=True,
        blank=True,
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
    )

    granted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    withdrawn_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    requested_by = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="requested_consents",
    )

    approved_by = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="approved_consents",
    )

    doctor = models.ForeignKey(
        "employees.Employee",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="patient_consents",
    )

    guardian = models.ForeignKey(
        "patient_management.family_members.FamilyMember",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="guardian_consents",
    )

    document = models.ForeignKey(
        "documents.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="patient_consents",
    )

    remarks = models.TextField(
        blank=True,
    )

    is_required = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    objects = ConsentManager()

    class Meta:
        ordering = [
            "-created_at",
        ]

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                    "consent_type",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "patient",
                    "consent_type",
                    "version",
                ],
                name="uq_patient_consent_version",
            ),
            models.UniqueConstraint(
                fields=[
                    "patient",
                    "consent_type",
                ],
                condition=Q(
                    is_active=True,
                ),
                name="uq_active_consent_per_type",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.patient} - {self.get_consent_type_display()} (v{self.version})"
