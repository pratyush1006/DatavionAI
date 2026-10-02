"""Compliance API serializers."""

from __future__ import annotations

from rest_framework import serializers

from apps.compliance.models import Consent, PhiAccessLog


class ConsentSerializer(serializers.ModelSerializer[Consent]):
    """Serialize organization-scoped patient consent records."""

    class Meta:
        model = Consent
        fields = (
            "id",
            "patient",
            "organization",
            "purpose",
            "status",
            "granted_by",
            "granted_at",
            "revoked_at",
            "expires_at",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "organization",
            "granted_by",
            "granted_at",
            "revoked_at",
            "created_at",
            "updated_at",
        )


class PhiAccessLogSerializer(serializers.ModelSerializer[PhiAccessLog]):
    """Serialize immutable PHI access audit records."""

    class Meta:
        model = PhiAccessLog
        fields = (
            "id",
            "actor",
            "organization",
            "patient",
            "action",
            "resource_type",
            "resource_id",
            "ip_address",
            "user_agent",
            "justification",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


__all__ = ["ConsentSerializer", "PhiAccessLogSerializer"]
