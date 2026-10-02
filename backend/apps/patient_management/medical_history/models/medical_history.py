"""Patient medical history aggregate."""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AllObjectsManager, BaseModel, DeletedObjectsManager
from apps.patient_management.constants import RelationshipType
from apps.patient_management.medical_history.constants import (
    AlcoholUse,
    ClinicalStatus,
    MedicalHistoryType,
)
from apps.patient_management.medical_history.managers import MedicalHistoryManager
from apps.patient_management.medical_history.validators import (
    validate_alcohol_use,
    validate_clinical_status,
    validate_history_type,
    validate_title,
)
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


class PatientMedicalHistory(BaseModel):
    """PatientMedicalHistory implementation."""

    objects = MedicalHistoryManager()
    all_objects = AllObjectsManager()
    deleted_objects = DeletedObjectsManager()

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="patient_medical_histories"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="medical_history_entries"
    )
    history_type = models.CharField(
        max_length=30,
        choices=MedicalHistoryType.choices,
        default=MedicalHistoryType.CONDITION,
        validators=[validate_history_type],
        db_index=True,
    )
    title = models.CharField(max_length=255, validators=[validate_title])
    description = models.TextField(blank=True)
    clinical_status = models.CharField(
        max_length=20,
        choices=ClinicalStatus.choices,
        default=ClinicalStatus.ACTIVE,
        validators=[validate_clinical_status],
        db_index=True,
    )
    onset_date = models.DateField(null=True, blank=True)
    resolved_date = models.DateField(null=True, blank=True)
    relationship = models.CharField(
        max_length=30, choices=RelationshipType.choices, blank=True
    )
    is_smoker = models.BooleanField(null=True, blank=True)
    alcohol_use = models.CharField(
        max_length=20,
        choices=AlcoholUse.choices,
        blank=True,
        validators=[validate_alcohol_use],
    )
    recorded_by = models.CharField(max_length=150, blank=True)
    is_verified = models.BooleanField(default=False, db_index=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="verified_medical_history_entries",
    )

    class Meta:
        """Meta implementation."""

        db_table = "patient_medical_histories"
        verbose_name = _("Patient Medical History")
        verbose_name_plural = _("Patient Medical Histories")
        ordering = ("-onset_date", "-created_at")
        indexes = [
            models.Index(
                fields=("organization", "patient", "history_type"),
                name="medhist_org_pat_type_idx",
            ),
            models.Index(
                fields=("organization", "patient", "clinical_status"),
                name="medhist_org_pat_status_idx",
            ),
            models.Index(
                fields=("patient", "onset_date"), name="medhist_patient_onset_idx"
            ),
        ]

    def clean(self) -> None:
        """Clean."""
        super().clean()
        if (
            self.onset_date
            and self.resolved_date
            and self.resolved_date < self.onset_date
        ):
            raise ValidationError(
                {"resolved_date": _("Resolved date cannot be before onset date.")}
            )
        if self.clinical_status == ClinicalStatus.RESOLVED and not self.resolved_date:
            raise ValidationError(
                {"resolved_date": _("Resolved histories require a resolved date.")}
            )
        if (
            self.history_type == MedicalHistoryType.FAMILY_HISTORY
            and not self.relationship
        ):
            raise ValidationError(
                {"relationship": _("Family-history entries require a relationship.")}
            )

    def normalize(self) -> None:
        """Normalize."""
        self.title = (self.title or "").strip()
        self.description = (self.description or "").strip()
        self.recorded_by = (self.recorded_by or "").strip()

    def __str__(self) -> str:
        """str  ."""
        return f"{self.title} - {self.patient_id}"


__all__ = ("PatientMedicalHistory",)
