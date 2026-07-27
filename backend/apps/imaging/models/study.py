"""
Study model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.imaging.constants import DEFAULT_STUDY_STATUS, Modality, StudyStatus
from apps.platform.organizations.models import Organization


class Study(BaseModel):
    """
    Represents an imaging study within an organization.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="imaging_studies",
        help_text="Organization that owns the imaging study.",
    )

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="imaging_studies",
        help_text="Patient associated with the imaging study.",
    )

    study_instance_uid = models.CharField(
        max_length=255,
        unique=True,
        help_text="DICOM Study Instance UID.",
    )

    accession_number = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        help_text="Study accession number.",
    )

    study_date = models.DateField(
        help_text="Date the study was performed.",
    )

    modality = models.CharField(
        max_length=10,
        choices=Modality.choices,
        help_text="DICOM modality.",
    )

    study_description = models.TextField(
        blank=True,
        help_text="Description of the imaging study.",
    )

    referring_physician = models.CharField(
        max_length=255,
        blank=True,
        help_text="Referring physician name.",
    )

    status = models.CharField(
        max_length=20,
        choices=StudyStatus.choices,
        default=DEFAULT_STUDY_STATUS,
        db_index=True,
        help_text="Current study status.",
    )

    class Meta:
        db_table = "imaging_studies"

        verbose_name = "Imaging Study"

        verbose_name_plural = "Imaging Studies"

        ordering = (
            "-study_date",
            "-created_at",
        )

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "study_date",
                ],
                name="imaging_study_org_date_idx",
            ),
            models.Index(
                fields=[
                    "patient",
                    "study_date",
                ],
                name="imaging_study_patient_date_idx",
            ),
            models.Index(
                fields=[
                    "modality",
                    "study_date",
                ],
                name="img_study_modality_dt_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the study display name.
        """

        return f"{self.study_instance_uid} ({self.get_modality_display()})"


__all__ = [
    "Study",
]
