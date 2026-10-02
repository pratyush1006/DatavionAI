"""
Base serializers for the Audit application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.audit.models import AuditLog


class AuditBaseSerializer(
    serializers.ModelSerializer,
):
    """
    Base serializer shared across Audit serializers.
    """

    class Meta:
        model = AuditLog

        fields = (
            "id",
            "created_at",
            "organization",
            "user",
            "action",
            "module",
            "object_type",
            "object_id",
            "old_values",
            "new_values",
            "request_id",
            "correlation_id",
            "session_key",
            "ip_address",
            "user_agent",
            "http_method",
            "request_path",
            "status_code",
            "success",
            "error_message",
        )

        read_only_fields = fields


__all__ = [
    "AuditBaseSerializer",
]
