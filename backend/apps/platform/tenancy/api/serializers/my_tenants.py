"""
User tenant serializer.

Used for organization switcher.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.platform.tenancy.models import (
    TenantMembership,
)


class MyTenantSerializer(
    serializers.ModelSerializer,
):
    """
    Tenant information available
    for authenticated user.
    """

    id = serializers.UUIDField(
        source="tenant.id",
    )

    name = serializers.CharField(
        source="tenant.name",
    )

    tenant_type = serializers.CharField(
        source="tenant.tenant_type",
    )

    status = serializers.CharField(
        source="tenant.status",
    )

    role = serializers.SerializerMethodField()

    class Meta:
        model = TenantMembership

        fields = (
            "id",
            "name",
            "tenant_type",
            "status",
            "role",
            "is_owner",
            "joined_at",
        )

    def get_role(
        self,
        obj: TenantMembership,
    ) -> str:
        """
        Resolve user tenant role.
        """

        if obj.is_owner:
            return "OWNER"

        return "MEMBER"


__all__ = ("MyTenantSerializer",)
