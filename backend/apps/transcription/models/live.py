"""Persistent live transcription sessions and ordered transcript segments."""

from __future__ import annotations

import uuid

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.platform.organizations.models import Organization
from apps.transcription.constants.live import (
    LiveSegmentKind,
    LiveSessionStatus,
    LiveSource,
)


class LiveTranscriptionSession(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="live_transcription_sessions",
    )
    patient = models.ForeignKey(
        "patient_core.Patient",
        on_delete=models.CASCADE,
        related_name="live_transcription_sessions",
    )
    encounter = models.ForeignKey(
        "encounters.Encounter",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="live_transcription_sessions",
    )
    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="created_live_transcription_sessions",
    )
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(
        max_length=24,
        choices=LiveSessionStatus.choices,
        default=LiveSessionStatus.CREATED,
        db_index=True,
    )
    source = models.CharField(
        max_length=30, choices=LiveSource.choices, default=LiveSource.BROWSER
    )
    device_id = models.UUIDField(null=True, blank=True)
    telemedicine_session_id = models.UUIDField(null=True, blank=True)
    appointment_id = models.UUIDField(null=True, blank=True)
    audio_mime_type = models.CharField(max_length=100, default="audio/webm")
    language = models.CharField(max_length=20, default="en")
    provider = models.CharField(max_length=80, blank=True)
    sequence_number = models.PositiveBigIntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    last_audio_at = models.DateTimeField(null=True, blank=True)
    websocket_ticket_hash = models.CharField(max_length=64, blank=True, default="")
    websocket_ticket_expires_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "transcription_live_sessions"
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "session_id"),
                name="trans_live_org_session_uniq",
            )
        ]
        indexes = [
            models.Index(
                fields=("organization", "status"), name="trans_live_org_status_idx"
            ),
            models.Index(
                fields=("patient", "created_at"), name="trans_live_pat_created_idx"
            ),
            models.Index(
                fields=("device_id", "status"), name="trans_live_device_status_idx"
            ),
            models.Index(
                fields=("telemedicine_session_id", "status"),
                name="trans_live_tm_status_idx",
            ),
        ]


class LiveTranscriptSegment(BaseModel):
    objects = BaseManager()
    session = models.ForeignKey(
        LiveTranscriptionSession, on_delete=models.CASCADE, related_name="segments"
    )
    segment_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    sequence = models.PositiveBigIntegerField()
    kind = models.CharField(max_length=16, choices=LiveSegmentKind.choices)
    speaker_label = models.CharField(max_length=120, blank=True)
    text = models.TextField()
    start_ms = models.PositiveBigIntegerField(null=True, blank=True)
    end_ms = models.PositiveBigIntegerField(null=True, blank=True)
    confidence = models.DecimalField(
        max_digits=6, decimal_places=5, null=True, blank=True
    )
    provider_segment_id = models.CharField(max_length=255, blank=True)
    is_current = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "transcription_live_segments"
        constraints = [
            models.UniqueConstraint(
                fields=("session", "sequence"), name="trans_live_seg_seq_uniq"
            )
        ]
        indexes = [
            models.Index(fields=("session", "kind"), name="trans_live_seg_kind_idx"),
            models.Index(fields=("session", "sequence"), name="trans_live_seg_seq_idx"),
        ]
