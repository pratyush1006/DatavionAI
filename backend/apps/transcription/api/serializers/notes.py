"""
API serializers for generated clinical notes.
"""

from __future__ import annotations

from apps.transcription.models import GeneratedNote
from rest_framework import serializers


class ClinicalNoteGenerateSerializer(serializers.Serializer):
    note_type = serializers.CharField(max_length=50, default="soap")


class ClinicalNoteReviewSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=("approve", "reject"))
    rejection_reason = serializers.CharField(
        required=False,
        allow_blank=True,
    )


class GeneratedNoteUpdateSerializer(serializers.Serializer):
    draft_text = serializers.CharField(allow_blank=False)


class GeneratedNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedNote
        fields = (
            "id",
            "note_id",
            "organization",
            "job",
            "patient",
            "encounter",
            "clinical_note",
            "status",
            "note_type",
            "draft_text",
            "structured_content",
            "generated_by_provider",
            "reviewed_by",
            "reviewed_at",
            "signed_at",
            "rejection_reason",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields
