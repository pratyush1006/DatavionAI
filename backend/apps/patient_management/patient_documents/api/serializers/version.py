"""Serializers for Patient Document versions."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.patient_documents.models import (
    PatientDocumentVersion,
)


class PatientDocumentVersionSerializer(
    serializers.ModelSerializer,
):
    """Serialize immutable document-version metadata."""

    class Meta:
        """Serializer metadata."""

        model = PatientDocumentVersion
        fields = (
            "id",
            "patient_document",
            "version_number",
            "storage_key",
            "original_filename",
            "mime_type",
            "file_size",
            "checksum",
            "status",
            "notes",
            "created_by",
            "created_at",
        )
        read_only_fields = fields


class PatientDocumentVersionCreateSerializer(
    serializers.Serializer,
):
    """Validate creation of a new document version."""

    storage_key = serializers.CharField(
        max_length=500,
    )
    original_filename = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
    mime_type = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
    )
    file_size = serializers.IntegerField(
        min_value=0,
        required=False,
        default=0,
    )
    checksum = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
    )


__all__ = (
    "PatientDocumentVersionCreateSerializer",
    "PatientDocumentVersionSerializer",
)
