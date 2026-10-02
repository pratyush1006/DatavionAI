"""
Master Patient Index candidate match model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseModel
from apps.patient_management.mpi.constants import MPIMatchStatus
from apps.patient_management.mpi.managers import MPIMatchManager
from apps.platform.organizations.models import Organization


class MPIMatchCandidate(BaseModel):
    """Store one reviewed candidate relationship between two MPI records."""

    objects = MPIMatchManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="mpi_match_candidates",
    )
    left_record = models.ForeignKey(
        "MPIRecord",
        on_delete=models.CASCADE,
        related_name="left_match_candidates",
    )
    right_record = models.ForeignKey(
        "MPIRecord",
        on_delete=models.CASCADE,
        related_name="right_match_candidates",
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=4,
    )
    status = models.CharField(
        max_length=20,
        choices=MPIMatchStatus.choices,
        default=MPIMatchStatus.PENDING,
        db_index=True,
    )
    evidence = models.JSONField(
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

    class Meta:
        """Database metadata for candidate matches."""

        db_table = "patient_mpi_match_candidates"
        ordering = ("-score", "-created_at")
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "left_record", "right_record"),
                name="unique_mpi_candidate_pair",
            ),
            models.CheckConstraint(
                condition=~models.Q(left_record=models.F("right_record")),
                name="mpi_candidate_records_distinct",
            ),
        ]
        indexes = [
            models.Index(
                fields=("organization", "status", "-score"),
                name="mpi_match_status_score_idx",
            ),
        ]

    def __str__(self) -> str:
        """Return a human-readable candidate representation."""

        return f"{self.left_record_id}:{self.right_record_id}"


__all__ = ("MPIMatchCandidate",)
