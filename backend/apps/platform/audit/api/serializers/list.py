"""
List serializer for the Audit application.
"""

from __future__ import annotations

from apps.platform.audit.api.serializers.base import (
    AuditBaseSerializer,
)


class AuditListSerializer(
    AuditBaseSerializer,
):
    """
    Serializer used for listing audit logs.
    """

    class Meta(
        AuditBaseSerializer.Meta,
    ):
        fields = (
            "id",
            "created_at",
            "organization",
            "user",
            "action",
            "module",
            "object_type",
            "object_id",
            "success",
        )

        read_only_fields = fields


__all__ = [
    "AuditListSerializer",
]
