"""
Master Patient Index record model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.mpi.constants import MPIRecordStatus
from apps.patient_management.mpi.managers import MPIRecordManager
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


class MPIRecord(BaseModel):
    """Organization-scoped identity index record for one canonical Patient."""

    objects = MPIRecordManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="mpi_records",
    )
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name="mpi_record",
    )
    enterprise_identifier = models.CharField(
        max_length=100,
        db_index=True,
    )
    status = models.CharField(
        max_length=20,
        choices=MPIRecordStatus.choices,
        default=MPIRecordStatus.ACTIVE,
        db_index=True,
    )
    source_system = models.CharField(
        max_length=100,
        blank=True,
    )
    source_patient_identifier = models.CharField(
        max_length=150,
        blank=True,
    )
    match_score = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=0,
    )
    confidence = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=0,
    )
    demographics_snapshot = models.JSONField(
        default=dict,
        blank=True,
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    reviewed_by_id = models.UUIDField(
        null=True,
        blank=True,
    )
    merged_into = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="merged_records",
    )

    class Meta:
        """Database metadata for MPI records."""

        db_table = "patient_mpi_records"
        ordering = ("enterprise_identifier",)
        indexes = [
            models.Index(
                fields=("organization", "status"),
                name="mpi_record_org_status_idx",
            ),
            models.Index(
                fields=("organization", "source_system", "source_patient_identifier"),
                name="mpi_record_source_idx",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "enterprise_identifier"),
                name="unique_mpi_enterprise_id_per_org",
            ),
        ]

    def __str__(self) -> str:
        """Return a human-readable MPI record."""

        return self.enterprise_identifier


__all__ = ("MPIRecord",)
