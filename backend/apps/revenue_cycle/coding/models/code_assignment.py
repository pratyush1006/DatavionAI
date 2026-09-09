from __future__ import annotations

"""Individual Coding assignment persistence model."""

from django.db import models

from apps.core.models.base import BaseModel

from ..constants import CodeSystem


class CodeAssignment(BaseModel):
    """Represent one assigned diagnosis, procedure, or modifier code."""

    coding_record = models.ForeignKey(
        "revenue_cycle.CodingRecord",
        on_delete=models.CASCADE,
        related_name="code_assignments",
    )
    code_system = models.CharField(
        max_length=32,
        choices=CodeSystem.choices,
    )
    code = models.CharField(max_length=64)
    description = models.CharField(
        max_length=512,
        blank=True,
    )
    sequence = models.PositiveIntegerField(default=1)
    present_on_admission = models.BooleanField(
        null=True,
        blank=True,
    )
    is_primary = models.BooleanField(default=False)
    evidence = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        app_label = "revenue_cycle"
        """Define CodeAssignment database metadata."""

        db_table = "revenue_cycle_code_assignments"
        ordering = ("sequence", "created_at")
        indexes = (
            models.Index(
                fields=("coding_record", "code_system", "code"),
                name="rc_code_record_system_code_idx",
            ),
        )
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "coding_record",
                    "code_system",
                    "code",
                    "sequence",
                ),
                name="rc_code_record_code_sequence_uniq",
            ),
        )


__all__ = ("CodeAssignment",)
