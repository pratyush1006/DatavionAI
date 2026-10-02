from django.db import models

from apps.clinical.diagnoses.constants import DiagnosisStatus, DiagnosisType
from apps.clinical.encounters.models import Encounter
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization


class Diagnosis(BaseModel):
    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="diagnoses",
    )
    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.CASCADE,
        related_name="diagnoses",
    )
    diagnosis_code = models.CharField(max_length=50, db_index=True)
    diagnosis_description = models.TextField(blank=True)
    diagnosis_type = models.CharField(
        max_length=20,
        choices=DiagnosisType.choices,
        default=DiagnosisType.SECONDARY,
        db_index=True,
    )
    status = models.CharField(
        max_length=20,
        choices=DiagnosisStatus.choices,
        default=DiagnosisStatus.ACTIVE,
        db_index=True,
    )
    is_primary = models.BooleanField(default=False)
    present_on_admission = models.BooleanField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "diagnoses"
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("diagnosis_code",), name="diagnoses_diagnos_3ecb67_idx"
            ),
            models.Index(fields=("status",), name="diagnoses_status_b3ae1b_idx"),
            models.Index(
                fields=("diagnosis_type",), name="diagnoses_diagnos_049279_idx"
            ),
            models.Index(fields=("encounter",), name="diagnoses_encount_1b4290_idx"),
            models.Index(fields=("organization",), name="diagnoses_organiz_c0ea99_idx"),
            models.Index(
                fields=("encounter", "is_primary"), name="diagnoses_encount_218ad8_idx"
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("encounter", "diagnosis_code", "diagnosis_type"),
                name="unique_diagnosis_per_encounter",
            ),
        ]

    def __str__(self):
        return f"{self.diagnosis_code} | {self.diagnosis_description} | {self.status}"
