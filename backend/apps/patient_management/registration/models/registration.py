"""
Patient Registration model.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.patient_management.patients.models import Patient
from apps.patient_management.registration.constants import (
    CancellationReason,
    RegistrationPriority,
    RegistrationSource,
    RegistrationStatus,
    RegistrationType,
    VerificationMethod,
    VisitType,
)
from apps.patient_management.registration.validators import (
    validate_cancellation_reason,
    validate_notes,
    validate_registration_number,
)
from apps.platform.organizations.models import Organization


class PatientRegistration(BaseModel):
    """
    Represents a patient registration within an organization.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="patient_registrations",
        verbose_name=_("Organization"),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="registrations",
        verbose_name=_("Patient"),
    )

    registration_number = models.CharField(
        max_length=50,
        validators=[
            validate_registration_number,
        ],
        verbose_name=_("Registration Number"),
    )

    registration_type = models.CharField(
        max_length=30,
        choices=RegistrationType.choices,
        default=RegistrationType.NEW_PATIENT,
        verbose_name=_("Registration Type"),
    )

    registration_status = models.CharField(
        max_length=40,
        choices=RegistrationStatus.choices,
        default=RegistrationStatus.DRAFT,
        db_index=True,
        verbose_name=_("Registration Status"),
    )

    registration_source = models.CharField(
        max_length=30,
        choices=RegistrationSource.choices,
        default=RegistrationSource.FRONT_DESK,
        verbose_name=_("Registration Source"),
    )

    visit_type = models.CharField(
        max_length=30,
        choices=VisitType.choices,
        default=VisitType.OPD,
        verbose_name=_("Visit Type"),
    )

    priority = models.CharField(
        max_length=20,
        choices=RegistrationPriority.choices,
        default=RegistrationPriority.NORMAL,
        verbose_name=_("Priority"),
    )

    verification_method = models.CharField(
        max_length=30,
        choices=VerificationMethod.choices,
        default=VerificationMethod.NONE,
        verbose_name=_("Verification Method"),
    )

    verified = models.BooleanField(
        default=False,
        verbose_name=_("Verified"),
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Verified At"),
    )

    verified_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_patient_registrations",
        verbose_name=_("Verified By"),
    )

    registration_datetime = models.DateTimeField(
        verbose_name=_("Registration Date & Time"),
    )

    checked_in_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Checked In At"),
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Completed At"),
    )

    cancellation_reason = models.CharField(
        max_length=50,
        choices=CancellationReason.choices,
        blank=True,
        verbose_name=_("Cancellation Reason"),
    )

    cancellation_notes = models.TextField(
        blank=True,
        validators=[
            validate_cancellation_reason,
        ],
        verbose_name=_("Cancellation Notes"),
    )

    notes = models.TextField(
        blank=True,
        validators=[
            validate_notes,
        ],
        verbose_name=_("Notes"),
    )

    class Meta:
        db_table = "patient_registration"

        verbose_name = _("Patient Registration")
        verbose_name_plural = _("Patient Registrations")

        ordering = ("-registration_datetime",)

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "registration_number",
                ),
                name="uq_registration_number_per_organization",
            ),
        ]

        indexes = [
            models.Index(
                fields=(
                    "organization",
                    "registration_status",
                ),
                name="idx_registration_status",
            ),
            models.Index(
                fields=(
                    "organization",
                    "patient",
                ),
                name="idx_registration_patient",
            ),
            models.Index(
                fields=("registration_datetime",),
                name="idx_registration_datetime",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.registration_number} - {self.patient}"

    @property
    def is_completed(
        self,
    ) -> bool:
        return self.registration_status == RegistrationStatus.COMPLETED

    @property
    def is_cancelled(
        self,
    ) -> bool:
        return self.registration_status == RegistrationStatus.CANCELLED

    @property
    def is_checked_in(
        self,
    ) -> bool:
        return self.registration_status == RegistrationStatus.CHECKED_IN

    @property
    def is_verified(
        self,
    ) -> bool:
        return self.verified
