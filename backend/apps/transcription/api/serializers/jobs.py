"""
API serializers for transcription jobs.
"""

from __future__ import annotations

from apps.transcription.constants import SourceType, TranscriptionProvider
from apps.transcription.models import TranscriptionJob
from rest_framework import serializers


class TranscriptionJobCreateSerializer(serializers.Serializer):
    patient = serializers.UUIDField()
    encounter = serializers.UUIDField(required=False, allow_null=True)
    audio_uri = serializers.URLField(max_length=2048)
    audio_mime_type = serializers.CharField(required=False, allow_blank=True)
    idempotency_key = serializers.CharField(max_length=128)
    source_type = serializers.ChoiceField(
        choices=SourceType.choices,
        default=SourceType.UPLOAD,
    )
    provider = serializers.ChoiceField(
        choices=TranscriptionProvider.choices,
        default=TranscriptionProvider.OPENAI_WHISPER,
    )
    language = serializers.CharField(max_length=20, default="en")
    metadata = serializers.JSONField(required=False)


class TranscriptionJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptionJob
        fields = (
            "id",
            "job_id",
            "organization",
            "patient",
            "encounter",
            "created_by",
            "idempotency_key",
            "source_type",
            "provider",
            "status",
            "audio_uri",
            "audio_mime_type",
            "language",
            "requested_at",
            "started_at",
            "completed_at",
            "failed_at",
            "transcript_text",
            "transcript_json",
            "speaker_count",
            "duration_seconds",
            "error_code",
            "error_message",
            "metadata",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields
