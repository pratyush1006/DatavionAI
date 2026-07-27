"""
ClinicalNote model.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.encounters.models import Encounter
from apps.clinical.patients.models import Patient
from apps.core.models import BaseManager, BaseModel
from apps.notes.constants.notes import DEFAULT_NOTE_TYPE, NoteType
from apps.organization.employees.models import Employee
from apps.platform.organizations.models import Organization


class ClinicalNote(BaseModel):
    """
    Represents a clinical note or encounter note.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="clinical_notes",
        help_text="Organization that owns the note.",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="clinical_notes",
        help_text="Patient associated with this note.",
    )

    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.CASCADE,
        related_name="clinical_note_records",
        null=True,
        blank=True,
        help_text="Encounter associated with this note.",
    )

    note_type = models.CharField(
        max_length=50,
        choices=NoteType.choices,
        default=DEFAULT_NOTE_TYPE,
        help_text="Type of clinical note.",
    )

    title = models.CharField(
        max_length=255,
        help_text="Note title.",
    )

    content = models.JSONField(
        blank=True,
        default=dict,
        help_text="Structured note content.",
    )

    raw_text = models.TextField(
        blank=True,
        help_text="Raw text transcription or voice-to-text content.",
    )

    is_amended = models.BooleanField(
        default=False,
        help_text="Whether the note has been amended.",
    )

    amendment_reason = models.TextField(
        blank=True,
        help_text="Reason for amending the note.",
    )

    original_note = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="amendments",
        null=True,
        blank=True,
        help_text="Original note if this is an amendment.",
    )

    signed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the note was signed.",
    )

    signed_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        related_name="signed_notes",
        null=True,
        blank=True,
        help_text="Employee who signed the note.",
    )

    created_by = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="created_clinical_notes",
        help_text="Employee who created the note.",
    )

    class Meta:
        db_table = "clinical_notes"

        verbose_name = "Clinical Note"

        verbose_name_plural = "Clinical Notes"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "patient",
                    "created_at",
                ],
                name="clin_note_pat_created_idx",
            ),
            models.Index(
                fields=[
                    "encounter",
                    "created_at",
                ],
                name="clin_note_enc_created_idx",
            ),
            models.Index(
                fields=[
                    "organization",
                    "note_type",
                ],
                name="clinical_note_org_type_idx",
            ),
            models.Index(
                fields=[
                    "created_by",
                    "created_at",
                ],
                name="clin_note_auth_created_idx",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the note display string.
        """

        return f"{self.title} - {self.patient.full_name}"


__all__ = [
    "ClinicalNote",
]
