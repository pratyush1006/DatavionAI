"""
Document create serializer.
"""

from __future__ import annotations

from apps.documents.api.serializers.base import (
    DocumentBaseSerializer,
)


class DocumentCreateSerializer(
    DocumentBaseSerializer,
):
    """
    Serializer used for document creation.
    """

    class Meta(
        DocumentBaseSerializer.Meta,
    ):
        read_only_fields = (
            "id",
            "status",
            "archived_at",
            "created_at",
            "updated_at",
        )


__all__ = ("DocumentCreateSerializer",)
