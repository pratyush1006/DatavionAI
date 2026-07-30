"""
Coding models.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.constants import CodeSystem


class ChargeCoding(BaseModel):
    """
    A diagnosis / procedure coding entry attached to a patient encounter
    for billing purposes.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="charge_codings",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="charge_codings",
    )

    code_system = models.CharField(
        max_length=20,
        choices=CodeSystem.choices,
        default=CodeSystem.CPT,
    )

    code = models.CharField(
        max_length=30,
        help_text="Coded value (e.g. CPT / ICD-10).",
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    encoded_at = models.DateTimeField(
        auto_now_add=True,
    )

    coded_by = models.CharField(
        max_length=150,
        blank=True,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    modifier = models.CharField(
        max_length=20,
        blank=True,
        help_text="Procedure modifier, if any.",
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "charge_codings"

        verbose_name = "Charge Coding Entry"

        verbose_name_plural = "Charge Coding Entries"

        ordering = ("-encoded_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "patient",
                    "code_system",
                ],
                name="coding_org_pat_sys_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "patient",
                    "code_system",
                    "code",
                ],
                name="unique_coding_entry",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.get_code_system_display()}: {self.code}"


__all__ = [
    "ChargeCoding",
]
