"""
Patient identifier model.
"""

from __future__ import annotations

from typing import ClassVar

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import AuditableModel
from apps.patient_management.identifiers.constants import (
    IdentifierPriority,
    IdentifierSource,
    IdentifierStatus,
    IdentifierType,
    VerificationStatus,
)
from apps.patient_management.identifiers.validators import (
    validate_aadhaar,
    validate_abha,
    validate_driving_license,
    validate_employee_id,
    validate_external_identifier,
    validate_insurance_member_id,
    validate_mrn,
    validate_national_id,
    validate_passport,
)
from apps.patient_management.models import Patient
from apps.platform.organizations.models import Organization

if TYPE_CHECKING:
    User = get_user_model()


class PatientIdentifier(AuditableModel):
    """
    Stores patient identifiers.
    """

    VALIDATORS: ClassVar[dict[str, callable]] = {
        IdentifierType.MRN: validate_mrn,
        IdentifierType.ABHA: validate_abha,
        IdentifierType.AADHAAR: validate_aadhaar,
        IdentifierType.PASSPORT: validate_passport,
        IdentifierType.DRIVING_LICENSE: validate_driving_license,
        IdentifierType.NATIONAL_ID: validate_national_id,
        IdentifierType.INSURANCE_MEMBER_ID: validate_insurance_member_id,
        IdentifierType.EMPLOYEE_ID: validate_employee_id,
        IdentifierType.EXTERNAL_EMR_ID: validate_external_identifier,
        IdentifierType.LEGACY_HOSPITAL_ID: validate_external_identifier,
        IdentifierType.OTHER: validate_external_identifier,
    }

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_identifiers",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="identifiers",
    )

    identifier_type = models.CharField(
        max_length=50,
        choices=IdentifierType.choices,
    )

    identifier_value = models.CharField(
        max_length=150,
    )

    display_value = models.CharField(
        max_length=150,
        blank=True,
    )

    priority = models.CharField(
        max_length=20,
        choices=IdentifierPriority.choices,
        default=IdentifierPriority.SECONDARY,
    )

    status = models.CharField(
        max_length=20,
        choices=IdentifierStatus.choices,
        default=IdentifierStatus.ACTIVE,
    )

    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )

    source = models.CharField(
        max_length=30,
        choices=IdentifierSource.choices,
        default=IdentifierSource.REGISTRATION,
    )

    issuing_authority = models.CharField(
        max_length=255,
        blank=True,
    )

    issuing_country = models.CharField(
        max_length=100,
        blank=True,
    )

    issued_at = models.DateField(
        null=True,
        blank=True,
    )

    expires_at = models.DateField(
        null=True,
        blank=True,
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    verified_by = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="verified_patient_identifiers",
    )

    system_uri = models.URLField(
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = _("Patient Identifier")
        verbose_name_plural = _("Patient Identifiers")
        ordering = (
            "patient",
            "identifier_type",
            "-is_primary",
            "identifier_value",
        )
        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                ],
                name="patient_id_org_patient_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "identifier_type",
                ],
                name="patient_id_org_type_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "identifier_value",
                ],
                name="patient_id_org_value_idx",
            ),
            models.Index(
                fields=[
                    "status",
                ],
                name="patient_id_status_idx",
            ),
            models.Index(
                fields=[
                    "verification_status",
                ],
                name="patient_id_verify_idx",
            ),
            models.Index(
                fields=[
                    "is_primary",
                ],
                name="patient_id_primary_idx",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "identifier_type",
                    "identifier_value",
                ],
                name="uniq_patient_identifier",
            ),
            models.UniqueConstraint(
                fields=[
                    "patient",
                    "identifier_type",
                ],
                condition=Q(
                    is_primary=True,
                ),
                name="uniq_primary_identifier_type",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.patient} - {self.identifier_type} ({self.identifier_value})"

    @property
    def is_verified(self) -> bool:
        return self.verification_status == VerificationStatus.VERIFIED

    @property
    def is_active(self) -> bool:
        return self.status == IdentifierStatus.ACTIVE

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False

        from django.utils import timezone

        return self.expires_at < timezone.localdate()

    def clean(self) -> None:
        super().clean()

        self.identifier_value = self.identifier_value.strip().upper()

        if not self.display_value:
            self.display_value = self.identifier_value

        validator = self.VALIDATORS.get(
            self.identifier_type,
        )

        if validator is not None:
            validator(self.identifier_value)

        if self.issued_at and self.expires_at and self.expires_at < self.issued_at:
            raise ValidationError(
                {
                    "expires_at": _(
                        "Expiry date cannot be before issue date.",
                    ),
                },
            )

        if self.is_primary:
            exists = (
                PatientIdentifier.objects.filter(
                    patient=self.patient,
                    identifier_type=self.identifier_type,
                    is_primary=True,
                )
                .exclude(pk=self.pk)
                .exists()
            )

            if exists:
                raise ValidationError(
                    {
                        "is_primary": _(
                            "Only one primary identifier is allowed "
                            "per identifier type.",
                        ),
                    },
                )

    def save(
        self,
        *args: object,
        **kwargs: object,
    ) -> None:
        self.full_clean()
        super().save(
            *args,
            **kwargs,
        )

    def mark_as_primary(self) -> None:
        PatientIdentifier.objects.filter(
            patient=self.patient,
            identifier_type=self.identifier_type,
            is_primary=True,
        ).exclude(
            pk=self.pk,
        ).update(
            is_primary=False,
        )

        self.is_primary = True
        self.save(
            update_fields=[
                "is_primary",
                "updated_at",
            ],
        )

    def activate(self) -> None:
        self.status = IdentifierStatus.ACTIVE
        self.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

    def deactivate(self) -> None:
        self.status = IdentifierStatus.INACTIVE
        self.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

    def revoke(self) -> None:
        self.status = IdentifierStatus.REVOKED
        self.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

    def verify(
        self,
        user: User,
    ) -> None:
        from django.utils import timezone

        self.verification_status = VerificationStatus.VERIFIED
        self.verified_by = user
        self.verified_at = timezone.now()

        self.save(
            update_fields=[
                "verification_status",
                "verified_by",
                "verified_at",
                "updated_at",
            ],
        )

    def reject(
        self,
    ) -> None:
        self.verification_status = VerificationStatus.REJECTED

        self.save(
            update_fields=[
                "verification_status",
                "updated_at",
            ],
        )


__all__ = [
    "PatientIdentifier",
]
