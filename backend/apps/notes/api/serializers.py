from rest_framework import serializers

from apps.notes.models import ClinicalNote, ClinicalNoteAmendment, ClinicalNoteTemplate


class ClinicalNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalNote
        fields = (
            "note_id",
            "patient",
            "encounter",
            "author",
            "signed_by",
            "note_type",
            "source",
            "status",
            "title",
            "body",
            "structured_content",
            "version",
            "signed_at",
            "locked_at",
            "transcription_job_id",
            "telemedicine_session_id",
            "document_reference",
            "storage_reference",
            "metadata",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "note_id",
            "author",
            "signed_by",
            "status",
            "version",
            "signed_at",
            "locked_at",
            "document_reference",
            "storage_reference",
            "created_at",
            "updated_at",
        )


class ClinicalNoteAmendmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalNoteAmendment
        fields = "__all__"
        read_only_fields = (
            "amendment_id",
            "organization",
            "requested_by",
            "reviewed_by",
            "status",
            "reviewed_at",
            "created_at",
            "updated_at",
        )


class ClinicalNoteTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalNoteTemplate
        fields = "__all__"
        read_only_fields = ("organization", "created_at", "updated_at")
