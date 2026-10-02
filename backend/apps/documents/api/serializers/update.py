"""
Document update serializer.
"""

from __future__ import annotations

from apps.documents.api.serializers.base import (
    DocumentBaseSerializer,
)


class DocumentUpdateSerializer(
    DocumentBaseSerializer,
):
    """
    Serializer used for document updates.
    """

    class Meta(
        DocumentBaseSerializer.Meta,
    ):
        fields = (
            "title",
            "document_type",
            "access_level",
            "metadata",
            "ai_metadata",
        )


__all__ = ("DocumentUpdateSerializer",)
