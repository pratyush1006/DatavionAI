"""
Detail serializer for the Audit application.
"""

from __future__ import annotations

from apps.audit.api.serializers.base import AuditBaseSerializer


class AuditDetailSerializer(AuditBaseSerializer):
    """
    Serializer used for retrieving a single audit log.
    """

    class Meta(AuditBaseSerializer.Meta):
        fields = AuditBaseSerializer.Meta.fields
        read_only_fields = fields
