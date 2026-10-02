"""
Tenant selection serializer.

Used when an authenticated user
selects an active organization.
"""

from __future__ import annotations

from rest_framework import serializers


class TenantSelectSerializer(
    serializers.Serializer,
):
    """
    Validate tenant selection request.
    """

    tenant_id = serializers.UUIDField()


__all__ = ("TenantSelectSerializer",)
