"""
Base document serializers.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.documents.models import (
    Document,
)


class DocumentBaseSerializer(
    serializers.ModelSerializer,
):
    """
    Common document serializer fields.
    """

    class Meta:
        model = Document

        fields = (
            "id",
            "tenant",
            "organization",
            "title",
            "document_type",
            "status",
            "access_level",
            "storage_key",
            "original_filename",
            "mime_type",
            "file_size",
            "checksum",
            "metadata",
            "ai_metadata",
            "archived_at",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "status",
            "archived_at",
            "created_at",
            "updated_at",
        )


__all__ = ("DocumentBaseSerializer",)
