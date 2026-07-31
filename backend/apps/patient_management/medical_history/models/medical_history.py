"""
Medical History models.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.patient_management.constants import RelationshipType
from apps.patient_management.medical_history.constants import (
    ClinicalStatus,
    MedicalHistoryType,
)
from apps.platform.organizations.models import Organization


class PatientMedicalHistory(BaseModel):
    """
    A medical history entry for a patient.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="patient_medical_histories",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="medical_history",
    )

    history_type = models.CharField(
        max_length=20,
        choices=MedicalHistoryType.choices,
        default=MedicalHistoryType.CONDITION,
        db_index=True,
    )

    title = models.CharField(
        max_length=255,
        help_text="Condition / procedure / item name.",
    )

    description = models.TextField(
        blank=True,
    )

    clinical_status = models.CharField(
        max_length=20,
        choices=ClinicalStatus.choices,
        default=ClinicalStatus.ACTIVE,
    )

    onset_date = models.DateField(
        null=True,
        blank=True,
    )

    resolved_date = models.DateField(
        null=True,
        blank=True,
    )

    relationship = models.CharField(
        max_length=20,
        choices=RelationshipType.choices,
        blank=True,
        help_text="Relationship, used for family history entries.",
    )

    is_smoker = models.BooleanField(
        null=True,
        blank=True,
        help_text="Social history: smoking status.",
    )

    alcohol_use = models.CharField(
        max_length=20,
        blank=True,
        help_text="Social history: alcohol use level.",
    )

    recorded_by = models.CharField(
        max_length=150,
        blank=True,
    )

    class Meta:
        db_table = "patient_medical_histories"

        verbose_name = "Patient Medical History"

        verbose_name_plural = "Patient Medical Histories"

        ordering = (
            "-onset_date",
            "-created_at",
        )

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                    "history_type",
                ],
                name="medhist_org_pat_type_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.get_history_type_display()}: {self.title}"


__all__ = [
    "PatientMedicalHistory",
]
