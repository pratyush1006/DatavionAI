"""
Clinical transcription persistence models.
"""

from __future__ import annotations

import uuid

from django.core.exceptions import ValidationError
from django.db import models

from apps.clinical.encounters.models import Encounter
from apps.core.models import BaseManager, BaseModel
from apps.notes.models import ClinicalNote
from apps.platform.organizations.models import Organization
from apps.transcription.constants import (
    NoteStatus,
    SourceType,
    TranscriptionProvider,
    TranscriptionStatus,
)


class TranscriptionJob(BaseModel):
    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="transcription_jobs",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.CASCADE,
        related_name="transcription_jobs",
    )
    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transcription_jobs",
    )
    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="created_transcription_jobs",
    )
    job_id = models.UUIDField(default=uuid.uuid4, editable=False)
    idempotency_key = models.CharField(max_length=128)
    source_type = models.CharField(
        max_length=20,
        choices=SourceType.choices,
        default=SourceType.UPLOAD,
    )
    provider = models.CharField(
        max_length=40,
        choices=TranscriptionProvider.choices,
        default=TranscriptionProvider.OPENAI_WHISPER,
    )
    status = models.CharField(
        max_length=20,
        choices=TranscriptionStatus.choices,
        default=TranscriptionStatus.CREATED,
        db_index=True,
    )
    audio_uri = models.URLField(max_length=2048, blank=True, default="")
    audio_mime_type = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=20, default="en")
    requested_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)
    transcript_text = models.TextField(blank=True)
    transcript_json = models.JSONField(default=dict, blank=True)
    speaker_count = models.PositiveIntegerField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    error_code = models.CharField(max_length=100, blank=True)
    error_message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "transcription_jobs"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("job_id",),
                name="trans_job_jobid_uniq",
            ),
            models.UniqueConstraint(
                fields=("organization", "idempotency_key"),
                name="trans_job_org_idem_uniq",
            ),
        ]
        indexes = [
            models.Index(
                fields=("organization", "status"),
                name="trans_job_org_status_idx",
            ),
            models.Index(
                fields=("patient", "created_at"),
                name="trans_job_pat_created_idx",
            ),
            models.Index(
                fields=("encounter", "created_at"),
                name="trans_job_enc_created_idx",
            ),
        ]

    def clean(self) -> None:
        super().clean()

        if self.encounter_id:
            encounter_org = (
                Encounter.objects.filter(pk=self.encounter_id)
                .values_list("organization_id", flat=True)
                .first()
            )
            if encounter_org and encounter_org != self.organization_id:
                raise ValidationError(
                    {"encounter": "Encounter belongs to another organization."}
                )

    def __str__(self) -> str:
        return f"{self.job_id} | {self.status}"


class GeneratedNote(BaseModel):
    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="generated_transcription_notes",
    )
    job = models.OneToOneField(
        TranscriptionJob,
        on_delete=models.CASCADE,
        related_name="generated_note",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.CASCADE,
        related_name="generated_transcription_notes",
    )
    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_transcription_notes",
    )
    clinical_note = models.OneToOneField(
        ClinicalNote,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_from_transcription",
    )
    note_id = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.CharField(
        max_length=20,
        choices=NoteStatus.choices,
        default=NoteStatus.DRAFT,
        db_index=True,
    )
    note_type = models.CharField(max_length=50, default="soap")
    draft_text = models.TextField()
    structured_content = models.JSONField(default=dict, blank=True)
    generated_by_provider = models.CharField(max_length=100, blank=True)
    reviewed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_transcription_notes",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    signed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    class Meta:
        db_table = "transcription_generated_notes"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("note_id",),
                name="trans_note_noteid_uniq",
            ),
        ]
        indexes = [
            models.Index(
                fields=("organization", "status"),
                name="trans_note_org_status_idx",
            ),
            models.Index(
                fields=("patient", "created_at"),
                name="trans_note_pat_created_idx",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        if self.encounter_id:
            encounter_org = (
                Encounter.objects.filter(pk=self.encounter_id)
                .values_list("organization_id", flat=True)
                .first()
            )
            if encounter_org and encounter_org != self.organization_id:
                raise ValidationError(
                    {"encounter": "Encounter belongs to another organization."}
                )
        if self.clinical_note_id:
            note_org = (
                ClinicalNote.objects.filter(pk=self.clinical_note_id)
                .values_list("organization_id", flat=True)
                .first()
            )
            if note_org and note_org != self.organization_id:
                raise ValidationError(
                    {"clinical_note": "Clinical note belongs to another organization."}
                )

    def __str__(self) -> str:
        return f"{self.note_id} | {self.status}"


__all__ = ("GeneratedNote", "TranscriptionJob")
