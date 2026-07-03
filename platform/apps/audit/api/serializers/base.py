"""
Base serializers for the Audit application.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.audit.models import AuditLog


class AuditBaseSerializer(serializers.ModelSerializer):
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
            "ip_address",
            "user_agent",
        )

        read_only_fields = fields
