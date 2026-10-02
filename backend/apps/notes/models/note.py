from __future__ import annotations

import uuid

from django.core.exceptions import ValidationError
from django.db import models

from apps.clinical.encounters.models import Encounter
from apps.core.models import BaseManager, BaseModel
from apps.notes.constants import NoteSource, NoteStatus, NoteType
from apps.platform.organizations.models import Organization


class ClinicalNote(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="clinical_notes"
    )
    patient = models.ForeignKey(
        "patient_core.Patient", on_delete=models.CASCADE, related_name="clinical_notes"
    )
    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="note_records",
    )
    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="authored_clinical_notes",
    )
    signed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="signed_clinical_notes",
    )
    note_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    note_type = models.CharField(
        max_length=32, choices=NoteType.choices, default=NoteType.SOAP
    )
    source = models.CharField(
        max_length=24, choices=NoteSource.choices, default=NoteSource.MANUAL
    )
    status = models.CharField(
        max_length=20,
        choices=NoteStatus.choices,
        default=NoteStatus.DRAFT,
        db_index=True,
    )
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    structured_content = models.JSONField(default=dict, blank=True)
    version = models.PositiveIntegerField(default=1)
    signed_at = models.DateTimeField(null=True, blank=True)
    locked_at = models.DateTimeField(null=True, blank=True)
    transcription_job_id = models.UUIDField(null=True, blank=True)
    telemedicine_session_id = models.UUIDField(null=True, blank=True)
    document_reference = models.CharField(max_length=512, blank=True)
    storage_reference = models.CharField(max_length=512, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "clinical_notes"
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("organization", "status"), name="clin_note_org_status_idx"
            ),
            models.Index(
                fields=("patient", "created_at"), name="clin_note_patient_created_idx"
            ),
            models.Index(
                fields=("encounter", "created_at"), name="clin_note_enc_created_idx"
            ),
            models.Index(
                fields=("organization", "note_type"), name="clin_note_org_type_idx"
            ),
        ]

    def clean(self):
        super().clean()
        if self.encounter_id:
            org_id = (
                Encounter.objects.filter(pk=self.encounter_id)
                .values_list("organization_id", flat=True)
                .first()
            )
            if org_id and org_id != self.organization_id:
                raise ValidationError(
                    {"encounter": "Encounter belongs to another organization."}
                )

    def __str__(self):
        return f"{self.note_id} | {self.status} | {self.title}"
