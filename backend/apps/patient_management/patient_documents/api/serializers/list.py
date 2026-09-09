"""Patient Document list serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.patient_documents.models import (
    PatientDocument,
)


class PatientDocumentListSerializer(
    serializers.ModelSerializer,
):
    """Serialize safe list metadata for patient documents."""

    class Meta:
        """Serializer metadata."""

        model = PatientDocument
        fields = (
            "id",
            "patient",
            "title",
            "category",
            "status",
            "original_filename",
            "mime_type",
            "file_size",
            "checksum",
            "is_confidential",
            "uploaded_at",
            "archived_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


__all__ = ("PatientDocumentListSerializer",)
