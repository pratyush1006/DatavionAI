"""
Document detail serializer.
"""

from __future__ import annotations

from apps.documents.api.serializers.base import (
    DocumentBaseSerializer,
)


class DocumentDetailSerializer(
    DocumentBaseSerializer,
):
    """
    Detailed document representation.
    """


__all__ = ("DocumentDetailSerializer",)
