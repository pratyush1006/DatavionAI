"""Patient Document detail serializer."""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.patient_documents.models import (
    PatientDocument,
)


class PatientDocumentDetailSerializer(
    serializers.ModelSerializer,
):
    """Serialize Patient Document detail without exposing storage internals."""

    class Meta:
        """Serializer metadata."""

        model = PatientDocument
        fields = (
            "id",
            "organization",
            "patient",
            "title",
            "category",
            "status",
            "description",
            "original_filename",
            "mime_type",
            "file_size",
            "checksum",
            "is_confidential",
            "metadata",
            "uploaded_at",
            "archived_at",
            "created_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


__all__ = ("PatientDocumentDetailSerializer",)
