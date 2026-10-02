"""
Document list serializer.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.documents.models import (
    Document,
)


class DocumentListSerializer(
    serializers.ModelSerializer,
):
    """
    Lightweight document listing serializer.
    """

    class Meta:
        model = Document

        fields = (
            "id",
            "title",
            "document_type",
            "status",
            "access_level",
            "original_filename",
            "mime_type",
            "file_size",
            "created_at",
            "updated_at",
        )


__all__ = ("DocumentListSerializer",)
